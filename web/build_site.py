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
    'economia': '<path d="M2 20h20"/><path d="M4 20V9l6 4V9l6 4V4h4v16"/>',
    'giovani': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    'energia': '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    'europa': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    'proposte': '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>',
}
icon = lambda k: f'<svg viewBox="0 0 24 24">{ICONS[k]}</svg>'

# ---------------------------------------------------------------- pages
PAGES = [  # key, file, nav label, card title
    ('home', 'index.html', 'Sintesi', 'Sintesi'),
    ('economia', 'economia.html', 'Economia e competenze', 'Economia e competenze'),
    ('persone', 'persone.html', 'Demografia', 'Demografia e territorio'),
    ('energia', 'energia.html', 'Energia', 'Energia'),
    ('europa', 'europa.html', 'Fondi UE 2028–34', 'Europa 2028–2034'),
    ('proposte', 'proposte.html', 'Proposte di intervento', 'Proposte di intervento'),
]
FILE = {k: f for k, f, *_ in PAGES}
LABEL = {k: lab for k, _, lab, _ in PAGES}
CHEV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
TITLE = {k: t for k, _, _, t in PAGES}
TOPICS = [k for k, *_ in PAGES if k not in ('home', 'proposte')]   # proposals are a standalone page

KEY_PRIO = ['Formazione tecnica e universitaria per il comparto chimico-farmaceutico',
            'Rafforzare le reti di imprese e fornitori',
            'Diversificare a partire dalle competenze esistenti']

FIG_CONC = """<div class="fig">
  <p class="fig-label">Grafico 1</p>
  <p class="fig-title">Esportazioni di beni per comparto, 2021–2025 (milioni di euro)</p>
  <div class="chart-box tall"><canvas id="chConc"></canvas></div>
  <p class="fig-note">La farmaceutica vale <strong>tra il 66% e l’80% dell’export in ogni anno dal 2021</strong>. Gli altri beni crescono fino al 2024, da 146 a 186 milioni, e calano nel 2025: l’aumento del 2025 è interamente farmaceutico.</p>
  <p class="source">Fonte: Camera di Commercio Rieti-Viterbo su dati ISTAT, rapporti sull’economia dell’Alto Lazio, edizioni 2023–2025 (per ogni anno l’edizione più recente). Le quote sono calcolate sui valori pubblicati nelle stesse tavole.</p>
  <details class="data"><summary><svg viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>Dati del grafico</summary><div class="oe-table__wrap" data-table="conc"></div></details>
</div>"""
FIG_SHARE = """<div class="fig">
  <p class="fig-label">Grafico 2</p>
  <p class="fig-title">Peso della farmaceutica sulle esportazioni (%)</p>
  <div class="chart-box short"><canvas id="chShare"></canvas></div>
  <p class="fig-note">Rieti dipende dalla farmaceutica molto più del Lazio, che pure è <strong>la prima regione italiana per export farmaceutico</strong>; in Italia la quota è del 9,1%.</p>
  <p class="source">Fonti: Rieti, Camera di Commercio Rieti-Viterbo su dati ISTAT, quota sull’export totale 2025 (la manifattura vale oltre il 98% dell’export reatino); Lazio e Italia, Farmindustria, Indicatori Farmaceutici 2025, quota sull’export manifatturiero 2024 (pp. 53 e 84).</p>
  <details class="data"><summary><svg viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>Dati del grafico</summary><div class="oe-table__wrap" data-table="share"></div></details>
</div>"""
CALLOUT_RISK = """<div class="callout"><svg viewBox="0 0 24 24"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg><p><strong>Perché è un rischio strutturale.</strong> Quando le esportazioni dipendono da un solo comparto e da poche imprese, le decisioni industriali prese altrove, le variazioni della domanda internazionale e i cambiamenti nella regolazione del farmaco si trasmettono direttamente al territorio. Nel 2026, secondo le rappresentanze sindacali, il principale gruppo del settore è in riorganizzazione. Una base di competenze più ampia riduce questa esposizione.</p></div>"""
TBL_COURSES = """<div class="tbl oe-table__wrap">
  <table class="oe-table">
    <caption class="oe-figure-label" style="text-align:left;padding:14px 16px 0">Tabella 1 · Corsi universitari attivi a Rieti, 2024/25</caption>
    <thead><tr><th>Area</th><th>Corsi</th><th class="num">Iscritti</th></tr></thead>
    <tbody>
      <tr><td>Professioni sanitarie</td><td>Infermieristica, radiologia, fisioterapia, laboratorio biomedico, igiene dentale, prevenzione, logopedia, dietistica</td><td class="num">628</td></tr>
      <tr><td>Ingegneria edile e ambientale</td><td>Tre corsi di laurea e di laurea magistrale</td><td class="num">467</td></tr>
      <tr><td>Medicina e chirurgia</td><td>Avviato nel 2024/25</td><td class="num">99</td></tr>
      <tr><td>Agricoltura e montagna</td><td>Scienze della montagna; gestione digitale dell’agricoltura e del territorio montano</td><td class="num">96</td></tr>
      <tr><td>Economia</td><td>Economia dell’innovazione</td><td class="num">41</td></tr>
      <tr class="hl"><td>Chimica, farmacia, biotecnologie, ingegneria chimica o industriale</td><td>Nessun corso</td><td class="num">0</td></tr>
    </tbody>
  </table>
</div>
<p class="source">Fonti: MUR, Anagrafe nazionale degli studenti, iscritti 2024/25 per sede del corso in provincia di Rieti (1.331 in totale); Sapienza Università di Roma, offerta formativa 2025/26 a Rieti, che aggiunge Psicologia.</p>"""
LEVERS = """<div class="plist">
  <div class="plist__i"><div class="plist__n">Formare</div><p class="plist__t">Competenze per il comparto</p><p class="plist__d">Percorsi ITS e universitari a Rieti in produzione, controllo qualità e tecnologie chimico-farmaceutiche, costruiti con le imprese.</p></div>
  <div class="plist__i"><div class="plist__n">Rafforzare</div><p class="plist__t">Fornitori e servizi locali</p><p class="plist__d">Manutenzione, convalida dei processi, servizi di laboratorio e logistica qualificata intorno alle imprese farmaceutiche.</p></div>
  <div class="plist__i"><div class="plist__n">Diversificare</div><p class="plist__t">Filiere affini</p><p class="plist__d">Estendere le competenze di processo e qualità a pompe dosatrici, trattamento delle acque e trasformazione alimentare, da verificare con le imprese.</p></div>
</div>"""

def _prio(icon_paths, title, need, action, kpi, key=True):
    need_row = f'<p class="prio__row"><b>Fabbisogno</b>{need}</p>' if need else ''
    return (f'<div class="prio__i{" prio__i--key" if key else ""}"><div class="prio__head"><span class="prio__ic"><svg viewBox="0 0 24 24">{icon_paths}</svg></span>'
            f'<p class="prio__t">{title}</p></div>{need_row}<p class="prio__row"><b>Azione prioritaria</b>{action}</p>'
            f'<p class="prio__row"><b>Indicatori di risultato</b>{kpi}</p></div>')
PRIO_KEY = '<div class="prio prio--3">' + ''.join([
    _prio(ICONS['giovani'], KEY_PRIO[0], 'Economia e competenze: profili chimici e farmaceutici tra i più difficili da reperire, senza corsi universitari o ITS a Rieti.',
          'Attivare a Rieti, con le fondazioni ITS laziali, un percorso in produzione e controllo qualità farmaceutico e valutare con gli atenei già presenti un corso di laurea professionalizzante in tecnologie chimico-farmaceutiche, con tirocini nelle imprese.',
          'Iscritti e diplomati; quota occupata in provincia a 12 mesi; difficoltà di reperimento dei profili interessati.'),
    _prio('<circle cx="12" cy="12" r="3"/><path d="M12 1v4"/><path d="M12 19v4"/><path d="M4.22 4.22l2.83 2.83"/><path d="M16.95 16.95l2.83 2.83"/><path d="M1 12h4"/><path d="M19 12h4"/>',
          KEY_PRIO[1], 'Export concentrato in poche imprese; nessuna struttura comune tra i produttori.',
          'Mappare con le imprese del comparto i profili mancanti e i requisiti per i fornitori; organizzare i produttori di pompe dosatrici in una rete comune.',
          'Fornitori locali qualificati e nuovi contratti; retribuzioni.'),
    _prio('<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>', KEY_PRIO[2], 'Export dipendente da un solo comparto; le altre esportazioni calano nel 2025.',
          'Individuare con imprese e Camera di Commercio le filiere affini in cui le competenze di processo e qualità sono trasferibili, come trattamento delle acque e trasformazione alimentare, e sostenere progetti pilota; per gli impianti agroalimentari comuni, verificare prima volumi, acquirenti e margini.',
          'Quota dell’export non farmaceutico; nuove imprese e addetti nelle filiere affini.')]) + '</div>'
_support = block('Accessibilità al lavoro e sostegno alle famiglie</p>', starts=('<div class="prio">',))
_grad = _prio('<path d="m9 18 6-6-6-6"/><path d="M3 12h12"/><path d="M21 5v14"/>', 'Trattenere e far rientrare i laureati', '',
              'Tirocini retribuiti e percorsi di rientro per i reatini che studiano a Roma e L’Aquila, collegati alle imprese del comparto.',
              'Tirocini trasformati in contratti; saldo migratorio dei laureati.', key=False)
PRIO_SUPPORT = _support.replace('<div class="prio">', '<div class="prio">' + _grad, 1)
_last = PRIO_SUPPORT.rfind('<div class="prio__i">')
PRIO_SUPPORT = PRIO_SUPPORT[:_last] + PRIO_SUPPORT[_match_div(PRIO_SUPPORT, _last):]   # drop agri-food: now part of diversification

TOPIC = {
 'persone': dict(
    h1='Declino demografico contenuto, forti divari territoriali',
    brief=['La provincia ha perso <strong>l\'1% dei residenti</strong> dal 2021, meno di diverse province vicine.',
           'Crescono solo i comuni della Sabina vicini a Roma; <strong>il capoluogo e la montagna perdono abitanti</strong>.',
           'Il saldo naturale negativo è il principale fattore di pressione demografica; i flussi migratori ne attenuano gli effetti.',
           'Il polo industriale Rieti–Cittaducale <strong>non ha aumentato i posti di lavoro tra il 2011 e il 2021</strong>, mentre i suoi residenti che lavorano a Roma sono passati da 1.120 a 1.653.'],
    why='La programmazione deve distinguere le esigenze della Sabina, del capoluogo e dei comuni montani. Senza nuove opportunità qualificate in provincia, la tenuta demografica resta legata al pendolarismo verso Roma.',
    sections=[('mappa', 'La mappa', 'Crescita in Sabina, contrazione nel capoluogo e nelle aree montane', block('id="mapPop"')),
              ('distanza', 'Distanza da Roma', 'Distanza da Roma, declino demografico e invecchiamento',
               two(block('id="chBands"'), block('Rieti e le province di confronto'))),
              ('bilancio', 'Bilancio demografico', 'Il saldo migratorio compensa il deficit delle nascite', block('Saldo naturale e flussi migratori')),
              ('mobilita', 'Mobilità', 'Il lavoro si sposta verso Roma, il polo industriale non cresce', block('id="mapRome"') + '\n' + two(block('id="chCommute"'), block('Evoluzione dei flussi pendolari')))],
    todo=['Accessibilità al lavoro e sostegno alle famiglie', 'Servizi essenziali nei piccoli comuni']),
 'economia': dict(
    h1='Una specializzazione farmaceutica da consolidare e diversificare',
    brief=['Dal 2021 la farmaceutica rappresenta <strong>tra due terzi e l’80% dell’export</strong> provinciale, contro il 48% nel Lazio: una concentrazione strutturale.',
           'I profili del comparto sono tra i più difficili da reperire: lo sono <strong>l’84% dei laureati in chimica e farmaceutica</strong> e il 98% degli specialisti in scienze matematiche, chimiche, fisiche e naturali richiesti dalle imprese.',
           'A Rieti <strong>non sono attivi corsi universitari né percorsi ITS</strong> in chimica, farmacia o biotecnologie che consentano di valorizzare questo know-how.'],
    why='Formare a Rieti le competenze richieste dal comparto ne rafforza il radicamento e consente di estenderle a filiere affini, riducendo l’esposizione a un solo settore e aumentando la resilienza del sistema produttivo.',
    sections=[('concentrazione', 'Concentrazione dell’export', 'Da cinque anni l’export dipende da un solo comparto',
               FIG_CONC + '\n' + two(FIG_SHARE, block('id="chVa"')) + '\n' + CALLOUT_RISK),
              ('domanda', 'Domanda di competenze', 'Un comparto che cerca competenze e fatica a trovarle',
               block('id="chProfiles"') + '\n<p class="txt">La difficoltà di reperimento si inserisce in un mercato del lavoro locale con retribuzioni contenute e una partecipazione inferiore alla media: creare posti qualificati nel comparto è anche la leva più diretta per migliorare la qualità dell’occupazione.</p>\n' + block('id="chEmp"')),
              ('formazione', 'Offerta formativa', 'A Rieti mancano i corsi per valorizzare il know-how del comparto',
               TBL_COURSES + '\n<p class="txt">La base scolastica esiste: l’IIS Rosatelli di Rieti ha 179 studenti negli indirizzi di chimica e biotecnologie e 306 in meccanica, meccatronica, elettronica e automazione. Dopo il diploma, però, in provincia non ci sono percorsi in questi ambiti: gli unici corsi ITS Academy sono di logistica e agroalimentare, e quelli laziali di farmaceutica operano a Roma e Pomezia. L’unico corso universitario vicino al comparto, Tecniche di laboratorio biomedico (49 iscritti), è orientato alla sanità. Senza percorsi locali, chi vuole studiare in questi ambiti si forma altrove: <strong>solo il 12% degli universitari reatini studia in provincia</strong>, e il saldo dei giovani laureati è il più negativo del Centro-Nord.</p>\n' + block('id="chGrad"')),
              ('diversificazione', 'Diversificazione', 'Dalle competenze farmaceutiche a un sistema produttivo più resiliente',
               '<p class="txt">Le competenze del comparto farmaceutico, come la produzione in ambiente controllato, il controllo qualità, la convalida dei processi e la manutenzione degli impianti, servono anche ad attività già presenti sul territorio. Formarle a Rieti rafforza il settore e allarga la base su cui possono crescere altre imprese, a partire da quelle della Pump Valley.</p>\n' + block('I principali poli produttivi') + '\n' + LEVERS)],
    todo=KEY_PRIO),
 'energia': dict(
    h1='Produzione rinnovabile: una risorsa per lo sviluppo produttivo',
    brief=['Il <strong>97,5%</strong> dell\'elettricità prodotta in provincia viene da fonti rinnovabili, soprattutto idroelettriche.',
           'Il fotovoltaico cresce ma resta <strong>inferiore ai livelli delle province di confronto</strong>.',
           'Le coperture industriali, logistiche e pubbliche offrono un potenziale da valutare attraverso verifiche tecniche sui singoli siti.'],
    why='Efficienza e autoproduzione possono rafforzare la competitività delle imprese, a partire dalle aree produttive di Cittaducale, dove opera il comparto farmaceutico, e da quella logistica di Fara in Sabina. Gli audit energetici devono orientare le priorità di investimento.',
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
    todo=['Formazione tecnica e universitaria per il comparto chimico-farmaceutico', 'Diversificare a partire dalle competenze esistenti', 'Efficienza energetica e autoproduzione']),
 'proposte': dict(
    h1='Tre priorità per competenze, filiere e diversificazione produttiva',
    brief=['<strong>Formare a Rieti le competenze del comparto chimico-farmaceutico</strong>, con percorsi ITS e universitari costruiti con le imprese.',
           '<strong>Rafforzare le reti di imprese e fornitori</strong> intorno alla farmaceutica e alla Pump Valley.',
           '<strong>Diversificare a partire dalle competenze esistenti</strong>, estendendole a filiere affini per ridurre la dipendenza da un solo comparto.'],
    why='Competenze, filiere e diversificazione affiancano gli investimenti infrastrutturali e rispondono direttamente alla concentrazione dell’export e alla carenza di profili qualificati.',
    sections=[('priorita', 'Priorità', 'Le tre priorità', PRIO_KEY),
              ('supporto', 'Interventi di supporto', 'Quattro interventi a sostegno delle priorità strategiche', PRIO_SUPPORT)],
    todo=[]),
}
CARDS = {
    'persone': ('−1,0', '%', 'Residenti dal 2021', 'Crescono solo i comuni vicini a Roma: il capoluogo e la montagna perdono abitanti.'),
    'economia': ('80', '%', 'Export dalla farmaceutica, 2025', 'Un comparto di eccellenza che concentra il rischio, cerca competenze e non trova a Rieti corsi per formarle.'),
    'energia': ('97,5', '%', 'Elettricità prodotta da rinnovabili', 'La produzione rinnovabile è un punto di forza; efficienza e fotovoltaico offrono ulteriori margini di sviluppo.'),
    'europa': ('2028', '', 'Avvio dei nuovi piani europei', 'La capacità progettuale è decisiva per tradurre le priorità territoriali in interventi finanziabili.'),
}

CARDS = {k: CARDS[k] for k in TOPICS}   # cards follow the topic order

def head(title, desc, css_href=CSS_URL):
    return (f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@200..800&family=Atkinson+Hyperlegible+Next:ital,wght@0,200..800;1,200..800&family=Hedvig+Letters+Serif:opsz@12..24&display=swap">\n'
            f'<link rel="stylesheet" href="{css_href}">\n')

def nav(active):
    def a(k, extra=''):
        cur = k == active
        return (f'<a href="{FILE[k]}" class="{extra}{"is-page" if cur else ""}"'
                f'{" aria-current=\"page\"" if cur else ""}>{TITLE[k] if k in TOPICS else LABEL[k]}</a>')
    topics = ''.join(a(k) for k in TOPICS)
    on_topic = ' is-page' if active in TOPICS else ''
    desktop = (a('home') + f'<div class="navdrop"><button class="navdrop__btn{on_topic}" type="button" aria-expanded="false" aria-haspopup="true">Temi {CHEV}</button>'
               f'<div class="navdrop__menu">{topics}</div></div>' + a('proposte', 'topnav__proposal '))
    mobile = a('home') + f'<span class="topnav__group">Temi</span>{topics}' + a('proposte', 'topnav__proposal ')
    return (f'<nav class="topnav" aria-label="Navigazione principale">\n  <div class="topnav__in">\n    <a class="topnav__logo" href="index.html" aria-label="OpenEconomics, sintesi"><img src="assets/logo-black.svg" alt="OpenEconomics" width="150" height="19"></a>\n'
            f'<div class="topnav__links">{desktop}</div>'
            f'<details class="topnav__mobile"><summary>Sezioni <span aria-hidden="true">+</span></summary><div class="topnav__menu">{mobile}</div></details>'
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

def cta(href, label, cls=''):
    return f'<a class="cta {cls}" href="{href}"><span class="cta__lbl">{label}</span><span class="cta__tile">{ARROW}</span></a>'

def home():
    cards = '\n'.join(
        f'<a class="tcard" href="{FILE[k]}"><div class="tcard__top"><span class="tcard__k">{TITLE[k]}</span><span class="tcard__ic">{icon(k)}</span></div>'
        f'<div class="tcard__num">{n}<small>{u}</small></div><div class="tcard__nl">{nl}</div><p class="tcard__d">{txt}</p>'
        f'<span class="tcard__go">Consulta i dati {ARROW}</span></a>' for k, (n, u, nl, txt) in CARDS.items())
    prio = [('Priorità 1', 'Formazione tecnica e universitaria per il comparto chimico-farmaceutico', 'Percorsi ITS e universitari a Rieti, costruiti con le imprese, per formare i profili oggi difficili da reperire.'),
            ('Priorità 2', 'Rafforzare le reti di imprese e fornitori', 'Fornitori e servizi locali intorno alla farmaceutica; una rete comune per la Pump Valley.'),
            ('Priorità 3', 'Diversificare a partire dalle competenze esistenti', 'Estendere il know-how di processo e qualità a filiere affini, per ridurre la dipendenza da un solo comparto.')]
    plist = '\n'.join(f'<div class="plist__i"><div class="plist__n">{a}</div><p class="plist__t">{b}</p><p class="plist__d">{c}</p></div>' for a, b, c in prio)
    return f'''<header class="hero hero--home" id="inizio">
  <div class="hero__text">
    <span class="chip">Analisi territoriale · Provincia di Rieti</span>
    <h1 class="title">Collegare formazione e imprese per creare lavoro qualificato a Rieti</h1>
    <p class="hero__sub">La farmaceutica traina l’export ma concentra il rischio su un solo comparto. Formare a Rieti le competenze che il settore cerca, rafforzare le filiere e diversificare: una strategia per trattenere i talenti e rendere l’economia più resiliente.</p>
    <div class="hero-meta">
      <div><div class="hero-meta__k">Fonti</div><div class="hero-meta__v">ISTAT, Camera di Commercio Rieti-Viterbo, Unioncamere, MUR, Ministero dell'Istruzione, Terna, GSE</div></div>
      <div><div class="hero-meta__k">Aggiornamento</div><div class="hero-meta__v">Settembre 2026 · 73 comuni, 149.766 residenti</div></div>
    </div>
  </div>
  <aside class="hero-agenda" aria-labelledby="agenda-title">
    <p class="agenda__eyebrow">Le ragioni della strategia</p>
    <h2 id="agenda-title">Una base industriale.<br>Un potenziale da realizzare.</h2>
    <p class="agenda__intro">Tre evidenze indicano perché le competenze del comparto farmaceutico devono essere al centro dell’intervento pubblico.</p>
    <div class="agenda__argument">
      <div class="agenda__step">
        <span class="agenda__number" aria-hidden="true">01</span>
        <div><h3>L’export dipende da un solo comparto</h3><p>La farmaceutica vale l’80% delle esportazioni, contro il 48% nel Lazio: una specializzazione di eccellenza che concentra però il rischio su poche imprese.</p></div>
      </div>
      <div class="agenda__step">
        <span class="agenda__number" aria-hidden="true">02</span>
        <div><h3>Il comparto cerca competenze che non trova</h3><p>I profili in chimica e farmaceutica sono tra i più difficili da reperire, ma a Rieti non esistono corsi universitari o ITS in questi ambiti.</p></div>
      </div>
      <div class="agenda__step">
        <span class="agenda__number" aria-hidden="true">03</span>
        <div><h3>Formare competenze per diversificare</h3><p>Valorizzare il know-how farmaceutico in filiere affini rafforza la resilienza del sistema produttivo e offre opportunità ai giovani laureati, oggi in forte uscita.</p></div>
      </div>
    </div>
  </aside>
</header>
<section class="s" id="temi">
  <div class="wrap">
    <span class="chip">I temi</span>
    <h2 class="title">Quattro ambiti per la programmazione territoriale</h2>
    <p class="lead">Economia e competenze documentano le ragioni della strategia. Demografia, energia e programmazione europea ne definiscono le condizioni territoriali e le opportunità di attuazione.</p>
    <div class="tcards tcards--2">
{cards}
    </div>
  </div>
</section>
<section class="s s-grey" id="proposte">
  <div class="wrap">
    <span class="chip" id="sintesi">Le priorità di intervento</span>
    <h2 class="title">Tre interventi per competenze, filiere e diversificazione</h2>
    <p class="lead">Formare i profili che il comparto farmaceutico cerca, rafforzare le relazioni di filiera e diversificare la base produttiva: tre interventi complementari per attuare la strategia.</p>
    <div class="plist">
{plist}
    </div>
    {cta(FILE['proposte'], 'Azioni e indicatori di risultato')}
  </div>
</section>
'''

def topic(k):
    t = TOPIC[k]
    standalone = k not in TOPICS
    i = TOPICS.index(k) if not standalone else len(TOPICS)
    brief = '\n'.join(f'<li>{CHECK}<span>{b}</span></li>' for b in t['brief'])
    body = [f'''<header class="thero">
  <div class="thero__text">
    <p class="crumb"><a href="index.html">Sintesi</a><span>/</span><span>{TITLE[k]}</span></p>
    <span class="chip">{TITLE[k] if standalone else f"Tema {i + 1} di {len(TOPICS)} · {TITLE[k]}"}</span>
    <h1 class="title">{t["h1"]}</h1>
  </div>
  <aside class="brief" aria-label="{'In sintesi' if standalone else 'Evidenze principali'}">
    <div class="brief__k">{'In sintesi' if standalone else 'Evidenze principali'}</div>
    <ul>{brief}</ul>
    <div class="brief__why"><div class="brief__k">Implicazioni per le politiche</div><p>{t["why"]}</p></div>
  </aside>
</header>''']
    for j, (sid, label, h2, html) in enumerate(t['sections']):
        cls = 's s-dark' if sid == 'verifica' else ('s s-grey' if j % 2 == 0 else 's')
        body.append(f'<section class="{cls}" id="{sid}" data-label="{label}">\n  <div class="wrap">\n    <span class="chip">Analisi · {label}</span>\n    <h2 class="title">{h2}</h2>\n{html}\n  </div>\n</section>')
    todo = ''
    if t['todo']:
        items = '\n'.join(f'<a href="{FILE["proposte"]}#{"priorita" if x in KEY_PRIO else "supporto"}"><div><div class="todo__t">{x}</div></div>{ARROW}</a>' for x in t['todo'])
        todo = f'<h3 class="sub">Proposte di intervento collegate</h3>\n<div class="todo">\n{items}\n</div>'
    prev_k = TOPICS[i - 1] if 0 < i <= len(TOPICS) - 1 else None
    next_k = TOPICS[i + 1] if i + 1 < len(TOPICS) else None
    pn = (f'<a class="prev" href="{FILE[prev_k]}"><span class="pn__k">Tema precedente</span><span class="pn__t">{TITLE[prev_k]}</span></a>' if prev_k
          else '<a class="prev" href="index.html"><span class="pn__k">Torna a</span><span class="pn__t">Sintesi</span></a>')
    if next_k:
        pn += f'<a class="next" href="{FILE[next_k]}"><span class="pn__k">Tema successivo</span><span class="pn__t">{TITLE[next_k]}</span></a>'
    elif not standalone:   # last topic leads to the proposals
        pn += f'<a class="next" href="{FILE["proposte"]}"><span class="pn__k">Prosegui con</span><span class="pn__t">{TITLE["proposte"]}</span></a>'
    else:                  # proposals page: back to the topics
        pn += f'<a class="next" href="{FILE[TOPICS[0]]}"><span class="pn__k">Consulta i temi</span><span class="pn__t">{TITLE[TOPICS[0]]}</span></a>'
    last_cls = 's s-grey' if len(t['sections']) % 2 == 0 else 's'   # keep the white/grey alternation
    body.append(f'<section class="{last_cls}">\n  <div class="wrap">\n{todo}\n<h3 class="sub">Altri ambiti di analisi</h3>\n<div class="pn">{pn}</div>\n  </div>\n</section>')
    return renumber('\n'.join(body))

def doc(title, desc, content):
    return ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head(title, desc) + '<style>body{margin:0}</style>\n</head>\n<body>\n' + content + '\n</body>\n</html>\n')

DESC = 'Analisi territoriale della Provincia di Rieti per decisori pubblici: temi chiave, approfondimenti sui dati, proposte e bilancio europeo 2028–2034.'
home_body = nav('home') + home() + FOOTER
(ROOT / 'index.html').write_text(doc('Rieti · Analisi territoriale e priorità di intervento', DESC, home_body), encoding='utf-8')
for k in TOPICS + ['proposte']:
    (ROOT / FILE[k]).write_text(doc(f'{TITLE[k]} · Rieti', DESC, nav(k) + topic(k) + FOOTER), encoding='utf-8')
# Artifact entry page: the viewer adds its own document skeleton, so no doctype/html/head here.
(ROOT / 'web' / 'artifact_home.html').write_text(head('Rieti · Analisi territoriale e priorità di intervento', DESC) + home_body, encoding='utf-8')
print('built', ['index.html'] + [FILE[k] for k in TOPICS + ['proposte']])
