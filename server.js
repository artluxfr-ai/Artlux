const http = require('http');
const fs = require('fs/promises');
const path = require('path');

const PORT = Number(process.env.PORT || 3000);
const DIST = path.resolve(__dirname, 'dist');
const MAX_UPLOAD_BYTES = 8 * 1024 * 1024;
const MAX_JSON_BYTES = Math.ceil(MAX_UPLOAD_BYTES * 1.38) + 128 * 1024;

const MIME_TYPES = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.txt': 'text/plain; charset=utf-8',
};

function sendJson(response, status, payload) {
  response.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
  });
  response.end(JSON.stringify(payload));
}

function readJson(request) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    request.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_JSON_BYTES) {
        reject(Object.assign(new Error('O ficheiro excede o limite de 8 MB.'), { status: 413 }));
        request.destroy();
        return;
      }
      chunks.push(chunk);
    });
    request.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf8')));
      } catch {
        reject(Object.assign(new Error('Pedido inválido.'), { status: 400 }));
      }
    });
    request.on('error', () => reject(Object.assign(new Error('Não foi possível ler o pedido.'), { status: 400 })));
  });
}

function validateReference(reference) {
  if (!reference) return null;
  if (!['image/jpeg', 'image/png'].includes(reference.mimeType)) {
    throw Object.assign(new Error('Use uma imagem JPG ou PNG.'), { status: 400 });
  }
  if (typeof reference.b64Json !== 'string' || !reference.b64Json.length) {
    throw Object.assign(new Error('A imagem de referência é inválida.'), { status: 400 });
  }
  const approximateBytes = Math.floor((reference.b64Json.length * 3) / 4);
  if (approximateBytes > MAX_UPLOAD_BYTES) {
    throw Object.assign(new Error('A imagem de referência excede o limite de 8 MB.'), { status: 413 });
  }
  return { b64Json: reference.b64Json, mimeType: reference.mimeType };
}

async function generatePreview(request, response) {
  try {
    const payload = await readJson(request);
    const description = typeof payload.description === 'string' ? payload.description.trim() : '';
    if (description.length < 8 || description.length > 900) {
      throw Object.assign(new Error('Descreva a sua ideia em pelo menos 8 caracteres.'), { status: 400 });
    }
    const reference = validateReference(payload.reference);
    const apiUrl = process.env.MANUS_API_URL;
    const apiKey = process.env.MANUS_API_KEY;
    if (!apiUrl || !apiKey) {
      throw Object.assign(new Error('A geração por IA ainda não está disponível. Tente novamente dentro de instantes.'), { status: 503 });
    }

    const prompt = [
      'Create one photorealistic premium hand-tufted rug design as a product mockup.',
      'The rug must visibly use dense yarn fibres, cut-pile texture, carefully carved contours and a refined handmade finish.',
      'Place the single finished rug on a subtle studio floor with a dark, elegant background.',
      'Use the user request and any attached reference only as creative direction:',
      description,
      'Do not add text, labels, watermarks, borders, UI, packaging, or a collage.',
    ].join(' ');

    const apiResponse = await fetch(`${apiUrl.replace(/\/$/, '')}/images.v1.ImageService/GenerateImage`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'connect-protocol-version': '1',
      },
      body: JSON.stringify({
        prompt,
        ...(reference ? { originalImages: [reference] } : {}),
      }),
      signal: AbortSignal.timeout(90000),
    });
    const responseBody = await apiResponse.json().catch(() => ({}));
    if (!apiResponse.ok || responseBody.error || !responseBody.image) {
      const message = responseBody?.error?.message || responseBody?.message || 'Não foi possível gerar a pré-visualização agora.';
      throw Object.assign(new Error(message), { status: apiResponse.status || 502 });
    }
    sendJson(response, 200, { image: responseBody.image });
  } catch (error) {
    const status = Number.isInteger(error.status) && error.status >= 400 && error.status < 600 ? error.status : 500;
    sendJson(response, status, { error: error.message || 'Ocorreu um erro ao gerar a pré-visualização.' });
  }
}

async function serveStatic(requestUrl, response) {
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(requestUrl, 'http://localhost').pathname);
  } catch {
    response.writeHead(400).end('Pedido inválido.');
    return;
  }
  if (pathname.includes('\0')) {
    response.writeHead(400).end('Pedido inválido.');
    return;
  }
  const relativePath = pathname === '/' ? 'index.html' : `${pathname.replace(/^\/+/, '')}${pathname.endsWith('/') ? 'index.html' : ''}`;
  const absolutePath = path.resolve(DIST, relativePath);
  if (!absolutePath.startsWith(`${DIST}${path.sep}`) && absolutePath !== DIST) {
    response.writeHead(403).end('Acesso negado.');
    return;
  }
  try {
    const contents = await fs.readFile(absolutePath);
    const extension = path.extname(absolutePath).toLowerCase();
    response.writeHead(200, {
      'Content-Type': MIME_TYPES[extension] || 'application/octet-stream',
      'Cache-Control': extension === '.html' || extension === '.json' ? 'no-cache' : 'public, max-age=604800',
      'X-Content-Type-Options': 'nosniff',
    });
    response.end(contents);
  } catch {
    try {
      const notFound = await fs.readFile(path.join(DIST, '404.html'));
      response.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache' });
      response.end(notFound);
    } catch {
      response.writeHead(404).end('Página não encontrada.');
    }
  }
}

const server = http.createServer((request, response) => {
  const pathname = new URL(request.url, 'http://localhost').pathname;
  if (request.method === 'GET' && pathname === '/_app/health') {
    response.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
    response.end(JSON.stringify({ ok: true }));
    return;
  }
  if (request.method === 'POST' && pathname === '/api/preview') {
    generatePreview(request, response);
    return;
  }
  if (request.method === 'POST' && pathname === '/api/preview') return;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    response.writeHead(405, { Allow: 'GET, HEAD, POST' }).end('Método não permitido.');
    return;
  }
  if (request.method === 'HEAD') {
    response.writeHead(200).end();
    return;
  }
  serveStatic(request.url, response);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Artlux server listening on port ${PORT}`);
});
