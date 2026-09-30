"""Build the multi-page web report (OE brand, Italian) for GitHub Pages and the Claude artifact.

Run from any directory:  python web/build_site.py
Inputs: web/src/* (content blocks, shared CSS/JS), analysis/output commuting table, the municipal
dataset, and the OpenEconomics front-end brand kit zip (design-system CSS and logos).
Outputs: index.html + one page per topic at the repository root (served by GitHub Pages),
assets/ (shared CSS, JS, logos) and web/artifact_home.html (entry page for the Claude artifact).
"""
from pathlib import Path
import json
import os
import re
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'web' / 'src'
ASSETS = ROOT / 'assets'
BRAND_ZIP = Path(os.environ.get('OE_BRAND_ZIP', Path.home() / 'OneDrive - OpenEconomics S.r.l' / 'Desktop' / 'oe-frontend-brand_20260711_0029-v6.zip'))

# ---------------------------------------------------------------- shared assets
z = zipfile.ZipFile(BRAND_ZIP)
rd = lambda p: z.read('oe-frontend-brand/' + p).decode('utf-8')
ASSETS.mkdir(exist_ok=True)
tokens = re.sub(r'@font-face\s*\{[^}]*\}', '', rd('ds-kit/colors_and_type.css'))   # fonts from Google Fonts
css = ('/* OpenEconomics DS v4.0: colors_and_type.css */\n' + tokens + '\n/* OpenEconomics DS v4.0: components.css */\n'
       + rd('ds-kit/components.css') + '\n' + (SRC / 'site_layer.css').read_text(encoding='utf-8')
       + '\n' + (SRC / 'site_extra.css').read_text(encoding='utf-8'))
(ASSETS / 'site.css').write_text(css, encoding='utf-8')
for name in ['logo-black.svg', 'logo-white.svg']:
    (ASSETS / name).write_text(rd('ds-kit/components/' + name), encoding='utf-8')

m = pd.read_csv(ROOT / 'analysis/output/commuting_municipal_2021.csv', dtype={'pro_com_t': str})
d = pd.read_csv(ROOT / 'New_Query_2026_09_30_10_19_18.csv', dtype={'pro_com_t': str})[['pro_com_t', 'latitude', 'longitude']]
m = m.merge(d, on='pro_com_t', validate='one_to_one')
muni = [[r.comune, round(r.latitude, 4), round(r.longitude, 4), int(r.popolazione_2025), round(r.variazione_pct_popolazione_2021_2025, 1),
         round(100 * r.share_rome_province), int(r.car_minutes_to_rome_city)] for r in m.itertuples()]
js = (SRC / 'site.js').read_text(encoding='utf-8').replace('{{MUNI}}', json.dumps(muni, ensure_ascii=False, separators=(',', ':')))
(ASSETS / 'site.js').write_text(js, encoding='utf-8')

# ---------------------------------------------------------------- content blocks
BLOCKS = (SRC / 'blocks.html').read_text(encoding='utf-8')

def _match_div(s, start):
    depth, i = 0, start
    for t in re.finditer(r'<div\b|</div>', s[start:]):
        depth += 1 if t.group() != '</div>' else -1
        if depth == 0:
            return start + t.end()
    raise ValueError('unbalanced div')

def block(marker, starts=('<div class="fig">', '<div class="tbl', '<div class="callout">', '<div class="prio', '<div class="claims">')):
    """Smallest known block (figure, table, callout...) in blocks.html that contains `marker`."""
    pos = BLOCKS.index(marker)
    best = None
    for st in starts:
        for mt in re.finditer(re.escape(st), BLOCKS):
            if mt.start() > pos:
                break
            end = _match_div(BLOCKS, mt.start())
            if end > pos and (best is None or mt.start() > best[0]):
                best = (mt.start(), end)
    out = BLOCKS[best[0]:best[1]]
    after = BLOCKS[best[1]:best[1] + 600].lstrip()
    if out.startswith('<div class="tbl') and after.startswith('<p class="source">'):
        out += '\n' + after[:after.index('</p>') + 4]
    return out

def renumber(html):
    n = {'Grafico': 0, 'Mappa': 0, 'Tabella': 0}
    def rep(mt):
        n[mt.group(1)] += 1
        return f'{mt.group(1)} {n[mt.group(1)]}'
    return re.sub(r'\b(Grafico|Mappa|Tabella) \d+\b', rep, html)

two = lambda a, b: f'<div class="two">\n{a}\n{b}\n</div>'
ARROW = '<svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
CHECK = '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>'
ICONS = {
    'persone': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'lavoro': '<rect x="4" y="3" width="16" height="16"/><path d="M4 11h16"/><path d="M12 3v8"/><path d="m8 19-2 3"/><path d="m18 22-2-3"/>',
    'imprese': '<path d="M2 20h20"/><path d="M4 20V9l6 4V9l6 4V4h4v16"/>',
    'giovani': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    'energia': '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    'europa': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    'proposte': '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>',
}
icon = lambda k: f'<svg viewBox="0 0 24 24">{ICONS[k]}</svg>'

# ---------------------------------------------------------------- pages
PAGES = [  # key, file, nav label, card title
    ('home', 'index.html', 'Home', 'Home'),
    ('persone', 'persone.html', 'Persone', 'Persone e territorio'),
    ('lavoro', 'lavoro.html', 'Lavoro', 'Lavoro e spostamenti'),
    ('imprese', 'imprese.html', 'Imprese', 'Imprese ed export'),
    ('giovani', 'giovani.html', 'Giovani', 'Giovani e competenze'),
    ('energia', 'energia.html', 'Energia', 'Energia'),
    ('europa', 'europa.html', 'Europa 2028–34', 'Europa 2028–2034'),
    ('proposte', 'proposte.html', 'Proposte', 'Le proposte'),
]
FILE = {k: f for k, f, *_ in PAGES}
TITLE = {k: t for k, _, _, t in PAGES}
TOPICS = [k for k, *_ in PAGES if k != 'home']

TOPIC = {
 'persone': dict(
    h1='La popolazione cala poco, ma i territori si allontanano tra loro',
    brief=['La provincia ha perso <strong>l\'1% dei residenti</strong> dal 2021, meno di diverse province vicine.',
           'Crescono solo i comuni della Sabina vicini a Roma; <strong>il capoluogo e la montagna perdono abitanti</strong>.',
           'Si perde popolazione soprattutto perché le nascite sono molte meno dei decessi, non perché le persone partono.'],
    why='Servono politiche diverse per la Sabina, per il capoluogo e per i piccoli comuni montani, non una ricetta unica.',
    sections=[('mappa', 'La mappa', 'Dove si cresce e dove si cala', block('id="mapPop"')),
              ('distanza', 'Distanza da Roma', 'Più ci si allontana da Roma, più la popolazione cala e invecchia',
               two(block('id="chBands"'), block('Rieti e le province di confronto'))),
              ('bilancio', 'Nascite e arrivi', 'La popolazione cala per l\'invecchiamento più che per le partenze', block('Perché si perde popolazione'))],
    todo=['Lavoro raggiungibile e famiglie che restano', 'Servizi essenziali nei piccoli comuni']),
 'lavoro': dict(
    h1='Un pendolare su quattro lavora nella provincia di Roma',
    brief=['Ogni giorno <strong>14.449 residenti</strong> escono dalla provincia per lavorare e solo 5.090 persone vi entrano.',
           'Nella Sabina quasi <strong>la metà dei lavoratori</strong> va verso Roma, con viaggi di oltre un\'ora.',
           'Il polo industriale Rieti–Cittaducale <strong>non ha creato posti di lavoro in dieci anni</strong>; salari e occupazione femminile restano bassi.'],
    why='Il lavoro qualificato va portato più vicino a chi vive qui; trasporti, orari e servizi per le famiglie contano quanto gli investimenti.',
    sections=[('roma', 'Verso Roma', 'Più si è vicini a Roma, più il lavoro si sposta lì', block('id="mapRome"')),
              ('destinazioni', 'Dove si lavora', 'Il lavoro locale arretra dal 2011', two(block('id="chCommute"'), block('Come sono cambiati gli spostamenti'))),
              ('viaggio', 'Il viaggio', 'Spostamenti lunghi e all\'alba', block('Come ci si sposta verso Roma')),
              ('occupazione', 'Occupazione e salari', 'Il lavoro locale paga poco e coinvolge meno persone', block('id="chEmp"'))],
    todo=['Lavoro raggiungibile e famiglie che restano', 'Una rete di imprese e fornitori']),
 'imprese': dict(
    h1='L\'export corre, ma poggia su poche imprese',
    brief=['Nel 2025 l\'export cresce del <strong>48,5%</strong>, ma tutto l\'aumento viene dalla farmaceutica; il resto cala del 6%.',
           'La farmaceutica è di fatto <strong>un solo stabilimento</strong>, con circa l\'1,3% degli occupati della provincia.',
           'La "Pump Valley" delle pompe dosatrici è radicata ed esporta, ma <strong>non ha una rete comune</strong>.'],
    why='Bisogna allargare le ricadute locali dell\'industria, con fornitori, manutenzione e formazione, e ridurre la dipendenza da un solo stabilimento.',
    sections=[('export', 'Export e valore', 'La crescita dell\'export non si traduce in valore diffuso', two(block('id="chExp"'), block('id="chVa"'))),
              ('poli', 'Poli produttivi', 'Specializzazioni reali, ma piccole in termini di occupazione', block('I principali poli produttivi'))],
    todo=['Una rete di imprese e fornitori', 'Una filiera formativa tecnica completa']),
 'giovani': dict(
    h1='I giovani studiano, partono e non tornano',
    brief=['Rieti perde giovani laureati <strong>più di ogni altra provincia del Centro-Nord</strong>.',
           'La scuola è solida: il problema è che solo <strong>il 12%</strong> degli universitari reatini studia in provincia, e pochi rientrano.',
           'Le imprese non trovano profili tecnici in chimica e meccanica, ma in provincia <strong>non esiste un corso post-diploma</strong> in questi campi.'],
    why='Uno o due corsi tecnici superiori a Rieti, ruoli per laureati nelle imprese e percorsi di rientro possono invertire la tendenza.',
    sections=[('laureati', 'Laureati', 'La perdita di giovani laureati è la peggiore del Centro-Nord', block('id="chGrad"') + '\n' + block('Istruzione e giovani: Rieti e i confronti')),
              ('domanda', 'Domanda delle imprese', 'I profili più difficili da trovare sono quelli delle specializzazioni locali', block('id="chProfiles"')),
              ('offerta', 'Offerta formativa', 'La scuola forma la base giusta, ma manca il gradino dopo il diploma',
               '<p class="txt">L\'IIS Rosatelli di Rieti ha circa 180 studenti negli indirizzi di chimica e biotecnologie e circa 350 in meccanica, meccatronica, elettronica e automazione; l\'IIS Aldo Moro di Fara in Sabina circa 380 in elettronica e telecomunicazioni. In provincia gli unici corsi ITS Academy, la formazione tecnica superiore dopo il diploma, sono di logistica e agroalimentare: quelli laziali di farmaceutica e meccatronica operano a Roma, Pomezia, Frosinone e Latina. L\'università a Rieti cresce (1.331 iscritti, erano 767 cinque anni fa) ma riguarda ingegneria edile e professioni sanitarie.</p>\n' + block('La formazione specialistica è giustificata'))],
    todo=['Una filiera formativa tecnica completa', 'Trattenere e far rientrare i laureati']),
 'energia': dict(
    h1='Quasi tutta l\'elettricità prodotta qui è rinnovabile',
    brief=['Il <strong>97,5%</strong> dell\'elettricità prodotta in provincia viene da fonti rinnovabili, soprattutto idroelettriche.',
           'Il fotovoltaico cresce ma resta <strong>molto sotto le province vicine</strong>.',
           'C\'è spazio sui tetti delle aree industriali, logistiche e pubbliche, da verificare sito per sito.'],
    why='L\'energia pulita può diventare un vantaggio per le imprese: si parte da audit sui siti con consumi elevati, prima di fissare obiettivi.',
    sections=[('produzione', 'Produzione', 'Una base rinnovabile già forte, un fotovoltaico ancora basso', two(block('id="chEnergy"'), block('id="chPv"'))),
              ('siti', 'Siti produttivi', 'Partire dai siti con consumi elevati',
               '<p class="txt">La priorità è partire dai siti con consumi elevati e verificati, come le aree produttive e logistiche di Cittaducale e Fara in Sabina: efficienza, calore di processo, fotovoltaico sui tetti e connessione alla rete, prima di fissare obiettivi in megawatt.</p>')],
    todo=['Energia sui siti produttivi']),
 'europa': dict(
    h1='Il prossimo bilancio europeo premierà chi arriva con progetti pronti',
    brief=['Dal 2028 ogni Paese avrà <strong>un unico piano</strong> per i fondi europei, con pagamenti legati a risultati misurabili.',
           'Tra gli obiettivi ci sono <strong>competenze, lavoro di qualità e cambiamento demografico</strong>: i problemi principali di Rieti.',
           'Il Lazio è una regione "più sviluppata" per la media di Roma: <strong>il divario di Rieti non si vede</strong> senza dati provinciali.'],
    why='Le decisioni si prendono tra fine 2026 e il 2027: è il momento di portare evidenze e progetti al tavolo regionale.',
    sections=[('quadro', 'La proposta', 'Cosa cambia con il bilancio 2028–2034', (SRC / 'europa_body.html').read_text(encoding='utf-8'))],
    todo=['Una filiera formativa tecnica completa', 'Trattenere e far rientrare i laureati', 'Energia sui siti produttivi']),
 'proposte': dict(
    h1='Tre priorità per trattenere i talenti, quattro interventi per sostenerle',
    brief=['<strong>Una filiera formativa tecnica completa</strong>, con corsi ITS a Rieti legati alle imprese locali.',
           '<strong>Trattenere e far rientrare i laureati</strong>, con tirocini retribuiti e ruoli qualificati.',
           '<strong>Una rete di imprese e fornitori</strong> intorno alla farmaceutica e alla Pump Valley.'],
    why='Le infrastrutture restano necessarie, ma queste leve sono più mirate, costano meno e rispondono direttamente ai dati.',
    sections=[('priorita', 'Priorità', 'Le tre priorità', block('<div class="prio prio--3">', starts=('<div class="prio',))),
              ('supporto', 'Interventi di supporto', 'Quattro interventi che creano le condizioni', block('Lavoro raggiungibile e famiglie che restano</p>', starts=('<div class="prio">',))),
              ('verifica', 'Verifica', 'Cinque convinzioni diffuse, messe alla prova dai dati', block('<div class="claims__head">', starts=('<div class="claims">',)))],
    todo=[]),
}
TOPIC['proposte']['sections'] = [(i, l, h, b.replace('2.1 e 2.3: profili introvabili', 'Giovani e competenze: profili introvabili')
                                  .replace('1.1 e 1.4: perdita di laureati', 'Giovani e lavoro: perdita di laureati')
                                  .replace('2.2: specializzazioni concentrate', 'Imprese: specializzazioni concentrate'))
                                 for i, l, h, b in TOPIC['proposte']['sections']]

CARDS = {
    'persone': ('−1,0', '%', 'Residenti dal 2021', 'Crescono solo i comuni vicini a Roma: il capoluogo e la montagna perdono abitanti.'),
    'lavoro': ('1 su 4', '', 'Pendolari che lavorano nella provincia di Roma', 'Ogni giorno 11.934 residenti vanno verso Roma; il polo industriale locale non cresce.'),
    'imprese': ('80', '%', 'Export dalla farmaceutica, 2025', 'L\'export cresce ma dipende da un solo stabilimento; le altre esportazioni calano.'),
    'giovani': ('−32,8', '‰', 'Saldo dei giovani laureati, 2023', 'La perdita di laureati più alta del Centro-Nord, mentre le imprese non trovano tecnici.'),
    'energia': ('97,5', '%', 'Elettricità prodotta da rinnovabili', 'Una base già verde; il fotovoltaico sui siti produttivi è ancora poco sviluppato.'),
    'europa': ('2028', '', 'Avvio dei nuovi piani europei', 'Il nuovo bilancio UE premierà chi arriva con progetti pronti e misurabili.'),
}

def head(title, desc, css_href='assets/site.css'):
    return (f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@200..800&family=Atkinson+Hyperlegible+Next:ital,wght@0,200..800;1,200..800&family=Hedvig+Letters+Serif:opsz@12..24&display=swap">\n'
            f'<link rel="stylesheet" href="{css_href}">\n')

def nav(active):
    links = '\n'.join(f'      <a href="{f}"{" class=\"is-page\" aria-current=\"page\"" if k == active else ""}>{lab}</a>' for k, f, lab, _ in PAGES)
    return (f'<nav class="topnav" aria-label="Pagine">\n  <div class="topnav__in">\n    <a class="topnav__logo" href="index.html" aria-label="OpenEconomics, home"><img src="assets/logo-black.svg" alt="OpenEconomics" width="150" height="19"></a>\n'
            f'    <div class="topnav__links">\n{links}\n    </div>\n  </div>\n</nav>\n<div class="subnav" id="subnav" hidden></div>\n')

FOOTER = '''<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <div class="footer__logo"><img src="assets/logo-white.svg" alt="OpenEconomics" width="220" height="28"></div>
        <p class="footer__tag">Enabling adaptation. Empowering impact. With platforms, strategy, and trust.</p>
      </div>
      <div>
        <span class="footer__cond-k">Condizioni d'uso</span>
        <p class="footer__cond">Il presente documento e tutte le informazioni in esso contenute possono essere divulgati, a condizione che la distribuzione avvenga citando OpenEconomics come fonte. Le informazioni sono fornite a scopo puramente informativo e non implicano alcuna garanzia o impegno da parte di OpenEconomics. Le analisi economiche contenute nel documento sono state elaborate sulla base di fonti pubbliche autorevoli e fornitori di dati specialistici, con l'obiettivo di offrire una valutazione professionale, oggettiva e prudenziale in linea con le prassi metodologiche di comparto. Al documento e ai suoi contenuti si applicano il copyright e le norme in materia di protezione dei dati personali.</p>
      </div>
    </div>
    <div class="footer__bar"><span>www.openeconomics.eu · Copyright © OpenEconomics Srl 2026</span><span>Analisi territoriale della Provincia di Rieti · Settembre 2026</span></div>
  </div>
</footer>
<div class="tip" id="tip" hidden></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js"></script>
<script src="assets/site.js"></script>
'''
SCQA = BLOCKS[BLOCKS.index('<div class="scqa">'):_match_div(BLOCKS, BLOCKS.index('<div class="scqa">'))]
PRIO_INDEX = {re.sub(r'<[^>]+>', '', t): i for i, t in enumerate(re.findall(r'<p class="prio__t">(.*?)</p>', BLOCKS))}

def cta(href, label, cls=''):
    return f'<a class="cta {cls}" href="{href}"><span class="cta__lbl">{label}</span><span class="cta__tile">{ARROW}</span></a>'

def home():
    cards = '\n'.join(
        f'<a class="tcard" href="{FILE[k]}"><div class="tcard__top"><span class="tcard__k">{TITLE[k]}</span><span class="tcard__ic">{icon(k)}</span></div>'
        f'<div class="tcard__num">{n}<small>{u}</small></div><div class="tcard__nl">{nl}</div><p class="tcard__d">{txt}</p>'
        f'<span class="tcard__go">Approfondisci i dati {ARROW}</span></a>' for k, (n, u, nl, txt) in CARDS.items())
    prio = [('Priorità 1', 'Una filiera formativa tecnica completa', 'Corsi tecnici superiori a Rieti in farmaceutica e meccatronica, costruiti con più imprese.'),
            ('Priorità 2', 'Trattenere e far rientrare i laureati', 'Tirocini retribuiti, percorsi di rientro e ruoli qualificati nelle imprese locali.'),
            ('Priorità 3', 'Una rete di imprese e fornitori', 'Organizzare la Pump Valley e allargare le ricadute locali della farmaceutica.')]
    plist = '\n'.join(f'<div class="plist__i"><div class="plist__n">{a}</div><p class="plist__t">{b}</p><p class="plist__d">{c}</p></div>' for a, b, c in prio)
    return f'''<header class="hero hero--home" id="inizio">
  <div class="hero__text">
    <span class="chip">Analisi territoriale · Provincia di Rieti</span>
    <h1 class="title">Rieti forma i talenti che le sue imprese cercano, ma non riesce a trattenerli</h1>
    <p class="hero__sub">Sei temi spiegati in modo semplice, ognuno con un approfondimento sui dati a un clic di distanza. In fondo, le proposte e il collegamento con il bilancio europeo 2028–2034.</p>
    <div class="hero__btns">{cta('#temi', 'Esplora i temi', 'cta--pop')}{cta(FILE['proposte'], 'Le proposte', 'cta--ghost')}</div>
    <div class="hero-meta">
      <div><div class="hero-meta__k">Fonti</div><div class="hero-meta__v">ISTAT, Camera di Commercio Rieti-Viterbo, Unioncamere, MUR, Ministero dell'Istruzione, Terna, GSE</div></div>
      <div><div class="hero-meta__k">Aggiornamento</div><div class="hero-meta__v">Settembre 2026 · 73 comuni, 149.766 residenti</div></div>
    </div>
  </div>
  <div class="hero__map" aria-hidden="true">
    <svg id="heroMap" viewBox="0 0 520 440"></svg>
    <div class="hero__cap">I 73 comuni · dimensione = residenti · in verde il capoluogo</div>
  </div>
</header>
<section class="s s-grey" id="sintesi">
  <div class="wrap">
    <span class="chip">In breve</span>
    <h2 class="title">La situazione in quattro passaggi</h2>
    {SCQA}
  </div>
</section>
<section class="s" id="temi">
  <div class="wrap">
    <span class="chip">I temi</span>
    <h2 class="title">Sei temi per capire Rieti</h2>
    <p class="lead">Ogni scheda riassume un tema in una frase e un numero. Un clic apre l'approfondimento con mappe, grafici e tabelle.</p>
    <div class="tcards">
{cards}
    </div>
  </div>
</section>
<section class="s s-grey" id="proposte">
  <div class="wrap">
    <span class="chip">Le proposte</span>
    <h2 class="title">Tre priorità per trattenere i talenti</h2>
    <p class="lead">Oltre alle infrastrutture, i dati indicano leve mirate e meno costose, sostenute da quattro interventi di supporto.</p>
    <div class="plist">
{plist}
    </div>
    {cta(FILE['proposte'], 'Tutte le proposte')}
  </div>
</section>
'''

def topic(k):
    t = TOPIC[k]
    i = TOPICS.index(k)
    brief = '\n'.join(f'<li>{CHECK}<span>{b}</span></li>' for b in t['brief'])
    body = [f'''<header class="thero">
  <div class="thero__text">
    <p class="crumb"><a href="index.html">Home</a><span>/</span><span>{TITLE[k]}</span></p>
    <span class="chip">Tema {i + 1} di {len(TOPICS)} · {TITLE[k]}</span>
    <h1 class="title">{t["h1"]}</h1>
  </div>
  <aside class="brief" aria-label="In breve">
    <div class="brief__k">In breve</div>
    <ul>{brief}</ul>
    <div class="brief__why"><div class="brief__k">Perché conta per chi decide</div><p>{t["why"]}</p></div>
    {cta("#" + t["sections"][0][0], "Vai ai dati", "cta--pop")}
  </aside>
</header>''']
    for j, (sid, label, h2, html) in enumerate(t['sections']):
        cls = 's s-dark' if sid == 'verifica' else ('s s-grey' if j % 2 == 0 else 's')
        body.append(f'<section class="{cls}" id="{sid}" data-label="{label}">\n  <div class="wrap">\n    <span class="chip">Focus sui dati · {label}</span>\n    <h2 class="title">{h2}</h2>\n{html}\n  </div>\n</section>')
    todo = ''
    if t['todo']:
        items = '\n'.join(f'<a href="{FILE["proposte"]}#{"priorita" if PRIO_INDEX.get(x, 9) < 3 else "supporto"}"><div><div class="todo__t">{x}</div></div>{ARROW}</a>' for x in t['todo'])
        todo = f'<h3 class="sub">Le proposte collegate a questo tema</h3>\n<div class="todo">\n{items}\n</div>'
    prev_k = TOPICS[i - 1] if i > 0 else None
    next_k = TOPICS[i + 1] if i + 1 < len(TOPICS) else None
    pn = (f'<a class="prev" href="{FILE[prev_k]}"><span class="pn__k">Tema precedente</span><span class="pn__t">{TITLE[prev_k]}</span></a>' if prev_k
          else '<a class="prev" href="index.html"><span class="pn__k">Torna a</span><span class="pn__t">Home</span></a>')
    pn += (f'<a class="next" href="{FILE[next_k]}"><span class="pn__k">Tema successivo</span><span class="pn__t">{TITLE[next_k]}</span></a>' if next_k
           else '<a class="next" href="index.html"><span class="pn__k">Torna a</span><span class="pn__t">Home</span></a>')
    last_cls = 's' if len(t['sections']) % 2 == 0 else 's s-grey'
    body.append(f'<section class="{last_cls}">\n  <div class="wrap">\n{todo}\n<h3 class="sub">Continua la lettura</h3>\n<div class="pn">{pn}</div>\n  </div>\n</section>')
    return renumber('\n'.join(body))

def doc(title, desc, content):
    return ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head(title, desc) + '<style>body{margin:0}</style>\n</head>\n<body>\n' + content + '\n</body>\n</html>\n')

DESC = 'Analisi territoriale della Provincia di Rieti per decisori pubblici: temi chiave, approfondimenti sui dati, proposte e bilancio europeo 2028–2034.'
home_body = nav('home') + home() + FOOTER
(ROOT / 'index.html').write_text(doc('Rieti, territorio e talenti', DESC, home_body), encoding='utf-8')
for k in TOPICS:
    (ROOT / FILE[k]).write_text(doc(f'{TITLE[k]} · Rieti', DESC, nav(k) + topic(k) + FOOTER), encoding='utf-8')
# Artifact entry page: the viewer adds its own document skeleton, so no doctype/html/head here.
(ROOT / 'web' / 'artifact_home.html').write_text(head('Rieti, territorio e talenti', DESC) + home_body, encoding='utf-8')
print('built', ['index.html'] + [FILE[k] for k in TOPICS])
