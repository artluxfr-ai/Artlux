from pathlib import Path
from shutil import copytree, rmtree

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
ASSETS = ROOT / 'site-assets'

NAV = [
    ('/tecnica/', 'Técnica', 'tecnica'),
    ('/galeria/', 'Galeria', 'galeria'),
    ('/apercu/', 'Pré-visualização IA', 'apercu'),
    ('/envios/', 'Envios', 'envios'),
    ('/faq/', 'FAQ', 'faq'),
]


def header(active=''):
    links = ''.join(f'<a class="{"active" if slug == active else ""}" href="{url}">{name}</a>' for url, name, slug in NAV)
    return f'''<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="/" aria-label="Artlux, página inicial"><img src="/assets/artlux-logo.jpg" alt="ARTLUX"></a>
    <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" data-menu-toggle><span></span><span></span><span></span></button>
    <nav class="main-nav" data-main-nav>{links}<a class="nav-order {'active' if active == 'encomendar' else ''}" href="/encomendar/">Encomendar</a></nav>
  </div>
</header>'''


def footer():
    return '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div><img class="footer-logo" src="/assets/artlux-logo.jpg" alt="ARTLUX"><p class="footer-copy">Tapetes personalizados feitos à mão com máquina de tufting. Atelier em França.</p></div>
      <div><p class="footer-label">Contacto</p><a class="footer-email" href="mailto:artluxfr@gmail.com">artluxfr@gmail.com</a><p class="footer-small">Encomendas exclusivamente online · Envio para todo o mundo</p></div>
      <div><p class="footer-label">Garantias europeias</p><p class="footer-small">Pagamento seguro · Direito de retratação de 14 dias para produtos não personalizados · RGPD · Fios conformes à norma REACH</p><a class="text-link" href="/envios/">Envios e condições →</a></div>
    </div>
    <div class="footer-bottom"><span>© 2026 Artlux · Artes personalizadas · França</span><span>Feito à mão, ponto a ponto</span></div>
  </div>
</footer>'''


def page(title, description, body, active=''):
    return f'''<!doctype html>
<html lang="pt">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#09090a">
  <meta name="description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ARTLUX">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <title>{title}</title>
  <link rel="icon" type="image/jpeg" href="/assets/favicon.jpg">
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
{header(active)}
<main>{body}</main>
{footer()}
<script src="/assets/app.js" defer></script>
</body>
</html>'''


def home():
    categories = [
        ('01', 'Anime & manga', 'Personagens favoritas, em retrato ou cena completa.'),
        ('02', 'Clubes de futebol', 'Brasões, cores e números da sua equipa.'),
        ('03', 'Animais & retratos', 'A partir de uma fotografia sua.'),
        ('04', 'Logótipos & marcas', 'Para lojas, escritórios, estúdios e gaming setups.'),
    ]
    category_markup = ''.join(f'<article class="category"><span class="category-number">{n}</span><h3>{title}</h3><p>{text}</p></article>' for n, title, text in categories)
    gallery = [
        ('rug-anime.jpg', 'Anime', 'Retrato anime'), ('rug-football.jpg', 'Futebol', 'Brasão de clube'),
        ('rug-pet.jpg', 'Animais', 'O seu animal'), ('rug-luxe.jpg', 'Decoração', 'Flor-de-lis dourada'),
    ]
    gallery_markup = ''.join(f'<a class="gallery-card" href="/galeria/"><img src="/assets/{img}" alt="{name}: {title}"><span class="gallery-caption">{name}<strong>{title}</strong></span></a>' for img, name, title in gallery)
    body = f'''<section class="hero"><div class="container hero-content">
  <p class="eyebrow">Atelier em França · Feito à mão</p><h1>O seu desenho, <em class="italic">tecido em lã.</em></h1>
  <p class="lede">Tapetes personalizados de anime, clubes de futebol, animais e logótipos — tufados ponto a ponto com máquina de tufting e acabados à mão.</p>
  <div class="hero-actions"><a class="btn btn-gold" href="/encomendar/">Pedir orçamento</a><a class="btn" href="/apercu/">Pré-visualizar com IA</a></div>
</div></section>
<section class="trust-strip"><div class="container trust-list"><span class="trust-item"><b class="trust-icon">✧</b>100% personalizado</span><span class="trust-item"><b class="trust-icon">✂</b>Tufting manual</span><span class="trust-item"><b class="trust-icon">⌾</b>Normas europeias</span><span class="trust-item"><b class="trust-icon">◉</b>Envio mundial</span></div></section>
<section class="section"><div class="container"><p class="eyebrow">O que criamos</p><div class="section-head"><h2>Qualquer ideia, em tapete</h2></div><div class="category-grid">{category_markup}</div></div></section>
<section class="section gallery-preview"><div class="container"><div class="section-head"><div><p class="eyebrow">Galeria</p><h2>Exemplos do nosso trabalho</h2></div><a class="text-link" href="/galeria/">Ver tudo →</a></div><div class="gallery-grid">{gallery_markup}</div></div></section>
<section class="section process-section"><div class="container process-layout"><div><p class="eyebrow">Como funciona</p><h2>Do pedido à sua porta</h2><ol class="process-list"><li><span class="step">1.</span><span>Envie a imagem, o tamanho e o tema pelo formulário.</span></li><li><span class="step">2.</span><span>Recebe por email o orçamento e uma maquete digital.</span></li><li><span class="step">3.</span><span>Aprovada a maquete, tufamos e acabamos o tapete à mão (2–4 semanas).</span></li><li><span class="step">4.</span><span>Enviamos com seguimento para qualquer país.</span></li></ol><a class="btn btn-gold" href="/encomendar/">Começar a minha encomenda</a></div><aside class="tech-card"><p class="eyebrow">Saber-fazer</p><h3>A técnica de tufting</h3><p>Cada fio é inserido num tecido esticado num bastidor com uma pistola de tufting manual, guiada pela mão do artesão. Depois vêm a cola, o forro, o corte e a escultura do relevo.</p><a class="text-link" href="/tecnica/">Conhecer o processo →</a></aside></div></section>'''
    return page('ARTLUX — Tapetes personalizados de anime, futebol e mais', 'Tapetes feitos à mão com máquina de tufting em França. Anime, clubes de futebol, animais, logótipos. Encomenda online, envio para todo o mundo.', body)


def tecnica():
    stages = [
        ('I', 'Desenho e maquete', 'A sua imagem é vetorizada e simplificada em zonas de cor. Escolhemos os fios e enviamos a maquete para aprovação.'),
        ('II', 'Tecido primário no bastidor', 'Um tecido de tufting é esticado com força num bastidor. O desenho é projetado e traçado em espelho, pois trabalhamos pelo verso.'),
        ('III', 'Tufting com a pistola', 'O artesão perfura o tecido e insere o fio, linha a linha, cor a cor. Usamos cut pile e loop pile para textura e relevo.'),
        ('IV', 'Colagem', 'O verso recebe uma camada de cola de látex que fixa cada ponto. Após a secagem, os fios ficam permanentemente presos.'),
        ('V', 'Forro secundário', 'Aplicamos uma tela ou feltro no verso para dar estrutura, proteger o chão e esconder o trabalho técnico. Antiderrapante sob pedido.'),
        ('VI', 'Corte, escultura e acabamento', 'Recortamos o contorno, dobramos e colamos as bordas e nivelamos o pelo. Os contornos são esculpidos para dar relevo ao desenho.'),
    ]
    cards = ''.join(f'<article class="step-card"><span class="roman">{n}</span><h3>{t}</h3><p>{d}</p></article>' for n, t, d in stages)
    body = f'''<section class="page-hero"><div class="container"><p class="eyebrow">O nosso saber-fazer</p><h1>Tufting manual, <em class="italic">ponto a ponto</em></h1><p class="lede">O tufting é uma técnica de tapeçaria em que o fio é injetado num tecido esticado com uma pistola elétrica de mão. Não há impressão: cada cor é tufada à mão pelo artesão.</p><figure class="tech-hero-image"><img src="/assets/hero-tufting.jpg" alt="Pistola de tufting em ação no bastidor"></figure></div></section>
<section class="content-section"><div class="container content-narrow"><h2>As máquinas</h2><div class="machine-grid"><article class="machine-card"><h3>Cut pile</h3><p>A pistola corta o fio a cada ponto, criando um pelo macio e denso (10–25 mm). Ideal para retratos e degradês.</p></article><article class="machine-card"><h3>Loop pile</h3><p>O fio forma pequenas laçadas fechadas. Mais resistente e com textura, ótimo para contornos e brasões.</p></article></div><p>Combinando as duas e várias alturas de pelo, damos profundidade e relevo a cada desenho.</p><h2>As 6 etapas</h2><div class="step-grid">{cards}</div><h2>Materiais e cuidados</h2><p>Fios acrílicos ou de lã, conformes ao regulamento europeu REACH. O pelo, entre 10 e 25 mm, é esculpido à mão. Para cuidar da peça, aspire regularmente e trate manchas com um pano húmido; não lave na máquina. Recomendado para uso interior, decoração de parede ou chão.</p><a class="btn btn-gold" href="/encomendar/">Pedir o meu tapete</a><figure class="finish-image"><img src="/assets/rug-finish.jpg" alt="Acabamento do verso com feltro"></figure></div></section>'''
    return page('A técnica de tufting — ARTLUX', 'Como fazemos os tapetes: desenho, bastidor, pistola de tufting manual, colagem, forro e acabamento à mão.', body, 'tecnica')


def galeria():
    items = [
        ('rug-anime.jpg', 'Anime', 'Retrato anime', 'Ø 90 cm · Cut pile 18 mm'),
        ('rug-football.jpg', 'Futebol', 'Brasão de clube', '80 × 100 cm · Cut + loop'),
        ('rug-pet.jpg', 'Animais', 'O seu animal', '70 × 75 cm · Cut pile 15 mm'),
        ('rug-luxe.jpg', 'Decoração', 'Flor-de-lis dourada', '120 × 150 cm · Cut pile 20 mm, esculpido'),
        ('hero-tufting.jpg', 'Processo', 'No atelier', 'Bastidor 150 × 150 cm · Tufting gun'),
        ('rug-finish.jpg', 'Processo', 'Acabamento', 'Feltro + cola · Corte das bordas'),
    ]
    cards = ''.join(f'<article class="gallery-card"><img src="/assets/{img}" alt="{title}"><span class="gallery-caption">{group}<strong>{title}</strong>{info}</span></article>' for img, group, title, info in items)
    body = f'''<section class="page-hero"><div class="container"><p class="eyebrow">Galeria</p><h1>Exemplos de <em class="italic">trabalho</em></h1><p class="lede">Cada peça é única e feita a partir da ideia de um cliente.</p></div></section><section class="content-section"><div class="container"><div class="all-gallery">{cards}</div><p style="margin-top:45px"><a class="btn btn-gold" href="/encomendar/">Quero o meu</a></p></div></section>'''
    return page('Galeria de tapetes — ARTLUX', 'Exemplos de tapetes tufados à mão: anime, clubes de futebol, animais e decoração.', body, 'galeria')


def apercu():
    body = '''<section class="page-hero"><div class="container"><p class="eyebrow">Pré-visualização IA</p><h1>Veja o seu tapete <em class="italic">antes de encomendar</em></h1><p class="lede">Envie uma imagem de referência (opcional), descreva o tapete e veja uma ideia visual do resultado. A maquete final é feita pelo nosso atelier.</p></div></section><section class="content-section"><div class="container preview-layout"><form class="form-panel" data-preview-form><h2>A sua ideia</h2><p>Junte uma referência e indique os detalhes que quer ver no tapete.</p><div class="form-field"><label for="reference">Imagem de referência</label><input id="reference" name="referencia" type="file" accept="image/png,image/jpeg"></div><div class="form-field"><label for="description">Descrição do tapete</label><textarea id="description" name="descricao" placeholder="Ex.: retrato do meu cão, fundo azul escuro, 80 × 100 cm..."></textarea></div><button class="btn btn-gold" type="submit">Gerar pré-visualização</button><p class="form-note">JPG/PNG, máx. 8 MB. A imagem é gerada por IA como referência; a maquete final é aprovada consigo por email.</p><p class="form-note" role="status" aria-live="polite" data-preview-status></p></form><aside class="preview-frame"><div class="preview-empty" data-preview-empty><div class="rings"></div><p>A sua pré-visualização aparece aqui.</p></div><div class="preview-result" data-preview-result><img src="" alt=""><p></p></div></aside></div></section>'''
    return page('Pré-visualização do seu tapete — ARTLUX', 'Envie uma imagem de referência, descreva o tapete e veja uma pré-visualização para o seu projeto.', body, 'apercu')


def envios():
    entries = [
        ('01', 'Encomendas 100% online', 'Não temos loja física. Todo o pedido — orçamento, maquete e pagamento — é feito online e por email.'),
        ('02', 'Envio para todo o mundo', 'Expedimos a partir de França com número de seguimento para a União Europeia e para todos os outros países. Envios fora da UE podem estar sujeitos a taxas alfandegárias do país de destino.'),
        ('03', 'Prazo de fabrico', 'Normalmente 2 a 4 semanas após aprovação da maquete, consoante o tamanho e a complexidade.'),
        ('04', 'Garantia legal de conformidade', 'Todos os produtos beneficiam da garantia legal de conformidade europeia de 2 anos contra defeitos de fabrico.'),
        ('05', 'Direito de retratação', 'Nos termos da diretiva europeia 2011/83/UE, os produtos fabricados segundo as especificações do cliente, ou seja, personalizados, estão excluídos do direito de retratação de 14 dias.'),
        ('06', 'Dados pessoais (RGPD)', 'Os seus dados e imagens são usados apenas para tratar a sua encomenda e nunca são partilhados ou vendidos.'),
        ('07', 'Direitos de imagem', 'Ao enviar um desenho, o cliente confirma que o pedido é para uso pessoal. Não reproduzimos marcas para revenda.'),
    ]
    rows = ''.join(f'<article class="condition"><span class="condition-mark">{n}</span><div><h3>{t}</h3><p>{d}</p></div></article>' for n, t, d in entries)
    body = f'''<section class="page-hero"><div class="container"><p class="eyebrow">Envios & condições</p><h1>Normas europeias, <em class="italic">entrega mundial</em></h1></div></section><section class="content-section"><div class="container content-narrow conditions">{rows}<p style="margin-top:33px">Dúvidas? Escreva para <a class="footer-email" href="mailto:artluxfr@gmail.com">artluxfr@gmail.com</a>.</p></div></section>'''
    return page('Envios e condições — ARTLUX', 'Encomendas exclusivamente online, envio para todo o mundo a partir de França, garantias e normas europeias.', body, 'envios')


def faq():
    faqs = [
        ('Que tamanhos fazem?', 'Trabalhamos desde formatos compactos até peças de grande dimensão. As opções mais pedidas são 60 × 90 cm, 80 × 120 cm, 100 × 150 cm e 120 × 180 cm; também fazemos medidas personalizadas e formatos redondos.'),
        ('Posso enviar qualquer imagem?', 'Pode enviar uma fotografia, ilustração, personagem, brasão ou logótipo. A imagem será simplificada em zonas de cor para obter um resultado nítido em tufting. Para pedidos de marcas, confirme que o uso é pessoal.'),
        ('Quanto tempo demora?', 'O prazo normal é de 2 a 4 semanas após a aprovação da maquete, variando com o tamanho e a complexidade do desenho.'),
        ('Enviam para o meu país?', 'Sim. Enviamos a partir de França com número de seguimento para a União Europeia e para outros destinos. Eventuais taxas aduaneiras fora da UE são da responsabilidade do destinatário.'),
        ('Como cuido do tapete?', 'Aspire regularmente e limpe pequenas manchas com um pano ligeiramente húmido. Não lave na máquina. Para manter a peça impecável, recomendamos uso em interior.'),
        ('Como peço um orçamento?', 'Use o formulário de encomenda com a sua ideia, tema, tamanho e país de entrega. Respondemos por email com orçamento e maquete digital. Também pode escrever diretamente para artluxfr@gmail.com.'),
    ]
    details = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    body = f'''<section class="page-hero"><div class="container"><p class="eyebrow">FAQ</p><h1>Perguntas <em class="italic">frequentes</em></h1><p class="lede">Tudo o que precisa de saber antes de imaginar a sua peça.</p></div></section><section class="content-section"><div class="container"><div class="faq-list">{details}</div></div></section>'''
    return page('Perguntas frequentes — ARTLUX', 'Tamanhos, prazos, materiais, envio e cuidados dos tapetes personalizados ARTLUX.', body, 'faq')


def encomendar():
    body = '''<section class="page-hero"><div class="container"><p class="eyebrow">Encomenda online</p><h1>Peça o seu <em class="italic">tapete</em></h1><p class="lede">Descreva a sua ideia. Respondemos por email com orçamento e maquete. Envie a imagem de referência em resposta ao nosso email ou diretamente para artluxfr@gmail.com.</p></div></section><section class="content-section"><div class="container order-layout"><form class="form-panel" data-order-form><h2>O seu projeto</h2><p>Preencha os detalhes essenciais. Ao enviar, o seu cliente de email abre uma mensagem já preparada para a Artlux.</p><noscript><p class="form-note">Sem JavaScript, envie a sua ideia diretamente para <a class="footer-email" href="mailto:artluxfr@gmail.com">artluxfr@gmail.com</a>.</p></noscript><div class="form-field"><label for="nome">Nome</label><input id="nome" name="nome" required autocomplete="name"></div><div class="form-field"><label for="email">Email</label><input id="email" name="email" type="email" required autocomplete="email"></div><div class="form-field"><label for="pais">País de entrega</label><input id="pais" name="pais" required autocomplete="country-name"></div><div class="form-field"><label for="tema">Tema</label><select id="tema" name="tema"><option>Anime / manga</option><option>Clube de futebol</option><option>Animal / retrato</option><option>Logótipo / marca</option><option>Outro</option></select></div><div class="form-field"><label for="tamanho">Tamanho</label><select id="tamanho" name="tamanho"><option>60 × 90 cm</option><option>80 × 120 cm</option><option>100 × 150 cm</option><option>120 × 180 cm</option><option>Redondo</option><option>Outro tamanho</option></select></div><div class="form-field"><label for="ideia">A sua ideia</label><textarea id="ideia" name="ideia" required placeholder="Conte-nos o motivo, as cores, a referência e os detalhes importantes."></textarea></div><button class="btn btn-gold" type="submit">Enviar pedido</button></form><aside class="tech-card"><p class="eyebrow">Próximos passos</p><h3>A sua ideia torna-se uma peça única.</h3><p>Depois de recebermos a mensagem, entraremos em contacto por email com orçamento e uma maquete digital. Só avançamos com o tufting após a sua aprovação.</p><p class="footer-label" style="margin-top:33px">Contacto direto</p><a class="footer-email" href="mailto:artluxfr@gmail.com">artluxfr@gmail.com</a></aside></div></section>'''
    return page('Encomendar um tapete — ARTLUX', 'Peça o orçamento do seu tapete personalizado: anime, futebol, animais, logótipos. Envio mundial.', body, 'encomendar')


def write_file(relative, content):
    target = DIST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')


def main():
    if DIST.exists():
        rmtree(DIST)
    DIST.mkdir()
    copytree(ASSETS, DIST / 'assets')
    (DIST / 'assets' / 'styles.css').write_text((ROOT / 'styles.css').read_text(encoding='utf-8'), encoding='utf-8')
    (DIST / 'assets' / 'app.js').write_text((ROOT / 'app.js').read_text(encoding='utf-8'), encoding='utf-8')
    write_file('index.html', home())
    write_file('tecnica/index.html', tecnica())
    write_file('galeria/index.html', galeria())
    write_file('apercu/index.html', apercu())
    write_file('envios/index.html', envios())
    write_file('faq/index.html', faq())
    write_file('encomendar/index.html', encomendar())
    write_file('404.html', page('Página não encontrada — ARTLUX', 'Esta página não existe.', '<section class="page-hero"><div class="container"><p class="eyebrow">404</p><h1>Página não <em class="italic">encontrada</em></h1><p class="lede">Volte à página inicial para conhecer os tapetes personalizados da Artlux.</p><a class="btn btn-gold" href="/">Ir para a página inicial</a></div></section>'))
    write_file('manus-routes.json', '{"routes":[{"path":"/","title":"ARTLUX — Tapetes personalizados"},{"path":"/tecnica/","title":"A técnica de tufting"},{"path":"/galeria/","title":"Galeria de tapetes"},{"path":"/apercu/","title":"Pré-visualização IA"},{"path":"/envios/","title":"Envios e condições"},{"path":"/faq/","title":"Perguntas frequentes"},{"path":"/encomendar/","title":"Encomendar um tapete"}]}')

if __name__ == '__main__':
    main()
