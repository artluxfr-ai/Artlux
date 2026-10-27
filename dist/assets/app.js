(() => {
  const toggle = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-main-nav]');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }));
  }

  const MAX_FILE_BYTES = 8 * 1024 * 1024;
  const fileToReference = (file) => new Promise((resolve, reject) => {
    if (!file) return resolve(null);
    if (!['image/jpeg', 'image/png'].includes(file.type)) return reject(new Error('Use uma imagem JPG ou PNG.'));
    if (file.size > MAX_FILE_BYTES) return reject(new Error('A imagem de referência deve ter, no máximo, 8 MB.'));
    const reader = new FileReader();
    reader.onerror = () => reject(new Error('Não foi possível ler a imagem selecionada.'));
    reader.onload = () => resolve({
      b64Json: String(reader.result).split(',')[1],
      mimeType: file.type,
    });
    reader.readAsDataURL(file);
  });

  const previewForm = document.querySelector('[data-preview-form]');
  if (previewForm) {
    const input = previewForm.querySelector('input[type=file]');
    const description = previewForm.querySelector('textarea');
    const button = previewForm.querySelector('button[type=submit]');
    const empty = document.querySelector('[data-preview-empty]');
    const result = document.querySelector('[data-preview-result]');
    const resultImage = result?.querySelector('img');
    const resultText = result?.querySelector('p');
    const status = document.querySelector('[data-preview-status]');
    const setStatus = (message, error = false) => {
      if (!status) return;
      status.textContent = message;
      status.classList.toggle('form-error', error);
    };

    previewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const idea = description?.value.trim() || '';
      if (idea.length < 8) {
        setStatus('Descreva a sua ideia em pelo menos 8 caracteres.', true);
        description?.focus();
        return;
      }
      try {
        button.disabled = true;
        button.textContent = 'A gerar…';
        setStatus('A criar a sua pré-visualização por IA. Isto pode demorar alguns segundos.');
        const reference = await fileToReference(input?.files?.[0]);
        const response = await fetch('/api/preview', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description: idea, reference }),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.image) throw new Error(data.error || 'Não foi possível gerar a pré-visualização agora.');
        if (resultImage) {
          resultImage.src = data.image.url || `data:${data.image.mimeType || 'image/png'};base64,${data.image.b64Json}`;
          resultImage.alt = `Pré-visualização de tapete: ${idea}`;
        }
        if (resultText) resultText.textContent = 'Pré-visualização gerada por IA. A maquete final é confirmada pelo atelier antes da produção.';
        empty?.setAttribute('hidden', '');
        result?.style.setProperty('display', 'block');
        setStatus('Pré-visualização pronta.');
      } catch (error) {
        setStatus(error.message || 'Ocorreu um erro ao gerar a pré-visualização.', true);
      } finally {
        button.disabled = false;
        button.textContent = 'Gerar pré-visualização';
      }
    });
  }

  document.querySelectorAll('[data-order-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const name = data.get('nome') || '';
      const subject = `Pedido de orçamento Artlux — ${name || 'novo cliente'}`;
      const lines = [
        'Olá Artlux,', '', 'Gostaria de pedir um orçamento para um tapete personalizado.', '',
        `Nome: ${data.get('nome') || ''}`, `Email: ${data.get('email') || ''}`,
        `País de entrega: ${data.get('pais') || ''}`, `Tema: ${data.get('tema') || ''}`,
        `Tamanho: ${data.get('tamanho') || ''}`, '', 'A minha ideia:', `${data.get('ideia') || ''}`,
      ];
      window.location.href = `mailto:artluxfr@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    });
  });
})();
