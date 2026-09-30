"""Rebuild human-capital, skills-demand and training-supply tables and the skills figure.

Inputs (read-only, analysis/sources/skills):
- istat_bes_territori_2025.zip: ISTAT BES dei territori 2025, provincial indicators (LFS-based indicators
  are volatile for a province of ~150,000 residents; multi-year averages are reported alongside).
- istat_posas_{2019,2026}_province.zip: ISTAT resident population by age, 1 January (2026 is an estimate).
- ustat_07/13/14a_*.csv: MUR-USTAT enrolments 2024/25 (14a excludes online universities and cells <5).
- excelsior_2025_{rieti,lazio,italia}.xlsx: Unioncamere-Ministero del Lavoro, planned hires in 2025.
  These are firms' hiring intentions, not realised hires.
- mim_studenti_secondaria2_indirizzo_2024_25.csv + mim_anagrafe_scuole_statali_2025_26.csv: MIM open data.
"""
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'analysis/sources/skills'
OUT = ROOT / 'analysis/output'
FIG = ROOT / 'analysis/figures'
PEERS = ['Rieti', 'Viterbo', "L'Aquila", 'Terni', 'Frosinone', 'Lazio', 'Italia']
PEER_CODES = {'057': 'Rieti', '056': 'Viterbo', '066': "L'Aquila", '055': 'Terni', '060': 'Frosinone'}

# --- BES dei territori -----------------------------------------------------------------------
BES_IND = {'11RIC025': 'Net migration of Italian graduates aged 25-39, per 1,000 graduates',
           '02IST003P': 'Graduates and other tertiary, aged 25-39 (%)',
           '02IST002': 'At least upper-secondary, aged 25-64 (%)',
           '02IST004': 'Diploma holders enrolling at university in the same year (%)',
           '02IST006': 'NEET aged 15-29 (%)',
           '02IST007': 'Lifelong learning, aged 25-64 (%)',
           '02IST010P': 'Inadequate numeracy, lower-secondary year 3 (%)',
           '03LAV001': 'Employment rate aged 20-64 (%)',
           '04BEC002P': 'Average gross annual pay of employees (EUR)'}
with zipfile.ZipFile(SRC / 'istat_bes_territori_2025.zip') as z:
    name = next(n for n in z.namelist() if 'Indicatori_per_provincia_sesso' in n)
    B = pd.read_excel(z.open(name), sheet_name='Indicatori_per_provincia_sesso')
B['CODICE'] = B.CODICE.str.replace(r'-N\d+$', '', regex=True)          # e.g. 02IST002-N22 (2022 LFS break) -> 02IST002
B = B[B.CODICE.isin(BES_IND) & B.TERRITORIO.isin(PEERS) & B.SESSO.astype(str).str.lower().str.startswith('t')]
years = [c for c in B.columns if str(c).startswith('V20')]
B[years] = B[years].apply(lambda s: pd.to_numeric(s.astype(str).str.replace(',', '.'), errors='coerce'))
bes = B.melt(id_vars=['CODICE', 'TERRITORIO'], value_vars=years, var_name='year', value_name='value').dropna()
bes['year'] = bes.year.str[1:].astype(int)
bes['indicator'] = bes.CODICE.map(BES_IND)
bes.rename(columns={'CODICE': 'code', 'TERRITORIO': 'territory'}).to_csv(OUT / 'bes_human_capital_long.csv', index=False)
latest = bes.sort_values('year').groupby(['CODICE', 'TERRITORIO']).last().reset_index()
wide = latest.pivot(index='CODICE', columns='TERRITORIO', values='value')[PEERS]
wide.insert(0, 'latest_year', latest.groupby('CODICE').year.max())
avg3 = bes[bes.year >= bes.groupby('CODICE').year.transform('max') - 2].groupby(['CODICE', 'TERRITORIO']).value.mean().unstack()[PEERS]
wide = wide.join(avg3.add_suffix(' (3-yr avg)')[['Rieti (3-yr avg)', 'Italia (3-yr avg)']])
wide.insert(0, 'indicator', wide.index.map(BES_IND))
wide.to_csv(OUT / 'bes_human_capital_peers.csv', index_label='code')
# Rank of graduate migration among all provinces in the latest year (1 = most negative).
with zipfile.ZipFile(SRC / 'istat_bes_territori_2025.zip') as z:
    A = pd.read_excel(z.open(name), sheet_name='Indicatori_per_provincia_sesso')
g = A[A.CODICE.eq('11RIC025') & A.SESSO.astype(str).str.lower().str.startswith('t')].copy()
ly = f"V{int(latest[latest.CODICE.eq('11RIC025')].year.max())}"
g['v'] = pd.to_numeric(g[ly].astype(str).str.replace(',', '.'), errors='coerce')
prov = g[g.TERRITORIO.isin(set(A.TERRITORIO) - {'Italia', 'Nord', 'Centro', 'Mezzogiorno', 'Nord-ovest', 'Nord-est', 'Sud', 'Isole'})]
prov = prov[~prov.TERRITORIO.isin(['Piemonte', "Valle d'Aosta/Vallée d'Aoste", 'Liguria', 'Lombardia', 'Trentino-Alto Adige/Südtirol', 'Veneto',
    'Friuli-Venezia Giulia', 'Emilia-Romagna', 'Toscana', 'Umbria', 'Marche', 'Lazio', 'Abruzzo', 'Molise', 'Campania', 'Puglia',
    'Basilicata', 'Calabria', 'Sicilia', 'Sardegna', 'Bolzano/Bozen', 'Trento'])].dropna(subset=['v'])
prov['rank_most_negative'] = prov.v.rank(method='min').astype(int)
prov[['TERRITORIO', 'v', 'rank_most_negative']].rename(columns={'TERRITORIO': 'province', 'v': f'graduate_net_migration_{ly[1:]}'}) \
    .sort_values('rank_most_negative').to_csv(OUT / 'bes_graduate_migration_rank.csv', index=False)

# --- Young adults 20-34 ---------------------------------------------------------------------------
def posas(year):
    with zipfile.ZipFile(SRC / f'istat_posas_{year}_province.zip') as z:
        p = pd.read_csv(z.open(z.namelist()[0]), sep=';', skiprows=1, encoding='latin1', dtype=str)
    p = p.iloc[:, [0, 1, 2, -1]]                       # 2019 adds marital-status columns; keep code, name, age, total
    p.columns = ['code', 'province', 'age', 'total']
    p = p[p.age.astype(str).str.fullmatch(r'\d+') & p.age.ne('999')]   # 999 = provincial total row
    p = p.assign(age=p.age.astype(int), total=pd.to_numeric(p.total))
    return p
young = []
for y in (2019, 2026):
    p = posas(y)
    for code, lab in list(PEER_CODES.items()) + [(None, 'Italia')]:
        q = p if code is None else p[p.code.eq(code)]
        young.append(dict(year=y, territory=lab, age_20_34=q[q.age.between(20, 34)].total.sum(), total=q.total.sum()))
young = pd.DataFrame(young).pivot(index='territory', columns='year')
young.columns = [f'{a}_{b}' for a, b in young.columns]
young['age_20_34_change_pct'] = 100 * (young.age_20_34_2026 / young.age_20_34_2019 - 1)
young['total_change_pct'] = 100 * (young.total_2026 / young.total_2019 - 1)
young.to_csv(OUT / 'young_adults_20_34.csv')

# --- University: where residents study, and the Rieti hub ---------------------------------------
u = pd.read_csv(SRC / 'ustat_14a_iscrittixresidenzasedecorsogruppo.csv', sep=';', encoding='cp1252', dtype={'SedeP': str})
u = u[u.AnnoA.eq('2024/2025')]
PROV_NAME = {'Rieti': 'RIETI', 'Viterbo': 'VITERBO', "L'Aquila": "L'AQUILA", 'Terni': 'TERNI', 'Frosinone': 'FROSINONE'}
SEDE = {'Rieti': '57', 'Viterbo': '56', "L'Aquila": '66', 'Terni': '55', 'Frosinone': '60'}
rows = []
for lab, up in PROV_NAME.items():
    x = u[u.ResidenzaP.str.upper().eq(up)]
    rows.append(dict(province=lab, students_non_online=x.Isc.sum(), share_taught_in_own_province=x[x.SedeP.eq(SEDE[lab])].Isc.sum()/x.Isc.sum(),
                     share_taught_in_rome=x[x.SedeP.eq('58')].Isc.sum()/x.Isc.sum()))
tot = pd.read_csv(SRC / 'ustat_07_iscrittixresidenza.csv', sep=';', encoding='cp1252', dtype={'CODIstatProv': str})
tot['CODIstatProv'] = tot.CODIstatProv.str.zfill(3)
trend = tot[tot.CODIstatProv.isin(PEER_CODES)].groupby(['AnnoA', 'CODIstatProv']).Isc.sum().unstack().rename(columns=PEER_CODES)
trend.to_csv(OUT / 'university_students_by_residence_trend.csv')
uni = pd.DataFrame(rows).set_index('province')
uni['students_all_universities'] = trend.loc['2024/2025'].reindex(uni.index)
uni.to_csv(OUT / 'university_students_where_they_study.csv')
ri = u[u.ResidenzaP.str.upper().eq('RIETI')]
ri.groupby('AteneoNOME').Isc.sum().sort_values(ascending=False).pipe(lambda s: pd.DataFrame({'students': s, 'share': s / s.sum()})) \
  .to_csv(OUT / 'university_rieti_residents_by_university.csv')
c = pd.read_csv(SRC / 'ustat_13_iscrittixcorso.csv', sep=';', encoding='cp1252', dtype={'SedeP': str})
hub = c[c.SedeP.eq('57')].groupby(['AnnoA', 'AteneoNOME', 'CorsoNOME']).Isc.sum().reset_index()
hub.to_csv(OUT / 'university_rieti_hub_courses.csv', index=False)

# --- Excelsior: demand for skills --------------------------------------------------------------
def sheets(fn):
    return pd.read_excel(SRC / fn, sheet_name=None, header=None)
def find_row(book, title_keys, label, header_keys=()):
    """First sheet whose top rows contain all title_keys (and header_keys), row whose first text cell starts with label."""
    for name, v in book.items():
        if name.lower().startswith(('indice', 'cop', 'nota', 'sez')):
            continue
        top = ' '.join(str(a) for a in v.head(12).values.ravel() if str(a) != 'nan').lower()
        if all(k in top for k in title_keys) and all(k in top for k in header_keys):
            for _, r in v.iterrows():
                cells = [a for a in r if str(a) != 'nan']
                if cells and str(cells[0]).strip().lower().startswith(label.lower()):
                    nums = [a for a in cells[1:] if isinstance(a, (int, float))]
                    if nums:
                        return nums
    raise LookupError(f'{title_keys} / {label} not found')
books = {'Rieti': sheets('excelsior_2025_rieti.xlsx'), 'Lazio': sheets('excelsior_2025_lazio.xlsx'), 'Italia': sheets('excelsior_2025_italia.xlsx')}
head = {}
for lab, bk in books.items():
    d = find_row(bk, ['reperimento', 'esperienza'], 'TOTALE', ['mancanza di candidati'])
    e = find_row(bk, ['livelli di istruzione'], 'TOTALE', ['tecnologica'])
    shares = [x / e[0] * 100 for x in e[1:6]] if e[1] > 100 else e[1:6]    # Italy file gives counts, not shares
    assert abs(sum(shares) - 100) < 1, (lab, shares)
    d = [d[0]] + ([x / d[0] * 100 for x in d[1:4]] if d[1] > 100 else d[1:4])   # Italy file gives counts
    head[lab] = dict(planned_hires=d[0], hard_to_fill_pct=d[1], hard_to_fill_no_candidates_pct=d[2],
                     hard_to_fill_inadequate_preparation_pct=d[3], university_level_pct=shares[0], its_level_pct=shares[1])
pd.DataFrame(head).T.to_csv(OUT / 'excelsior_2025_headline.csv', index_label='territory')
RI = books['Rieti']
PROFILES = [('Tav4', 'Specialisti in scienze matematiche, chimiche', 'Science specialists (maths, chemistry, physics, natural sciences)'),
            ('Tav4', 'Ingegneri', 'Engineers'),
            ('Tav4', 'Tecnici della gestione dei processi produttivi', 'Production-process technicians'),
            ('Tav4', 'Tecnici in campo ingegneristico', 'Engineering technicians'),
            ('Tav4', 'Tecnici della salute', 'Health technicians'),
            ('Tav4', 'Meccanici artigianali, montatori, riparatori', 'Mechanics, fitters and maintenance workers'),
            ('Tav4', 'Operai specializzati meccanica di precisione', 'Precision-mechanics workers'),
            ('Tav4', 'Operatori impianti raffinazione gas e prod. petroliferi, per chimica', 'Chemical plant operators'),
            ('Tav4', 'Personale non qualificato addetto allo spostamento e alla consegna merci', 'Unskilled goods-handling and delivery staff'),
            ('Tav8', 'Indirizzo chimico-farmaceutico', 'Degree: chemistry-pharmaceutical'),
            ('Tav8', 'Indirizzo meccanica, meccatronica ed energia', 'Upper-secondary: mechanics, mechatronics, energy'),
            ('Tav8', 'Indirizzo elettronica ed elettrotecnica', 'Upper-secondary: electronics, electrotechnics')]
prof = []
for sheet, label, en in PROFILES:
    v = RI[sheet]
    hit = None
    for _, r in v.iterrows():
        cells = [a for a in r if str(a) != 'nan']
        if cells and str(cells[0]).strip().lower().startswith(label.lower()):
            hit = [pd.to_numeric(a, errors='coerce') for a in cells[1:]]     # '-' = suppressed -> NaN
            break
    if hit is None:
        print('Excelsior row not found:', label)
        continue
    # Tav4: hires, % under 30?.. , % hard to fill ; Tav8: hires, then shares with hard-to-fill in position 3
    hires, hard = (hit[0], hit[2]) if sheet == 'Tav4' else (hit[0], hit[4])
    prof.append(dict(profile=en, source_label=label, table=sheet, planned_hires_2025=hires, hard_to_fill_pct=hard))
prof = pd.DataFrame(prof)
prof.to_csv(OUT / 'excelsior_2025_rieti_profiles.csv', index=False)

# --- Upper-secondary technical and vocational supply --------------------------------------------
s = pd.read_csv(SRC / 'mim_studenti_secondaria2_indirizzo_2024_25.csv', dtype=str)
a = pd.read_csv(SRC / 'mim_anagrafe_scuole_statali_2025_26.csv', dtype=str)
a = a[a.PROVINCIA.str.upper().eq('RIETI')][['CODICESCUOLA', 'DENOMINAZIONESCUOLA', 'DENOMINAZIONEISTITUTORIFERIMENTO', 'DESCRIZIONECOMUNE']]
s = s.merge(a, on='CODICESCUOLA', how='inner')
s['students'] = s.ALUNNIMASCHI.astype(int) + s.ALUNNIFEMMINE.astype(int)
supply = s.groupby(['DENOMINAZIONEISTITUTORIFERIMENTO', 'DESCRIZIONECOMUNE', 'TIPOPERCORSO', 'INDIRIZZO']).students.sum().reset_index()
supply.sort_values(['TIPOPERCORSO', 'students'], ascending=[True, False]).to_csv(OUT / 'secondary_school_supply_rieti_2024_25.csv', index=False)
KEY = r'CHIM|BIOTEC|MECC|ELETTR|AUTOMAZ|MANUTENZ|ENERG|LOGIST|TRASPORT|APPARATI|ACQUE|INDUSTRIA'
tech = supply[supply.INDIRIZZO.str.contains(KEY, case=False, na=False)]
tech.groupby('TIPOPERCORSO').students.sum().to_csv(OUT / 'secondary_school_technical_tracks_rieti_summary.csv')

# --- Figure ---------------------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={'width_ratios': [1, 1.25]})
gm = bes[bes.CODICE.eq('11RIC025')]
last = gm.year.max()
m = gm[gm.year.eq(last)].set_index('TERRITORIO').value.reindex(PEERS[:-1] + ['Italia'])
av = gm[gm.year.between(last - 4, last)].groupby('TERRITORIO').value.mean().reindex(m.index)
ax = axes[0]
ypos = np.arange(len(m))
ax.barh(ypos, m.values, color=['#bd633b' if k == 'Rieti' else '#406c83' for k in m.index], height=.6, label=str(last))
ax.scatter(av.values, ypos, color='#222', zorder=3, s=22, label=f'{last-4}-{last} average')
ax.set_yticks(ypos, [k if k != 'Italia' else 'Italy*' for k in m.index]); ax.invert_yaxis()
ax.axvline(0, color='#555', lw=.7)
ax.set_xlabel('Net migration of Italian graduates aged 25-39, per 1,000')
ax.set_title('Rieti loses young graduates faster than any Centre-North province', loc='left', fontsize=11)
ax.legend(frameon=False, fontsize=9, loc='lower left')
ax = axes[1]
p = prof[~prof.profile.str.startswith('Unskilled')].dropna(subset=['hard_to_fill_pct']).sort_values('hard_to_fill_pct')
ax.barh(p.profile, p.hard_to_fill_pct, color=['#bd633b' if h >= 60 else '#8fb0c0' for h in p.hard_to_fill_pct])
for i, (h, n) in enumerate(zip(p.hard_to_fill_pct, p.planned_hires_2025)):
    ax.text(h + 1, i, f'{h:.0f}%  ·  {int(round(n, -1))} hires', va='center', fontsize=8.5)
ax.axvline(head['Rieti']['hard_to_fill_pct'], color='#555', lw=.8, ls='--')
ax.text(head['Rieti']['hard_to_fill_pct'] + 1, len(p) - .4, 'all hires', fontsize=8, color='#555')
ax.set_xlim(0, 125); ax.set_xlabel('Planned 2025 hires judged hard to fill, %')
ax.set_title('Technical profiles are scarce, but volumes are small', loc='left', fontsize=11)
ax.tick_params(axis='y', labelsize=8.5)
fig.text(.02, .01, '*Italy counts only moves to and from abroad. Sources: ISTAT BES dei territori 2025 (11RIC025); '
         'Unioncamere-Ministero del Lavoro, Excelsior 2025, Rieti (hiring intentions).', fontsize=8, color='#555555')
fig.tight_layout(rect=(0, .04, 1, 1))
fig.savefig(FIG / '06_skills_and_graduates.png', dpi=200, bbox_inches='tight')
fig.savefig(FIG / '06_skills_and_graduates.svg', bbox_inches='tight')

pd.set_option('display.width', 200)
print(wide.round(1).to_string())
print(young.round(1).to_string())
print(uni.round(3).to_string())
print(pd.DataFrame(head).T.round(1))
print(prof.round(1).to_string())
print(tech.groupby('TIPOPERCORSO').students.sum())
print(hub[hub.AnnoA.eq('2024/2025')].groupby('AteneoNOME').Isc.sum(), hub.groupby('AnnoA').Isc.sum().tail(6))
