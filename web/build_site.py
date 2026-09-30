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
import hashlib
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

# Change asset URLs whenever their contents change, preventing stale browser CSS/JS.
CSS_URL = 'assets/site.css?v=' + hashlib.sha256(css.encode('utf-8')).hexdigest()[:12]
JS_URL = 'assets/site.js?v=' + hashlib.sha256(js.encode('utf-8')).hexdigest()[:12]

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
    ('home', 'index.html', 'Sintesi', 'Sintesi'),
    ('persone', 'persone.html', 'Demografia', 'Demografia e territorio'),
    ('lavoro', 'lavoro.html', 'Lavoro', 'Lavoro e mobilità'),
    ('imprese', 'imprese.html', 'Imprese', 'Imprese ed export'),
    ('giovani', 'giovani.html', 'Competenze', 'Giovani e competenze'),
    ('energia', 'energia.html', 'Energia', 'Energia'),
    ('europa', 'europa.html', 'Fondi UE 2028–34', 'Europa 2028–2034'),
    ('proposte', 'proposte.html', 'Proposte di intervento', 'Proposte di intervento'),
]
FILE = {k: f for k, f, *_ in PAGES}
TITLE = {k: t for k, _, _, t in PAGES}
TOPICS = [k for k, *_ in PAGES if k != 'home']

TOPIC = {
 'persone': dict(
    h1='Declino demografico contenuto, forti divari territoriali',
    brief=['La provincia ha perso <strong>l\'1% dei residenti</strong> dal 2021, meno di diverse province vicine.',
           'Crescono solo i comuni della Sabina vicini a Roma; <strong>il capoluogo e la montagna perdono abitanti</strong>.',
           'Il saldo naturale negativo è il principale fattore di pressione demografica; i flussi migratori ne attenuano gli effetti.'],
    why='La programmazione deve distinguere le esigenze della Sabina, del capoluogo e dei comuni montani, integrando sviluppo economico e accesso ai servizi.',
    sections=[('mappa', 'La mappa', 'Crescita in Sabina, contrazione nel capoluogo e nelle aree montane', block('id="mapPop"')),
              ('distanza', 'Distanza da Roma', 'Distanza da Roma, declino demografico e invecchiamento',
               two(block('id="chBands"'), block('Rieti e le province di confronto'))),
              ('bilancio', 'Bilancio demografico', 'Il saldo migratorio compensa il deficit delle nascite', block('Saldo naturale e flussi migratori'))],
    todo=['Accessibilità al lavoro e sostegno alle famiglie', 'Servizi essenziali nei piccoli comuni']),
 'lavoro': dict(
    h1='Un pendolare su quattro lavora nella provincia di Roma',
    brief=['Ogni giorno <strong>14.449 residenti</strong> escono dalla provincia per lavorare e solo 5.090 persone vi entrano.',
           'Nella Sabina quasi <strong>la metà dei lavoratori</strong> va verso Roma, con viaggi di oltre un\'ora.',
           'Il polo industriale Rieti–Cittaducale <strong>presenta livelli occupazionali sostanzialmente invariati tra il 2011 e il 2021</strong>; salari e occupazione femminile restano bassi.'],
    why='Rafforzare l’occupazione locale richiede investimenti produttivi, collegamenti adeguati ai turni di lavoro e servizi che favoriscano la partecipazione, in particolare femminile.',
    sections=[('roma', 'Verso Roma', 'La prossimità a Roma orienta i flussi di lavoro', block('id="mapRome"')),
              ('destinazioni', 'Destinazioni di lavoro', 'Il lavoro locale arretra dal 2011', two(block('id="chCommute"'), block('Evoluzione dei flussi pendolari'))),
              ('viaggio', 'Tempi di percorrenza', 'Tempi e orari del pendolarismo limitano l’accessibilità al lavoro', block('Modalità e tempi degli spostamenti verso Roma')),
              ('occupazione', 'Occupazione e salari', 'Retribuzioni contenute e bassa partecipazione al lavoro', block('id="chEmp"'))],
    todo=['Accessibilità al lavoro e sostegno alle famiglie', 'Rafforzare le reti di imprese e fornitori']),
 'imprese': dict(
    h1='Export in crescita, base produttiva concentrata',
    brief=['Nel 2025 l\'export cresce del <strong>48,5%</strong>, ma tutto l\'aumento viene dalla farmaceutica; il resto cala del 6%.',
           'La farmaceutica è concentrata in <strong>poche aziende</strong>, con circa l\'1,3% degli occupati della provincia.',
           'La "Pump Valley" delle pompe dosatrici è radicata ed esporta, ma <strong>non ha una rete comune</strong>.'],
    why='La priorità è ampliare le ricadute territoriali dell’industria attraverso forniture locali, servizi specializzati e formazione, riducendo la dipendenza da poche imprese.',
    sections=[('export', 'Export e valore', 'La crescita dell\'export non si traduce in valore diffuso', two(block('id="chExp"'), block('id="chVa"'))),
              ('poli', 'Poli produttivi', 'Specializzazioni forti, ricadute occupazionali circoscritte', block('I principali poli produttivi'))],
    todo=['Rafforzare le reti di imprese e fornitori', 'Completare la filiera formativa tecnica']),
 'giovani': dict(
    h1='La perdita di laureati indebolisce il potenziale di sviluppo',
    brief=['Rieti perde giovani laureati <strong>più di ogni altra provincia del Centro-Nord</strong>.',
           'La partecipazione all’istruzione è elevata, ma solo <strong>il 12%</strong> degli universitari reatini studia in provincia: il raccordo con il lavoro locale resta debole.',
           'Le imprese non trovano profili tecnici in chimica e meccanica, ma in provincia <strong>non esiste un corso post-diploma</strong> in questi campi.'],
    why='Uno o due corsi tecnici superiori a Rieti, ruoli per laureati nelle imprese e percorsi di rientro possono invertire la tendenza.',
    sections=[('laureati', 'Laureati', 'Il saldo dei giovani laureati è il più negativo del Centro-Nord', block('id="chGrad"') + '\n' + block('Istruzione e giovani: Rieti e i confronti')),
              ('domanda', 'Domanda delle imprese', 'Le carenze di competenze interessano le specializzazioni locali', block('id="chProfiles"')),
              ('offerta', 'Offerta formativa', 'Completare la filiera tecnica con percorsi post-diploma',
               '<p class="txt">L\'IIS Rosatelli di Rieti ha circa 180 studenti negli indirizzi di chimica e biotecnologie e circa 350 in meccanica, meccatronica, elettronica e automazione; l\'IIS Aldo Moro di Fara in Sabina circa 380 in elettronica e telecomunicazioni. In provincia gli unici corsi ITS Academy, la formazione tecnica superiore dopo il diploma, sono di logistica e agroalimentare: quelli laziali di farmaceutica e meccatronica operano a Roma, Pomezia, Frosinone e Latina. L\'università a Rieti cresce (1.331 iscritti, erano 767 cinque anni fa) ma riguarda ingegneria edile e professioni sanitarie.</p>\n' + block('La domanda locale sostiene una formazione specialistica mirata'))],
    todo=['Completare la filiera formativa tecnica', 'Trattenere e far rientrare i laureati']),
 'energia': dict(
    h1='Produzione rinnovabile: una risorsa per lo sviluppo produttivo',
    brief=['Il <strong>97,5%</strong> dell\'elettricità prodotta in provincia viene da fonti rinnovabili, soprattutto idroelettriche.',
           'Il fotovoltaico cresce ma resta <strong>inferiore ai livelli delle province di confronto</strong>.',
           'Le coperture industriali, logistiche e pubbliche offrono un potenziale da valutare attraverso verifiche tecniche sui singoli siti.'],
    why='Efficienza e autoproduzione possono rafforzare la competitività delle imprese. Gli audit energetici sui siti a maggiore consumo devono orientare le priorità di investimento.',
    sections=[('produzione', 'Produzione', 'Elevata produzione rinnovabile, fotovoltaico da sviluppare', two(block('id="chEnergy"'), block('id="chPv"'))),
              ('siti', 'Siti produttivi', 'Concentrare gli interventi sui siti a maggiore consumo',
               '<p class="txt">La priorità è partire dai siti con consumi elevati e verificati, come le aree produttive e logistiche di Cittaducale e Fara in Sabina: efficienza, calore di processo, fotovoltaico sui tetti e connessione alla rete, prima di fissare obiettivi in megawatt.</p>')],
    todo=['Efficienza energetica e autoproduzione']),
 'europa': dict(
    h1='Programmazione europea 2028–2034: preparare le priorità territoriali',
    brief=['La proposta europea prevede <strong>piani nazionali e regionali integrati</strong>, con pagamenti legati a risultati misurabili.',
           'Tra gli obiettivi figurano <strong>competenze, lavoro di qualità e cambiamento demografico</strong>: ambiti prioritari per Rieti.',
           'Il Lazio è una regione "più sviluppata" per la media di Roma: <strong>il divario di Rieti resta sottorappresentato</strong> senza dati provinciali.'],
    why='Rieti deve contribuire alla programmazione regionale con un quadro condiviso dei fabbisogni e progetti dotati di obiettivi, responsabilità e indicatori di risultato.',
    sections=[('quadro', 'La proposta', 'Il quadro europeo e le implicazioni per Rieti', (SRC / 'europa_body.html').read_text(encoding='utf-8'))],
    todo=['Completare la filiera formativa tecnica', 'Trattenere e far rientrare i laureati', 'Efficienza energetica e autoproduzione']),
 'proposte': dict(
    h1='Tre priorità strategiche per competenze, occupazione e imprese',
    brief=['<strong>Completare la filiera formativa tecnica</strong>, con corsi ITS a Rieti legati alle imprese locali.',
           '<strong>Trattenere e far rientrare i laureati</strong>, con tirocini retribuiti e ruoli qualificati.',
           '<strong>Rafforzare le reti di imprese e fornitori</strong> intorno alla farmaceutica e alla Pump Valley.'],
    why='Formazione tecnica, occupazione qualificata e reti di impresa affiancano gli investimenti infrastrutturali: tre priorità direttamente collegate ai fabbisogni del territorio.',
    sections=[('priorita', 'Priorità', 'Le tre priorità', block('<div class="prio prio--3">', starts=('<div class="prio',))),
              ('supporto', 'Interventi di supporto', 'Quattro interventi a sostegno delle priorità strategiche', block('Accessibilità al lavoro e sostegno alle famiglie</p>', starts=('<div class="prio">',)))],
    todo=[]),
}
TOPIC['proposte']['sections'] = [(i, l, h, b.replace('2.1 e 2.3: carenza di profili tecnici', 'Giovani e competenze: carenza di profili tecnici')
                                  .replace('1.1 e 1.4: perdita di laureati', 'Giovani e lavoro: perdita di laureati')
                                  .replace('2.2: specializzazioni concentrate', 'Imprese: specializzazioni concentrate'))
                                 for i, l, h, b in TOPIC['proposte']['sections']]

CARDS = {
    'persone': ('−1,0', '%', 'Residenti dal 2021', 'Crescono solo i comuni vicini a Roma: il capoluogo e la montagna perdono abitanti.'),
    'lavoro': ('1 su 4', '', 'Pendolari che lavorano nella provincia di Roma', 'Ogni giorno 11.934 residenti vanno verso Roma; il polo industriale locale non cresce.'),
    'imprese': ('80', '%', 'Export dalla farmaceutica, 2025', 'L\'export cresce ma dipende da poche aziende; le altre esportazioni calano.'),
    'giovani': ('−32,8', '‰', 'Saldo dei giovani laureati, 2023', 'La perdita di laureati più alta del Centro-Nord, mentre le imprese non trovano tecnici.'),
    'energia': ('97,5', '%', 'Elettricità prodotta da rinnovabili', 'La produzione rinnovabile è un punto di forza; efficienza e fotovoltaico offrono ulteriori margini di sviluppo.'),
    'europa': ('2028', '', 'Avvio dei nuovi piani europei', 'La capacità progettuale è decisiva per tradurre le priorità territoriali in interventi finanziabili.'),
}

def head(title, desc, css_href=CSS_URL):
    return (f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@200..800&family=Atkinson+Hyperlegible+Next:ital,wght@0,200..800;1,200..800&family=Hedvig+Letters+Serif:opsz@12..24&display=swap">\n'
            f'<link rel="stylesheet" href="{css_href}">\n')

def nav(active):
    links = '\n'.join(
        f'<a href="{f}" class="{"topnav__proposal " if k == "proposte" else ""}{"is-page" if k == active else ""}"'
        f'{" aria-current=\"page\"" if k == active else ""}>{lab}</a>'
        for k, f, lab, _ in PAGES)
    return (f'<nav class="topnav" aria-label="Navigazione principale">\n  <div class="topnav__in">\n    <a class="topnav__logo" href="index.html" aria-label="OpenEconomics, sintesi"><img src="assets/logo-black.svg" alt="OpenEconomics" width="150" height="19"></a>\n'
            f'<div class="topnav__links">{links}</div>'
            f'<details class="topnav__mobile"><summary>Sezioni <span aria-hidden="true">+</span></summary><div class="topnav__menu">{links}</div></details>'
            '\n  </div>\n</nav>\n<div class="subnav" id="subnav" hidden></div>\n')

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
FOOTER = FOOTER.replace('src="assets/site.js"', f'src="{JS_URL}"')
SCQA = BLOCKS[BLOCKS.index('<div class="scqa">'):_match_div(BLOCKS, BLOCKS.index('<div class="scqa">'))]
PRIO_INDEX = {re.sub(r'<[^>]+>', '', t): i for i, t in enumerate(re.findall(r'<p class="prio__t">(.*?)</p>', BLOCKS))}

def cta(href, label, cls=''):
    return f'<a class="cta {cls}" href="{href}"><span class="cta__lbl">{label}</span><span class="cta__tile">{ARROW}</span></a>'

def home():
    cards = '\n'.join(
        f'<a class="tcard" href="{FILE[k]}"><div class="tcard__top"><span class="tcard__k">{TITLE[k]}</span><span class="tcard__ic">{icon(k)}</span></div>'
        f'<div class="tcard__num">{n}<small>{u}</small></div><div class="tcard__nl">{nl}</div><p class="tcard__d">{txt}</p>'
        f'<span class="tcard__go">Consulta i dati {ARROW}</span></a>' for k, (n, u, nl, txt) in CARDS.items())
    prio = [('Priorità 1', 'Completare la filiera formativa tecnica', 'Corsi tecnici superiori a Rieti in farmaceutica e meccatronica, costruiti con più imprese.'),
            ('Priorità 2', 'Trattenere e far rientrare i laureati', 'Tirocini retribuiti, percorsi di rientro e ruoli qualificati nelle imprese locali.'),
            ('Priorità 3', 'Rafforzare le reti di imprese e fornitori', 'Organizzare la Pump Valley e allargare le ricadute locali della farmaceutica.')]
    plist = '\n'.join(f'<div class="plist__i"><div class="plist__n">{a}</div><p class="plist__t">{b}</p><p class="plist__d">{c}</p></div>' for a, b, c in prio)
    return f'''<header class="hero hero--home" id="inizio">
  <div class="hero__text">
    <span class="chip">Analisi territoriale · Provincia di Rieti</span>
    <h1 class="title">Collegare formazione e imprese per creare lavoro qualificato a Rieti</h1>
    <p class="hero__sub">Completare la filiera tecnica, sostenere l’inserimento dei laureati e rafforzare le reti produttive: una strategia per trattenere competenze e ampliare le ricadute dello sviluppo sul territorio.</p>
    <div class="hero__btns">{cta('#proposte', 'Le priorità di intervento', 'cta--pop')}{cta('#temi', 'Le evidenze', 'cta--ghost')}</div>
    <div class="hero-meta">
      <div><div class="hero-meta__k">Fonti</div><div class="hero-meta__v">ISTAT, Camera di Commercio Rieti-Viterbo, Unioncamere, MUR, Ministero dell'Istruzione, Terna, GSE</div></div>
      <div><div class="hero-meta__k">Aggiornamento</div><div class="hero-meta__v">Settembre 2026 · 73 comuni, 149.766 residenti</div></div>
    </div>
  </div>
  <aside class="hero-agenda" aria-labelledby="agenda-title">
    <p class="agenda__eyebrow">Le ragioni della strategia</p>
    <h2 id="agenda-title">Una base industriale.<br>Un potenziale da realizzare.</h2>
    <p class="agenda__intro">Tre evidenze indicano perché competenze e filiere produttive devono essere al centro dell’intervento pubblico.</p>
    <div class="agenda__argument">
      <div class="agenda__step">
        <span class="agenda__number" aria-hidden="true">01</span>
        <div><h3>Le specializzazioni industriali offrono una base concreta</h3><p>Farmaceutica e pompe dosatrici esprimono competenze radicate e una presenza sui mercati internazionali su cui costruire lo sviluppo locale.</p></div>
      </div>
      <div class="agenda__step">
        <span class="agenda__number" aria-hidden="true">02</span>
        <div><h3>Le carenze di competenze limitano le ricadute locali</h3><p>Le imprese faticano a reperire profili in chimica e meccanica; mancano percorsi ITS provinciali nelle specializzazioni industriali.</p></div>
      </div>
      <div class="agenda__step">
        <span class="agenda__number" aria-hidden="true">03</span>
        <div><h3>La perdita di laureati indebolisce il potenziale di sviluppo</h3><p>Rieti registra il saldo dei giovani laureati più negativo del Centro-Nord: creare opportunità qualificate è decisivo per trattenerli.</p></div>
      </div>
    </div>
    <a class="agenda__link" href="#temi">Le evidenze a supporto {ARROW}</a>
  </aside>
</header>
<section class="s" id="temi">
  <div class="wrap">
    <span class="chip">I temi</span>
    <h2 class="title">Sei ambiti per la programmazione territoriale</h2>
    <p class="lead">Imprese, competenze e lavoro documentano le ragioni della strategia. Demografia, energia e programmazione europea ne definiscono le condizioni territoriali e le opportunità di attuazione.</p>
    <div class="tcards">
{cards}
    </div>
  </div>
</section>
<section class="s s-grey" id="proposte">
  <div class="wrap">
    <span class="chip" id="sintesi">Le priorità di intervento</span>
    <h2 class="title">Tre interventi per collegare competenze e sviluppo produttivo</h2>
    <p class="lead">Formare i profili richiesti dalle imprese, creare opportunità per i laureati e ampliare le relazioni di filiera: tre interventi complementari per attuare la strategia.</p>
    <div class="plist">
{plist}
    </div>
    {cta(FILE['proposte'], 'Azioni e indicatori di risultato')}
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
  <aside class="brief" aria-label="Evidenze principali">
    <div class="brief__k">Evidenze principali</div>
    <ul>{brief}</ul>
    <div class="brief__why"><div class="brief__k">Implicazioni per le politiche</div><p>{t["why"]}</p></div>
    {cta("#" + t["sections"][0][0], "Consulta l’analisi", "cta--pop")}
  </aside>
</header>''']
    for j, (sid, label, h2, html) in enumerate(t['sections']):
        cls = 's s-dark' if sid == 'verifica' else ('s s-grey' if j % 2 == 0 else 's')
        body.append(f'<section class="{cls}" id="{sid}" data-label="{label}">\n  <div class="wrap">\n    <span class="chip">Analisi · {label}</span>\n    <h2 class="title">{h2}</h2>\n{html}\n  </div>\n</section>')
    todo = ''
    if t['todo']:
        items = '\n'.join(f'<a href="{FILE["proposte"]}#{"priorita" if PRIO_INDEX.get(x, 9) < 3 else "supporto"}"><div><div class="todo__t">{x}</div></div>{ARROW}</a>' for x in t['todo'])
        todo = f'<h3 class="sub">Proposte di intervento collegate</h3>\n<div class="todo">\n{items}\n</div>'
    prev_k = TOPICS[i - 1] if i > 0 else None
    next_k = TOPICS[i + 1] if i + 1 < len(TOPICS) else None
    pn = (f'<a class="prev" href="{FILE[prev_k]}"><span class="pn__k">Tema precedente</span><span class="pn__t">{TITLE[prev_k]}</span></a>' if prev_k
          else '<a class="prev" href="index.html"><span class="pn__k">Torna a</span><span class="pn__t">Home</span></a>')
    pn += (f'<a class="next" href="{FILE[next_k]}"><span class="pn__k">Tema successivo</span><span class="pn__t">{TITLE[next_k]}</span></a>' if next_k
           else '<a class="next" href="index.html"><span class="pn__k">Torna a</span><span class="pn__t">Home</span></a>')
    last_cls = 's s-grey' if len(t['sections']) % 2 == 0 else 's'   # keep the white/grey alternation
    body.append(f'<section class="{last_cls}">\n  <div class="wrap">\n{todo}\n<h3 class="sub">Altri ambiti di analisi</h3>\n<div class="pn">{pn}</div>\n  </div>\n</section>')
    return renumber('\n'.join(body))

def doc(title, desc, content):
    return ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head(title, desc) + '<style>body{margin:0}</style>\n</head>\n<body>\n' + content + '\n</body>\n</html>\n')

DESC = 'Analisi territoriale della Provincia di Rieti per decisori pubblici: temi chiave, approfondimenti sui dati, proposte e bilancio europeo 2028–2034.'
home_body = nav('home') + home() + FOOTER
(ROOT / 'index.html').write_text(doc('Rieti · Analisi territoriale e priorità di intervento', DESC, home_body), encoding='utf-8')
for k in TOPICS:
    (ROOT / FILE[k]).write_text(doc(f'{TITLE[k]} · Rieti', DESC, nav(k) + topic(k) + FOOTER), encoding='utf-8')
# Artifact entry page: the viewer adds its own document skeleton, so no doctype/html/head here.
(ROOT / 'web' / 'artifact_home.html').write_text(head('Rieti · Analisi territoriale e priorità di intervento', DESC) + home_body, encoding='utf-8')
print('built', ['index.html'] + [FILE[k] for k in TOPICS])
