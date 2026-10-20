import json, re, os

HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Marques da Costa</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,300..900;1,62..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="base.css">
</head>
<body>
"""

NAV = [("equipamentos", "Equipamentos"), ("acessorios", "Acessórios"), ("setores", "Setores"),
       ("onde-comprar", "Onde comprar"), ("empresa", "Empresa"), ("contato", "Contato")]


def header(active):
    links = "".join(f'<a href="{k}.html"{" class=\"on\"" if k == active else ""}>{v}</a>' for k, v in NAV)
    return f"""<header class="top">
  <a href="index.html"><img class="logo" src="img/logo_branca.png" alt="Marques da Costa"></a>
  <nav>{links}<a class="call" href="{WAURL}" target="_blank" rel="noopener"><svg class="wai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>Pedir orçamento</a></nav>
  <div class="burger" aria-hidden="true"><i></i><i></i><i></i></div>
</header>
"""


home_body = open("home.body.html").read()
FOOTER = re.search(r"(<footer>.*</footer>)", home_body, re.S).group(1)
WA = re.search(r'(<a class="wa-float".*?</a>)', home_body, re.S).group(1)


WAURL = "https://wa.me/5514997043457"
MAPS = "https://www.google.com/maps/search/?api=1&query="


def mmenu(active):
    items = [("index", "Início")] + NAV
    links = "".join(f'<a href="{k}.html"{" class=\"on\"" if k == (active or "index") else ""}>{v}</a>' for k, v in items)
    return f"""<div class="mmenu" id="mmenu" hidden><div class="hd"><img src="img/logo_branca.png" alt="Marques da Costa"><button class="x" type="button" aria-label="Fechar menu">×</button></div>
<nav>{links}</nav>
<div class="ft"><a class="btn wa" href="{WAURL}" target="_blank" rel="noopener">Pedir orçamento pelo WhatsApp</a><p>+55 14 99704-3457 · (14) 3425-2533<br>vendas@marquesdacosta.com.br</p></div></div>"""


COMMON_JS = """<script>
(function(){
  var m=document.getElementById('mmenu'),b=document.querySelector('.burger');
  if(b&&m){b.onclick=function(){m.hidden=false;document.body.style.overflow='hidden'};m.querySelector('.x').onclick=function(){m.hidden=true;document.body.style.overflow=''}}
  document.querySelectorAll('.form .send .btn').forEach(function(btn){btn.onclick=function(){
    var f=btn.closest('form'),t=['Olá! Vim pelo site da Marques da Costa.'];
    f.querySelectorAll('label').forEach(function(l){var i=l.querySelector('input,select,textarea');if(i&&i.value)t.push(l.childNodes[0].textContent.trim()+': '+i.value)});
    window.open('https://wa.me/5514997043457?text='+encodeURIComponent(t.join('\\n')),'_blank')}});
  var c=document.querySelector('.calc');
  if(c){var ins=c.querySelectorAll('input'),out=c.querySelector('.res b'),sm=c.querySelector('small');
    var f=function(){var e=parseFloat(ins[0].value.replace(',','.')),p=parseFloat(ins[1].value.replace(',','.'));
      if(e>0&&p>=0&&e>2*p){var d=+(e-2*p).toFixed(1);out.textContent=String(d).replace('.',',')+' mm';sm.textContent=e+' − (2 × '+p+') = '+d+' mm. Na dúvida, a equipe técnica confirma a medida com você.'}else out.textContent='—'};
    ins.forEach(function(i){i.oninput=f});f()}
})();
</script>"""


def page(slug, title, active, body):
    html = HEAD.replace("__TITLE__", title) + header(active) + "<main>\n" + body + "\n</main>\n" + FOOTER + "\n" + WA + "\n" + mmenu(active) + "\n" + COMMON_JS + "\n</body>\n</html>\n"
    html = html.replace('<a class="wa-float" href="#"', f'<a class="wa-float" href="{WAURL}" target="_blank" rel="noopener"')
    html = html.replace('<meta name="viewport"', '<meta name="robots" content="noindex,nofollow">\n<meta name="viewport"')
    open(f"site/{slug}.html", "w").write(html)


os.makedirs("site", exist_ok=True)

# ---------- Home ----------
hb = re.sub(r"<header class=\"top\">.*?</header>", header("").strip(), home_body, flags=re.S)
hb = re.search(r"<main>(.*)</main>", hb, re.S).group(1)
for a, c in [('<a class="slab" href="#">', f'<a class="slab" href="{WAURL}" target="_blank" rel="noopener">'),
             ('<a class="btn or" href="#">Orçar MU 4500', '<a class="btn or" href="mu-4500.html#orcamento">Orçar MU 4500'),
             ('<a class="btn out" href="#">Ficha técnica', '<a class="btn out" href="mu-4500.html">Ficha técnica'),
             ('<a class="btn or" href="#">Orçar MC 2000', '<a class="btn or" href="mc-2000.html#orcamento">Orçar MC 2000'),
             ('<a href="#">Conheça nossa história', '<a href="empresa.html">Conheça nossa história'),
             ('<a class="btn dk" href="#">Ver mapa de revendas', '<a class="btn dk" href="onde-comprar.html">Ver mapa de revendas'),
             ('<a class="btn ln" href="#">Quero ser revendedor', '<a class="btn ln" href="seja-revendedor.html">Quero ser revendedor')]:
    assert a in hb, a
    hb = hb.replace(a, c)
hb = hb.replace('<a href="#"><b>', '<a href="setores.html"><b>')
page("index", "Limpeza de tubos industriais", "", hb)

CTA = f"""<section class="ctaband"><div class="wrap">
  <h2 class="display">Precisa limpar<br>tubos? Fale com a fábrica.</h2>
  <div class="r"><p>Resposta da equipe técnica em horário comercial.</p><a class="btn dk big" href="{WAURL}" target="_blank" rel="noopener"><svg class="wai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>Pedir orçamento pelo WhatsApp</a></div>
</div></section>"""

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'


def form(product, dark=True):
    cls = "form" if dark else "form lt"
    opts = "".join(f"<option{' selected' if p == product else ''}>{p}</option>" for p in ["MU 4500", "MC 2000", "ME 1.5 Escareação", "ME 1.5 Polimento", "Acessórios"])
    return f"""<form class="{cls}">
  <label>Nome<input placeholder="Seu nome"></label>
  <label>Empresa<input placeholder="Razão social ou usina"></label>
  <label>WhatsApp<input placeholder="(00) 00000-0000"></label>
  <label>E-mail<input placeholder="voce@empresa.com.br"></label>
  <label>Equipamento<select>{opts}</select></label>
  <label>Tensão disponível<select><option>380 V</option><option>220 V</option><option>440 V</option></select></label>
  <label>Diâmetro interno do tubo<input placeholder="ex.: 56 mm"></label>
  <label>Comprimento do tubo<input placeholder="ex.: 6 m"></label>
  <label class="full">Detalhes<textarea placeholder="Tubo reto ou com curva, liso ou corrugado, quantidade de tubos…"></textarea></label>
  <div class="send"><button class="btn wa" type="button">Enviar pedido de orçamento</button><small>Resposta da equipe técnica pelo WhatsApp.</small></div>
</form>"""


QUESTIONS = """<ol class="ask">
  <li><b>1</b><div>Qual a medida interna do tubo?<small>Diâmetro externo menos duas vezes a parede.</small></div></li>
  <li><b>2</b><div>Qual o comprimento do tubo?<small>Define o comprimento do eixo flexível.</small></div></li>
  <li><b>3</b><div>Qual a tensão disponível no local?<small>220, 380 ou 440 V.</small></div></li>
  <li><b>4</b><div>O tubo é liso ou corrugado por dentro?<small>Corrugado pede escova; liso aceita roseta.</small></div></li>
  <li><b>5</b><div>O tubo é reto ou tem curvas?<small>Curvas pedem junta universal ou eixo flexível.</small></div></li>
</ol>"""

# ---------- Produto ----------
PRODUCTS = {
    "mu-4500": dict(
        name="MU 4500", sub="Motor para limpeza de evaporadores", img="hero-mu4500.jpg", pos="30% 60%", cut="mu4500.png",
        lead="O motor tradicional das usinas de açúcar. Alta rotação para arrancar incrustação endurecida dos tubos de evaporadores, trabalhando com roseta de aço.",
        about=["Desenvolvido para a rotina de parada de safra: o MU 4500 gira a 4.500 rpm e transmite a força do motor pelo eixo flexível até a roseta, que fresa a incrustação por dentro do tubo.",
               "É o equipamento mais usado em evaporadores de usinas sucroenergéticas e em tubulações industriais longas e retas."],
        apps=["Usinas de açúcar", "Evaporadores", "Tubulações industriais"],
        kit=[("Eixo flexível", "de série"), ("Caneta", "de série"), ("Roseta, escova e demais acessórios", "vendidos à parte")],
        note="Venda exclusiva pela matriz, em Marília/SP.",
        specs=[("Motor", "Trifásico 3 CV"), ("Tensão", "220 / 380 / 440 V — 60 Hz"), ("Rotação", "4.500 rpm"), ("Eixo flexível", "Ø 19, 25 ou 30 mm"),
               ("Alma de aço", "1/2\" e 5/8\""), ("Caneta", "19, 25 ou 30 mm"), ("Rosetas", "Aço carbono, bronze ou nylon"),
               ("Comprimento do eixo", "5, 6, 7, 8, 10 ou 12 m — outros sob consulta"), ("Acessório indicado", "Roseta de aço")],
        acc=[("roseta.png", "Roseta", "Incrustação pesada", "Recomendado"), ("escova.png", "Escova", "Limpeza leve e preventiva", "Compatível")],
        others=["mc-2000", "me-15"]),
    "mc-2000": dict(
        name="MC 2000", sub="Motor para limpeza de caldeiras", img="2.jpg", pos="30% 50%", cut="mc2000.png",
        lead="Base móvel inclusa e eixo de até 30 metros: leva a limpeza até a caldeira, sem desmontar nada. Ideal com escova de aço.",
        about=["Rotação de 2.000 rpm, pensada para a limpeza de tubos de caldeiras industriais e para a manutenção preventiva de trocadores de calor.",
               "Com eixo flexível de até 30 metros, alcança tubulações longas sem precisar mover o equipamento a cada tubo."],
        apps=["Caldeiras industriais", "Tubulações longas", "Manutenção preventiva"],
        kit=[("Eixo flexível", "de série"), ("Caneta", "de série"), ("Base móvel", "de série"), ("Roseta, escova e demais acessórios", "vendidos à parte")],
        note="Disponível na matriz, nas filiais e nas revendas autorizadas.",
        specs=[("Motor", "Trifásico 3 CV"), ("Tensão", "220 / 380 / 440 V — 60 Hz"), ("Rotação", "2.000 rpm"), ("Eixo flexível", "Ø 19, 25, 30 ou 34 mm"),
               ("Alma de aço", "3/8\", 1/2\" ou 5/8\""), ("Caneta", "19, 25, 30 mm, 1/2\", 2\" ou 3\""), ("Rosetas", "Aço carbono, bronze ou nylon"),
               ("Comprimento do eixo", "5 a 30 m — sob medida"), ("Mobilidade", "Base móvel inclusa"), ("Acessório indicado", "Escova de aço e roseta")],
        acc=[("escova.png", "Escova", "Limpeza leve e preventiva", "Recomendado"), ("roseta.png", "Roseta", "Incrustação pesada", "Compatível")],
        others=["mu-4500", "me-15"]),
    "me-15": dict(
        name="ME 1.5", sub="Esmeril com mangote", img="1.jpg", pos="40% 50%", cut="me15.png",
        lead="Um motor, duas funções. A troca da peça na ponta do eixo transforma o equipamento de escareação de pneus em polidor de metais.",
        about=["Na versão Escareação, prepara carcaças de pneus para a recapagem, limpando cortes e danos antes da aplicação da borracha nova.",
               "Na versão Polimento, faz desbaste e acabamento de ligas metálicas — de tanques e pias de inox a peças usinadas."],
        apps=["Recapagem de pneus", "Polimento de metais", "Desbaste"],
        kit=[("Eixo flexível", "de série"), ("Caneta", "de série"), ("Base móvel", "opcional"), ("Engate rápido e demais acessórios", "vendidos à parte")],
        note="Disponível na matriz, nas filiais e nas revendas autorizadas.",
        specs=[("Motor", "1,5 CV monofásico ou trifásico"), ("Tensão monofásico", "110 / 220 V — 60 Hz"), ("Tensão trifásico", "220 / 380 V — 60 Hz"),
               ("Rotação", "3.450 rpm"), ("Eixo flexível", "5/8\", 25 ou 34 mm"), ("Comprimento do eixo", "2 ou 3 m"), ("Caneta", "1/2\", 5/8\" ou 3/4\""),
               ("Disco ou lixa", "até 6\""), ("Troca de função", "Substituição da peça na ponta")],
        acc=[("engate.png", "Engate rápido", "Troca ágil de ferramentas", "Compatível")],
        others=["mu-4500", "mc-2000"]),
}


def product_page(slug):
    p = PRODUCTS[slug]
    about = "".join(f"<p>{x}</p>" for x in p["about"])
    apps = "".join(f"<span>{a}</span>" for a in p["apps"])
    kit = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in p["kit"])
    specs = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in p["specs"])
    acc = "".join(f'<a href="acessorios.html"><span class="im"><img src="img/{i}" alt=""></span><b>{n}</b><span>{d}</span><em>{r} para o {p["name"]}</em></a>' for i, n, d, r in p["acc"])
    oth = ""
    for o in p["others"]:
        q = PRODUCTS[o]
        oth += f'<a href="{o}.html"><div><b>{q["name"]}</b><span>{q["sub"]}</span></div><img src="img/{q["cut"]}" alt=""></a>'
    versions = ""
    if slug == "me-15":
        versions = """<section class="sec"><div class="wrap">
  <h2 class="display h2">Duas versões,<br><span>o mesmo motor.</span></h2>
  <div class="me" style="padding:40px 0 0"><div class="pair">
    <figure><img src="img/1.jpg" alt="Escareação de pneu"><figcaption style="border-color:var(--line)"><b>Escareação</b><span style="color:var(--steel)">Recapagem e reforma de pneus</span></figcaption></figure>
    <figure><img src="img/5.jpg" alt="Polimento de inox"><figcaption style="border-color:var(--line)"><b>Polimento</b><span style="color:var(--steel)">Desbaste e acabamento de metais</span></figcaption></figure>
  </div></div>
</div></section>"""
    body = f"""<section class="phero" style="--img:url(img/{p['img']});--pos:{p['pos']}">
  <p class="crumbs"><a href="equipamentos.html">Equipamentos</a> / {p['name']}</p>
  <div class="in">
    <h1 class="display">{p['name']}</h1>
    <p class="lead">{p['lead']}</p>
    <div class="acts"><a class="btn wa" href="#orcamento">Orçar o {p['name']}</a><a class="btn out" href="#orcamento">Pedir ficha técnica</a></div>
  </div>
  <div class="cut"></div>
</section>

<section class="sec"><div class="wrap two">
  <div><h2 class="display h2">{p['sub']}</h2><div class="apps">{apps}</div></div>
  <div class="body-l">{about}<ul class="kit" style="margin-top:36px">{kit}</ul><p class="note">{p['note']}</p></div>
</div></section>

{versions}

<section class="sec gray"><div class="wrap stage">
  <div class="art"><img src="img/{p['cut']}" alt="{p['name']}"><span class="tag">{p['name']} · Fabricado em Marília/SP</span></div>
  <div><h2 class="display h2">Ficha técnica</h2><table class="spec lt" style="margin-top:32px">{specs}</table></div>
</div></section>

<section class="sec"><div class="wrap">
  <h2 class="display h2">Acessórios para o {p['name']}</h2>
  <div class="acc">{acc}</div>
</div></section>

<section class="sec dark" id="orcamento"><div class="wrap quote">
  <div><h2 class="display h2">Orçamento certo<br><span>na primeira conversa.</span></h2>
  <p class="body-l" style="margin-top:20px">Com estas cinco respostas a equipe técnica indica o eixo, a caneta e a ferramenta certos para o seu tubo.</p>{QUESTIONS}</div>
  {form(p['name'] if slug != 'me-15' else 'ME 1.5 Escareação')}
</div></section>

<section class="sec"><div class="wrap">
  <h2 class="display h2">Outros equipamentos</h2>
  <div class="others">{oth}</div>
</div></section>"""
    page(slug, p["name"], "equipamentos", body)


for s in PRODUCTS:
    product_page(s)

# ---------- Equipamentos ----------
def eqrow(slug, rev, pos):
    p = PRODUCTS[slug]
    facts = {"mu-4500": [("Rotação", "4.500 rpm"), ("Motor", "3 CV"), ("Eixo", "até 12 m")],
             "mc-2000": [("Rotação", "2.000 rpm"), ("Motor", "3 CV"), ("Eixo", "até 30 m")],
             "me-15": [("Rotação", "3.450 rpm"), ("Motor", "1,5 CV"), ("Eixo", "2 ou 3 m")]}[slug]
    f = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in facts)
    return f"""<div class="eqrow{' rev' if rev else ''}">
  <div class="ph" style="--img:url(img/{p['img']});--pos:{pos}"></div>
  <div class="tx"><h2 class="display">{p['name']}<small>{p['sub']}</small></h2><p>{p['lead']}</p>
  <dl class="facts">{f}</dl>
  <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn dk" href="{slug}.html">Ver detalhes</a><a class="btn lt" href="{slug}.html#orcamento">Orçar</a></div></div>
</div>"""


eq = f"""<section class="phero" style="--img:url(img/2.jpg);--pos:35% 50%">
  <div class="in"><h1 class="display">Equipamentos</h1>
  <p class="lead">Três máquinas de fabricação própria para limpar tubos e preparar superfícies — do evaporador da usina à recapagem de pneus.</p></div>
  <div class="cut"></div>
</section>
<section>
{eqrow('mu-4500', False, '30% 70%')}
{eqrow('mc-2000', True, '30% 50%')}
{eqrow('me-15', False, '45% 50%')}
</section>
<section class="sec gray"><div class="wrap">
  <h2 class="display h2">Qual escolher?</h2>
  <div class="cmpwrap"><table class="cmp">
    <tr><th></th><th>MU 4500</th><th>MC 2000</th><th>ME 1.5</th></tr>
    <tr><td>Uso principal</td><td>Evaporadores de usinas</td><td>Caldeiras industriais</td><td>Pneus e metais</td></tr>
    <tr><td>Rotação</td><td>4.500 rpm</td><td>2.000 rpm</td><td>3.450 rpm</td></tr>
    <tr><td>Motor</td><td>Trifásico 3 CV</td><td>Trifásico 3 CV</td><td>1,5 CV mono ou trifásico</td></tr>
    <tr><td>Eixo flexível</td><td>5 a 12 m</td><td>5 a 30 m</td><td>2 ou 3 m</td></tr>
    <tr><td>Ferramenta</td><td>Roseta</td><td>Escova e roseta</td><td>Disco, lixa, engate rápido</td></tr>
    <tr><td>Mobilidade</td><td>Base fixa</td><td>Base móvel inclusa</td><td>Base móvel opcional</td></tr>
    <tr><td>Onde comprar</td><td>Somente matriz</td><td>Matriz e revendas</td><td>Matriz e revendas</td></tr>
  </table></div>
</div></section>
{CTA}"""
page("equipamentos", "Equipamentos", "equipamentos", eq)

# ---------- Acessórios ----------
acc = f"""<section class="phero" style="--img:url(img/3.jpg);--pos:40% 50%">
  <div class="in"><h1 class="display">Acessórios</h1>
  <p class="lead">Rosetas, escovas, eixos e canetas fabricados para trabalhar com os nossos motores. Reposição na matriz e em todas as revendas autorizadas.</p></div>
  <div class="cut"></div>
</section>
<section><div class="wrap">
  <div class="accrow"><div class="im"><img src="img/roseta.png" alt="Roseta"></div><div>
    <h2 class="display">Roseta</h2><p>Fresa a incrustação endurecida por dentro do tubo. É a ferramenta de limpeza pesada de evaporadores e caldeiras.</p>
    <table class="spec lt"><tr><td>Materiais</td><td>Aço carbono, bronze ou nylon</td></tr><tr><td>Medidas</td><td>Conforme o diâmetro interno do tubo</td></tr><tr><td>Usar com</td><td>MU 4500 (recomendado) · MC 2000</td></tr></table></div></div>
  <div class="accrow"><div class="im"><img src="img/escova.png" alt="Escova"></div><div>
    <h2 class="display">Escova</h2><p>Remove oxidação e depósitos leves. Indicada para manutenção preventiva e para tubos corrugados por dentro.</p>
    <table class="spec lt"><tr><td>Materiais</td><td>Aço ou bronze</td></tr><tr><td>Aplicação</td><td>Limpeza interna leve de tubulações</td></tr><tr><td>Usar com</td><td>MC 2000 (recomendado) · MU 4500</td></tr></table></div></div>
  <div class="accrow"><div class="im"><img src="img/engate.png" alt="Engate rápido"></div><div>
    <h2 class="display">Engate rápido</h2><p>Conecta o carbide à caneta e permite trocar a ferramenta no eixo flexível sem interromper o trabalho.</p>
    <table class="spec lt"><tr><td>Material</td><td>Aço</td></tr><tr><td>Medidas</td><td>1/2" e 5/8"</td></tr><tr><td>Usar com</td><td>ME 1.5</td></tr></table></div></div>
</div></section>
<section class="sec gray"><div class="wrap">
  <h2 class="display h2">Peças de reposição</h2>
  <div class="mini">
    <div><b>Eixo flexível</b><p>Transmite a rotação do motor até a ferramenta. Vários diâmetros e comprimentos.</p></div>
    <div><b>Caneta</b><p>Peça da ponta que segura a ferramenta. Compatível com escovas e rosetas.</p></div>
    <div><b>Alma de aço</b><p>Núcleo do eixo flexível, responsável pelo torque e pela durabilidade.</p></div>
    <div><b>Carrinho</b><p>Base com rodas para deslocar o equipamento durante a limpeza.</p></div>
  </div>
</div></section>
<section class="sec dark"><div class="wrap">
  <h2 class="display h2">Qual acessório <span>em qual motor?</span></h2>
  <table class="cmptab">
    <tr><th>Acessório</th><th>MU 4500</th><th>MC 2000</th><th>ME 1.5</th></tr>
    <tr><td>Roseta · aço, bronze, nylon</td><td class="rec">Recomendado</td><td>Compatível</td><td class="no">—</td></tr>
    <tr><td>Escova · aço, bronze</td><td>Compatível</td><td class="rec">Recomendado</td><td class="no">—</td></tr>
    <tr><td>Engate rápido · 1/2" e 5/8"</td><td class="no">—</td><td class="no">—</td><td class="rec">Compatível</td></tr>
  </table>
</div></section>
<section class="sec"><div class="wrap measure">
  <div><h2 class="display h2">Como medir<br><span>o seu tubo</span></h2>
  <div class="body-l" style="margin-top:24px"><p>A roseta é escolhida pelo diâmetro <b>interno</b> do tubo e precisa de cerca de 1 mm de folga para trabalhar.</p><p>Meça o diâmetro externo e a espessura da parede. O interno é o externo menos duas vezes a parede.</p></div></div>
  <div class="calc">
    <div class="row"><label>Diâmetro externo (mm)<input value="60"></label><label>Parede (mm)<input value="2"></label></div>
    <div class="res"><span>Diâmetro interno</span><b>56 mm</b></div>
    <a class="btn wa" style="margin-top:16px" href="contato.html">Enviar medida para orçamento</a>
    <small>60 − (2 × 2) = 56 mm. Na dúvida, a equipe técnica confirma a medida com você.</small>
  </div>
</div></section>
{CTA}"""
page("acessorios", "Acessórios", "acessorios", acc)

# ---------- Setores ----------
def srow(name, text, uses, img, pos, rev):
    return f"""<div class="srow{' rev' if rev else ''}"><div class="ph" style="--img:url(img/{img});--pos:{pos}"></div>
<div class="tx"><h2 class="display">{name}</h2><p>{text}</p><p class="uses">Equipamento indicado: <span>{uses}</span></p></div></div>"""


st = f"""<section class="phero plain">
  <div class="in"><h1 class="display">Setores que<br><span>atendemos</span></h1>
  <p class="lead">Onde há tubo para limpar ou superfície para preparar, há uma máquina Marques da Costa trabalhando.</p></div>
  <div class="cut"></div>
</section>
<section>
{srow('Sucroenergético', 'Limpeza de tubos de evaporadores em usinas de açúcar e etanol e em destilarias — a origem da empresa, em 1964.', 'MU 4500 com roseta', 'hero-mu4500.jpg', '70% 50%', False)}
{srow('Caldeiras industriais', 'Manutenção e limpeza de tubos de caldeiras a vapor e de geração de energia, conforme a rotina de inspeção da NR-13.', 'MC 2000 com escova ou roseta', '2.jpg', '30% 50%', True)}
{srow('Borracha e pneus', 'Escareação de carcaças em recapagem e reforma de pneus: limpeza de cortes e danos antes da borracha nova.', 'ME 1.5 Escareação', '1.jpg', '55% 50%', False)}
{srow('Metalurgia', 'Polimento e desbaste de ligas metálicas para acabamento industrial — inox, tanques, peças usinadas.', 'ME 1.5 Polimento', '5.jpg', '60% 50%', True)}
</section>
<section class="sec dark"><div class="wrap">
  <h2 class="display h2">E também</h2>
  <div class="slist">
    <div><b>Alimentício</b><p>Limpeza de equipamentos de processamento e secagem: secadores de grãos, amendoim e café.</p><em>MC 2000</em></div>
    <div><b>Papel e celulose</b><p>Manutenção de tubulações de processo e caldeiras industriais.</p><em>MC 2000 · MU 4500</em></div>
    <div><b>Petroquímico</b><p>Limpeza especializada de tubulações em refinarias e plantas industriais.</p><em>MC 2000 · MU 4500</em></div>
    <div><b>Outros setores</b><p>Soluções adaptáveis a qualquer indústria que precise de limpeza mecanizada de tubos.</p><em>Consulte a equipe técnica</em></div>
  </div>
</div></section>
{CTA}"""
page("setores", "Setores", "setores", st)

# ---------- Onde comprar ----------
mp = json.load(open("map.json"))
paths = "".join(f'<path d="{d}"/>' for _, d in mp["paths"])
pins = ""
for x, y, n, kind in mp["pins"]:
    if kind is True or kind == "1" or n == "Matriz":
        pins += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#0F0F10" stroke="#F15A22" stroke-width="4"/>'
    elif kind == "f":
        pins += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#0F0F10"/>'
    else:
        pins += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#F15A22" stroke="#fff" stroke-width="2"/>'
svg = ""
STORES = [
    ("Matriz Marques da Costa", "Marília · SP", "Av. Eugênio Coneglian, 2586 · (14) 3425-2533", True),
    ("Filial Pontal", "Pontal · SP", "Rua Rui Barbosa, 488 · (16) 3953-1544", False),
    ("Filial Nordeste", "Recife · PE", "Rua Itacari, 369 · (81) 3471-3275", False),
    ("Casa da Caldeira", "Paiçandu · PR", "(44) 3244-1734 · (44) 99907-0808", False),
    ("Comax Ferramentas", "Guarulhos · SP", "Rua Alto do Rio Doce, 66", False),
    ("Norte Sul Equipamentos", "São Paulo · SP", "Rua Dias da Silva, 512", False),
    ("Fabio Pelicer Máquinas", "São José do Rio Preto · SP", "Rua Silvio Pelicer Filho, 500", False),
    ("Gebor Comercial", "Contagem · MG", "Av. Tomaz Gonzaga, 422", False),
    ("Gebor Importação e Exportação", "Serra · ES", "Rua Pedro Zangrande, 405", False),
    ("Loop Industrial", "Bento Gonçalves · RS", "Rua Augusto Geisel, 465", False),
    ("Máquinas PLC", "São José do Rio Preto · SP", "Estrada Silvio Pelicer Filho, 500A", False),
    ("Palhinha Solda e Corte", "Ribeirão Preto · SP", "Rua Ceará, 972", False),
    ("Pré-Forte Máquinas", "São Paulo · SP", "Rua Valdemar Martins, 828 · (11) 3926-0800", False),
    ("Sabrafer Soluções", "Guarulhos · SP", "Av. João Veloso Silva, 521 · (11) 2085-2862", False),
    ("Tecnobor", "Itajaí · SC", "Av. Governador Adolfo Konder, 705", False),
    ("Tecnobor", "São Paulo · SP", "Rua Antonio Fonseca, 523", False),
]
from urllib.parse import quote
sl = "".join(f'<div class="store{" mx" if m else ""}" data-uf="{c[-2:]}" data-q="{(n+" "+c).lower()}"><b>{n}</b><span class="c">{c}</span><span class="t">{t}</span><a class="r" href="{MAPS}{quote(t.split(" · ")[0]+", "+c.replace(" · ", " "))}" target="_blank" rel="noopener">Como chegar</a></div>' for n, c, t, m in STORES)
oc = f"""<section class="phero plain">
  <div class="in"><h1 class="display">Onde<br><span>comprar</span></h1>
  <p class="lead">Matriz em Marília, filiais em Recife e Pontal e 13 revendas autorizadas com acessórios e reposição.</p></div>
  <div class="cut"></div>
</section>
<section class="sec"><div class="wrap finder">
  <div>
    <h2 class="display h2" style="font-size:72px">Encontre a revenda mais próxima</h2>
    <div class="search"><input placeholder="Digite sua cidade ou estado"><button type="button">Buscar</button></div>
    <div class="filters"><span class="on">Todos</span><span>SP</span><span>PR</span><span>SC</span><span>RS</span><span>MG</span><span>ES</span><span>PE</span></div>
    <div class="stores">{sl}</div>
  </div>
  <div class="mapbox"><div id="map"></div><div class="legend"><span><i style="background:#0F0F10;border:3px solid #F15A22"></i>Matriz</span><span><i style="background:#0F0F10"></i>Filiais</span><span><i style="background:#F15A22"></i>Revendas</span></div></div>
</div></section>
<link rel="stylesheet" href="vendor/leaflet.css">
<script src="vendor/leaflet.js"></script><script src="vendor/br-uf.js"></script><script src="vendor/revendas.js"></script>
<script>
const map=L.map('map',{{zoomControl:true,scrollWheelZoom:false}});
L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png',{{attribution:'&copy; OpenStreetMap &copy; CARTO',subdomains:'abcd',maxZoom:19}}).addTo(map);
const ufLayer=L.geoJSON(BR_UF);
const ic=t=>L.divIcon({{className:'pin pin-'+t,iconSize:t==='matriz'?[26,26]:[18,18]}});
let matriz;
REVENDAS.forEach(r=>{{const m=L.marker([r.lat,r.lng],{{icon:ic(r.tipo)}}).addTo(map).bindPopup('<b>'+r.nome+'</b><br>'+r.cidade+'<br><a target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination='+r.lat+','+r.lng+'">Como chegar</a>');if(r.tipo==='matriz')matriz=m;}});
map.fitBounds(ufLayer.getBounds(),{{padding:[12,12]}});
matriz.openPopup();
const ss=[...document.querySelectorAll('.store')],inp=document.querySelector('.search input'),chips=[...document.querySelectorAll('.filters span')];let uf='Todos';
const ap=()=>{{const q=inp.value.trim().toLowerCase();ss.forEach(s=>{{s.hidden=!((uf==='Todos'||s.dataset.uf===uf)&&(!q||s.dataset.q.includes(q)||s.textContent.toLowerCase().includes(q)))}})}};
chips.forEach(c=>c.onclick=()=>{{chips.forEach(x=>x.classList.remove('on'));c.classList.add('on');uf=c.textContent;ap()}});
inp.oninput=ap;document.querySelector('.search button').onclick=ap;
</script>
<section class="ctaband"><div class="wrap">
  <h2 class="display">Quer revender<br>Marques da Costa?</h2>
  <div class="r"><p>Condições para revendas e distribuidores.</p><a class="btn dk big" href="seja-revendedor.html">Cadastrar minha empresa</a></div>
</div></section>"""
page("onde-comprar", "Onde comprar", "onde-comprar", oc)

# ---------- Seja revendedor ----------
sr = f"""<section class="phero" style="--img:url(img/hero-mu4500.jpg);--pos:20% 70%">
  <p class="crumbs"><a href="onde-comprar.html">Onde comprar</a> / Seja um revendedor</p>
  <div class="in"><h1 class="display">Revenda o que<br><span>a indústria já usa.</span></h1>
  <p class="lead">Máquinas e acessórios com demanda contínua em paradas de safra e manutenções preventivas, com 62 anos de marca por trás.</p>
  <div class="acts"><a class="btn wa" href="#cadastro">Quero ser revendedor</a></div></div>
  <div class="cut"></div>
</section>
<section class="sec"><div class="wrap">
  <h2 class="display h2">Por que representar<br><span>a Marques da Costa</span></h2>
  <div class="benef">
    <div><b>Margem atraente</b><p>Condições comerciais para revendas e distribuidores, com recompra constante de rosetas, escovas e eixos.</p></div>
    <div><b>Conformidade NR-12</b><p>Equipamentos desenvolvidos conforme as normas de segurança industrial.</p></div>
    <div><b>Suporte de fábrica</b><p>Treinamento, peças de reposição a pronta entrega e apoio direto da engenharia.</p></div>
    <div><b>Várias aplicações</b><p>Caldeiras fogotubulares, evaporadores, condensadores, recapagem e metalurgia.</p></div>
    <div><b>Material de venda</b><p>Catálogo digital e impresso, fichas técnicas e oportunidades da sua região encaminhadas para você.</p></div>
    <div><b>Marca reconhecida</b><p>Mais de 60 anos de presença em usinas e plantas industriais de todo o Brasil.</p></div>
  </div>
</div></section>
<section class="sec dark"><div class="wrap testi">
  <span class="q" aria-hidden="true">“</span>
  <div><blockquote>Indico a utilização da máquina para limpeza dos tubos fogotubulares: facilita o serviço e aumenta a qualidade da limpeza, dando maior rendimento para a caldeira.</blockquote>
  <cite><b>Lucas Kreutz</b> · Engenheiro mecânico e inspetor de caldeiras</cite></div>
</div></section>
<section class="sec gray" id="cadastro"><div class="wrap two">
  <div><h2 class="display h2">Cadastre<br>sua empresa</h2><p class="body-l" style="margin-top:20px">A diretoria comercial analisa o perfil da sua região e entra em contato para apresentar a política de distribuição.</p></div>
  <form class="form lt">
    <label>Nome<input placeholder="Seu nome"></label>
    <label>Razão social<input placeholder="Nome da empresa"></label>
    <label>E-mail<input placeholder="voce@empresa.com.br"></label>
    <label>WhatsApp<input placeholder="(00) 00000-0000"></label>
    <label class="full">Região ou estados de atuação<input placeholder="ex.: interior de Goiás e Triângulo Mineiro"></label>
    <label class="full">Conte sobre a sua empresa<textarea placeholder="Segmento, clientes atendidos, linhas que já revende…"></textarea></label>
    <div class="send"><button class="btn dk" type="button">Enviar cadastro</button><small>Retorno da diretoria comercial.</small></div>
  </form>
</div></section>"""
page("seja-revendedor", "Seja um revendedor", "onde-comprar", sr)

# ---------- Empresa ----------
UNITS = """<div class="units">
  <div><b>Matriz</b><p>Av. Eugênio Coneglian, 2586 · Distrito Industrial<br>Marília/SP · CEP 17512-050<br>(14) 3425-2533 · (14) 3425-2544</p><a href="https://www.google.com/maps/search/?api=1&query=Av.%20Eug%C3%AAnio%20Coneglian%2C%202586%2C%20Mar%C3%ADlia%20SP" target="_blank" rel="noopener">Como chegar</a></div>
  <div><b>Filial Nordeste</b><p>Rua Itacari, 369 · Imbiribeira<br>Recife/PE · CEP 51200-080<br>(81) 3471-3275 · (81) 99600-9479</p><a href="https://www.google.com/maps/search/?api=1&query=Rua%20Itacari%2C%20369%2C%20Recife%20PE" target="_blank" rel="noopener">Como chegar</a></div>
  <div><b>Filial Pontal</b><p>Rua Rui Barbosa, 488 · Vila Adelaide de Freitas<br>Pontal/SP · CEP 14180-000<br>(16) 3953-1544 · (16) 98129-8719</p><a href="https://www.google.com/maps/search/?api=1&query=Rua%20Rui%20Barbosa%2C%20488%2C%20Pontal%20SP" target="_blank" rel="noopener">Como chegar</a></div>
</div>"""
em = f"""<section class="phero" style="--img:url(img/fachada.jpg);--pos:50% 70%">
  <div class="in"><h1 class="display">Três gerações.<br><span>Mesma fábrica.</span></h1>
  <p class="lead">Empresa familiar de Marília/SP, fabricando equipamentos de limpeza industrial desde 1964.</p></div>
  <div class="cut"></div>
</section>
<section class="sec"><div class="wrap story">
  <div class="big">1964<small>Marília · SP</small></div>
  <div class="body-l"><p>Em 1964, Heráclito Marques da Costa e o filho Antônio viram um problema nas usinas de açúcar: a limpeza dos tubos dos evaporadores era feita à mão, levava dias e exigia muito esforço.</p>
  <p>A resposta foi uma máquina. O motor com eixo flexível mecanizou a limpeza e deu origem à Indústrias Marques da Costa.</p>
  <p>A empresa passou de geração em geração mantendo o mesmo compromisso com qualidade e inovação, e ampliou o portfólio para caldeiras, indústria alimentícia, papel e celulose, petroquímica, recapagem e metalurgia.</p></div>
</div>
<div class="wrap"><div class="then">
  <div><b>Começo</b><p>Uma oficina em Marília e uma ideia para o setor açucareiro: trocar a limpeza manual dos evaporadores por uma máquina.</p></div>
  <div><b>Hoje</b><p>Matriz e fábrica em Marília, filiais em Recife e Pontal, 13 revendas autorizadas e clientes em oito setores da indústria.</p></div>
</div></div></section>
<section class="historia" style="height:680px"><div class="copy"><h2 class="display">Uma marca<br>fundamental<br>para o trabalho.</h2><div></div></div></section>
<section class="sec dark"><div class="wrap">
  <h2 class="display h2">O que nos move</h2>
  <div class="mvv">
    <div><b>Missão</b><p>Desenvolver produtos que facilitem o trabalho das empresas e das pessoas no dia a dia, fidelizando clientes e tornando a Marques da Costa uma marca fundamental para a indústria.</p></div>
    <div><b>Visão</b><p>Ser reconhecida pela criação de produtos e acessórios de alta qualidade, que permitam às empresas trabalhar com mais economia, rapidez e segurança.</p></div>
    <div><b>Valores</b><ul><li>Segurança</li><li>Comprometimento</li><li>Qualidade</li><li>Foco no cliente</li><li>Respeito</li><li>Inovação</li></ul></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <h2 class="display h2">Nossas unidades</h2>
  {UNITS}
</div></section>"""
page("empresa", "Empresa", "empresa", em)

# ---------- Contato ----------
ct = f"""<section class="phero plain">
  <div class="in"><h1 class="display">Fale com<br><span>a fábrica</span></h1>
  <p class="lead">Orçamentos, dúvidas técnicas e assistência. A equipe responde pelo WhatsApp em horário comercial.</p></div>
  <div class="cut"></div>
</section>
<section class="sec"><div class="wrap">
  <div class="chan">
    <div><dt>WhatsApp comercial</dt><dd>Orçamentos e dúvidas<small><a class="btn wa" style="margin-top:14px" href="{WAURL}" target="_blank" rel="noopener"><svg class="wai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>Iniciar conversa</a><span style="display:block;margin-top:10px;color:var(--steel)">+55 14 99704-3457</span></small></dd></div>
    <div><dt>Central de atendimento</dt><dd>(14) 3425-2533<small>(14) 3425-2544 · segunda a sexta</small></dd></div>
    <div><dt>E-mail</dt><dd style="font-size:32px">vendas@<br>marquesdacosta.com.br<small>Projetos especiais: projeto@marquesdacosta.com.br</small></dd></div>
  </div>
</div></section>
<section class="sec dark" id="orcamento"><div class="wrap quote">
  <div><h2 class="display h2">Pedido de<br><span>orçamento</span></h2>
  <p class="body-l" style="margin-top:20px">Quanto mais informação sobre o tubo, mais rápido e certo vem o orçamento.</p>{QUESTIONS}</div>
  {form('MU 4500')}
</div></section>
<section class="sec"><div class="wrap">
  <h2 class="display h2">Visite uma unidade</h2>
  {UNITS}
</div></section>"""
page("contato", "Contato", "contato", ct)

# ---------- Menu mobile ----------
mm = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Menu</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900&display=swap" rel="stylesheet"><link rel="stylesheet" href="base.css"></head><body>
<div class="mmenu"><div class="hd"><img src="img/logo_branca.png" alt="Marques da Costa"><span class="x" aria-label="Fechar">×</span></div>
<nav><a class="on" href="#">Início</a><a href="#">Equipamentos</a><a href="#">Acessórios</a><a href="#">Setores</a><a href="#">Onde comprar</a><a href="#">Empresa</a><a href="#">Contato</a></nav>
<div class="ft"><a class="btn wa" href="#">Pedir orçamento pelo WhatsApp</a><p>+55 14 99704-3457 · (14) 3425-2533<br>vendas@marquesdacosta.com.br</p></div></div>
</body></html>"""
open("site/menu-mobile.html", "w").write(mm)
print("ok")
