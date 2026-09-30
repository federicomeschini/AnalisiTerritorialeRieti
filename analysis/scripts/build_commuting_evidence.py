"""Rebuild commuting tables and the commuting slide figure. Run from any working directory.

Inputs (read-only):
- matrix_pendoLAVORO_2021.txt: ISTAT 2021 work matrix (model-based, at least 3 days/week, 31/12/2021).
- analysis/sources/istat_pendolarismo/matrici_pendolarismo_2011.zip: ISTAT 2011 census matrix
  (full count below 20,000 residents; study and work; sex, mode, departure time, duration).
- analysis/sources/istat_pendolarismo/Lazio.zip: ISTAT inter-municipal road matrix, 1/1/2021 municipalities
  (TEP_TOT = minutes with traffic impedance, TTP_TOT = free-flow minutes, KM_TOT = road km).
- Optional: the ISTAT 2021 study matrix (non-employed students only, model-based), published only through
  esploradati.istat.it. Fetch it with fetch_istat_study_matrix.py; when absent, study results use 2011 only.

Comparability: 2011 is a census count of people who declared travelling daily from home (study includes
nursery and pre-school; each person reports one motive). 2021 is modelled from administrative sources for
trips on at least 3 days a week, and the study matrix excludes employed students. Neither matrix reports
school level; 2011-2021 differences mix real change with these definitional changes.
"""
from pathlib import Path
import io
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'analysis/sources/istat_pendolarismo'
OUT = ROOT / 'analysis/output'
FIG = ROOT / 'analysis/figures'
RI, RM, RIETI, ROMA = '057', '058', '057059', '058091'

D = pd.read_csv(ROOT / 'New_Query_2026_09_30_10_19_18.csv', dtype={'pro_com_t': str})
M = D[D.provincia.eq('RI')].set_index('pro_com_t')
M['distance_band'] = np.select([M.distanza_corretta_roma_km < 55, M.distanza_corretta_roma_km <= 85], ['<55', '55-85'], default='>85')

# --- 2021 work matrix -------------------------------------------------------------------------
W = pd.read_csv(ROOT / 'matrix_pendoLAVORO_2021.txt', sep='\t', dtype=str)
W['n'] = W.Pendolari.astype(int)
W = W.rename(columns={'Procom_res': 'o', 'Procom_lav': 'd', 'Prov_res': 'po', 'Prov_lav': 'pd'})
res, jobs = W[W.po.eq(RI)], W[W.pd.eq(RI)]
assert set(res.o) == set(M.index)

def by_origin(mask):
    return res[mask].groupby('o').n.sum()
mun = pd.DataFrame({
    'resident_workers': by_origin(res.n > 0),
    'work_in_same_municipality': by_origin(res.o.eq(res.d)),
    'work_other_rieti_municipality': by_origin(res.pd.eq(RI) & res.o.ne(res.d)),
    'work_in_rieti_city': by_origin(res.d.eq(RIETI) & res.o.ne(RIETI)),
    'work_in_rome_province': by_origin(res.pd.eq(RM)),
    'work_in_rome_city': by_origin(res.d.eq(ROMA)),
    'work_elsewhere': by_origin(~res.pd.isin([RI, RM])),
    'jobs_filled_by_commuters': jobs.groupby('d').n.sum(),
    'jobs_filled_from_outside_province': jobs[jobs.po.ne(RI)].groupby('d').n.sum(),
}).fillna(0).astype(int)
mun['share_rome_province'] = mun.work_in_rome_province / mun.resident_workers
mun['share_rieti_city'] = mun.work_in_rieti_city / mun.resident_workers
mun['jobs_per_resident_worker'] = mun.jobs_filled_by_commuters / mun.resident_workers

# --- Road travel times (ISTAT, 1/1/2021 municipalities) ----------------------------------------
with zipfile.ZipFile(SRC / 'Lazio.zip') as z:
    T = pd.read_csv(z.open('R12_RI.csv'), sep=';', decimal=',', usecols=lambda c: c.strip() in {'OR_PROCOM', 'DEST_PROCOM', 'TEP_TOT', 'TTP_TOT', 'KM_TOT'})
T.columns = T.columns.str.strip()
T['o'] = T.OR_PROCOM.astype(str).str.zfill(6)
T['d'] = T.DEST_PROCOM.astype(str).str.zfill(6)
for dest, label in [(ROMA, 'rome_city'), (RIETI, 'rieti_city')]:
    t = T[T.d.eq(dest)].set_index('o')
    mun[f'car_minutes_to_{label}'] = t.TEP_TOT
    mun[f'road_km_to_{label}'] = t.KM_TOT
mun.loc[RIETI, ['car_minutes_to_rieti_city', 'road_km_to_rieti_city']] = 0
assert mun.car_minutes_to_rome_city.notna().all() and mun.car_minutes_to_rieti_city.notna().all()
mun = mun.join(M[['comune', 'popolazione_2025', 'variazione_pct_popolazione_2021_2025', 'distanza_corretta_roma_km', 'distance_band']])
mun.index.name = 'pro_com_t'
mun.sort_values('resident_workers', ascending=False).to_csv(OUT / 'commuting_municipal_2021.csv')

def band_table(g):
    w = g.resident_workers.sum()
    return pd.Series(dict(municipalities=len(g), resident_workers=w,
        share_same_municipality=g.work_in_same_municipality.sum()/w,
        share_rieti_city=g.work_in_rieti_city.sum()/w, share_rome_province=g.work_in_rome_province.sum()/w,
        jobs_per_resident_worker=g.jobs_filled_by_commuters.sum()/w,
        population_change_pct=100*(g.popolazione_2025.sum()/(g.popolazione_2025/(1+g.variazione_pct_popolazione_2021_2025/100)).sum()-1)))
mun['rome_time_band'] = pd.cut(mun.car_minutes_to_rome_city, [0, 90, 105, 999], labels=['<=90 min', '91-105 min', '>105 min'])
mun['rieti_time_band'] = pd.cut(mun.car_minutes_to_rieti_city, [-1, 30, 45, 999], labels=['<=30 min', '31-45 min', '>45 min'])
pd.concat({'distance_band': mun.groupby('distance_band').apply(band_table),
           'rome_car_time_band': mun.groupby('rome_time_band', observed=True).apply(band_table),
           'rieti_car_time_band': mun.groupby('rieti_time_band', observed=True).apply(band_table)}).to_csv(OUT / 'commuting_bands_2021.csv')
corr = pd.DataFrame({
    'pearson_share_rome_vs_population_change': [mun.share_rome_province.corr(mun.variazione_pct_popolazione_2021_2025)],
    'pearson_share_rome_vs_car_minutes_rome': [mun.share_rome_province.corr(mun.car_minutes_to_rome_city)],
    'pearson_share_rome_vs_corrected_distance': [mun.share_rome_province.corr(mun.distanza_corretta_roma_km)],
    'pearson_car_minutes_vs_corrected_distance': [mun.car_minutes_to_rome_city.corr(mun.distanza_corretta_roma_km)]})
corr.T.rename(columns={0: 'value'}).to_csv(OUT / 'commuting_correlations_2021.csv', index_label='statistic')

# --- 2011 census matrix: study and work, with sex, mode and time ------------------------------
COLS = ['rec', 'tres', 'prov', 'com', 'sex', 'motive', 'place', 'provd', 'comd', 'country', 'mode', 'depart', 'duration', 'estimate', 'count']
rows = []
with zipfile.ZipFile(SRC / 'matrici_pendolarismo_2011.zip') as z:
    name = next(n for n in z.namelist() if n.endswith('.txt'))
    for line in io.TextIOWrapper(z.open(name), encoding='latin1'):
        f = line.split()
        if f[2] == RI or f[7] == RI:
            rows.append(f)
C = pd.DataFrame(rows, columns=COLS)
C['o'], C['d'] = C.prov + C.com, C.provd + C.comd
S = C[C.rec.eq('S')].assign(n=lambda x: x['count'].astype(int))        # stratum totals: use 'Numero di individui'
L = C[C.rec.eq('L')].assign(n=lambda x: x.estimate.astype(float))      # mode/time detail: use 'Stima' (households only)
MOTIVE = {'1': 'study', '2': 'work'}

def dest_group(x):
    return np.select([x.place.eq('1'), x.provd.eq(RI), x.provd.eq(RM), x.place.eq('3')],
                     ['same municipality', 'other Rieti municipality', 'Rome province', 'abroad'], default='other Italian province')
S, L = S.assign(dest=dest_group(S)), L.assign(dest=dest_group(L))
s_res = S[S.prov.eq(RI)]

# --- Harmonised flow tables: o, d, po, pd, n for every available year and motive ----------------
# Drop the 2021 study matrix (txt as released, or an esploradati CSV/zip export) into the project root
# or analysis/sources/istat_pendolarismo with 'studio'/'study' and '2021' in its name, then rerun.
STUDY_2021_COLUMNS = None   # e.g. dict(o='Procom_res', d='Procom_stu', n='Pendolari') if autodetection fails

def load_istat_matrix(path):
    """Return (flows with o, d, po, pd, n and any extra dimension columns, extra column names)."""
    for sep in ['\t', ';', ',']:
        raw = pd.read_csv(path, sep=sep, dtype=str, encoding_errors='replace')
        if raw.shape[1] >= 3:
            break
    raw.columns = raw.columns.str.strip()
    m = STUDY_2021_COLUMNS
    if m is None:
        low = {c: c.lower() for c in raw.columns}
        def find(*keys, exclude=()):
            return next((c for c, l in low.items() if all(k in l for k in keys) and not any(e in l for e in exclude)), None)
        m = dict(o=find('procom', 'res') or find('orig') or find('comune', 'resid') or find('ref_area'),
                 d=find('procom', exclude=('res',)) or find('dest') or find('comune', 'stud') or find('comune', 'lav'),
                 n=find('pendolari') or find('obs_value') or find('valore') or find('value'))
    missing = [k for k, v in m.items() if v is None]
    if missing:
        raise ValueError(f'Cannot identify {missing} in {path.name}; columns are {list(raw.columns)}. Set STUDY_2021_COLUMNS.')
    code = lambda x: x.str.extract(r'(\d{6})', expand=False)   # 6-digit PROCOM from '057059', 'IT057059' or '057059 - Rieti'
    out = pd.DataFrame({'o': code(raw[m['o']]), 'd': code(raw[m['d']]), 'n': pd.to_numeric(raw[m['n']], errors='coerce')})
    others = [c for c in raw.columns if c not in m.values()]
    motive = next((c for c in others if raw[c].str.contains('stud', case=False, na=False).any()
                   and raw[c].str.contains('lavor', case=False, na=False).any()), None)
    if motive:                                                  # combined work + study export
        out = out[raw[motive].str.contains('stud', case=False, na=False).values]
    extra = [c for c in others if c != motive and 1 < raw[c].nunique() <= 20]
    for c in extra:                                             # e.g. an age class (6-16 / other), if published
        out[c] = raw.loc[out.index, c].values
    out = out.dropna(subset=['o', 'd', 'n'])
    out['po'], out['pd'] = out.o.str[:3], out.d.str[:3]
    return out, extra

def with_dest(x):
    return x.assign(dest=dest_group(x.assign(place=np.where(x.o.eq(x.d), '1', '2'), provd=x.pd)))

F = {(y, MOTIVE[k]): s_res[s_res.motive.eq(k)].assign(po=lambda x: x.prov, pd=lambda x: x.provd)[['o', 'd', 'po', 'pd', 'n']]
     for y, k in [(2011, '1'), (2011, '2')]}
F[(2021, 'work')] = res[['o', 'd', 'po', 'pd', 'n']]
INBOUND = {(2011, m): S[S.provd.eq(RI) & S.prov.ne(RI) & S.motive.eq(k)].n.sum() for k, m in MOTIVE.items()}
INBOUND[(2021, 'work')] = jobs[jobs.po.ne(RI)].n.sum()
candidates = [f for base in [ROOT, SRC] for f in sorted(base.iterdir())
              if f.suffix.lower() in {'.txt', '.csv', '.zip'} and '2021' in f.name and any(k in f.name.lower() for k in ['stud', 'study'])]
if candidates:
    st, study_extra = load_istat_matrix(candidates[0])
    print(f'2021 study matrix: {candidates[0].name}, {len(st):,} rows, extra dimensions {study_extra}')
    F[(2021, 'study')] = st[st.po.eq(RI)]
    INBOUND[(2021, 'study')] = st[st.pd.eq(RI) & st.po.ne(RI)].n.sum()
    absent = set(M.index) - set(F[(2021, 'study')].o)
    if absent:
        print('warning: no 2021 study flows for', sorted(absent))
    for c in study_extra:
        with_dest(F[(2021, 'study')]).groupby([c, 'dest']).n.sum().unstack().to_csv(OUT / f'study_commuting_2021_by_{c}.csv')
else:
    print('2021 study matrix not found: study results use 2011 only.')

flows = []
for (year, motive), x in F.items():
    for dest, n in with_dest(x).groupby('dest').n.sum().items():
        flows.append(dict(year=year, motive=motive, destination=dest, people=n))
    flows += [dict(year=year, motive=motive, destination='of which Rieti city (from other municipalities)', people=x[x.d.eq(RIETI) & x.o.ne(RIETI)].n.sum()),
              dict(year=year, motive=motive, destination='of which Rome city', people=x[x.d.eq(ROMA)].n.sum()),
              dict(year=year, motive=motive, destination='inbound from outside province', people=INBOUND[(year, motive)])]
flows = pd.DataFrame(flows)
base = ~flows.destination.str.startswith(('of which', 'inbound'))
flows['share_of_resident_commuters'] = flows.people / flows[base].groupby(['year', 'motive']).people.sum().reindex(
    pd.MultiIndex.from_frame(flows[['year', 'motive']])).values
flows.to_csv(OUT / 'commuting_flows_2011_2021.csv', index=False)

PARTS = ['same_municipality', 'rieti_city', 'rome_province']
def municipal_profile(x):
    t = pd.DataFrame({'commuters': x.groupby('o').n.sum(), 'same_municipality': x[x.o.eq(x.d)].groupby('o').n.sum(),
                      'rieti_city': x[x.d.eq(RIETI) & x.o.ne(RIETI)].groupby('o').n.sum(),
                      'rome_province': x[x.pd.eq(RM)].groupby('o').n.sum()})
    return t.reindex(M.index).fillna(0)
for motive in ['work', 'study']:
    years = [y for y in (2011, 2021) if (y, motive) in F]
    t = pd.concat({y: municipal_profile(F[(y, motive)]) for y in years}, axis=1)
    t.columns = [f'{c}_{y}' for y, c in t.columns]
    band = t.join(mun.distance_band).groupby('distance_band').sum()
    for frame in (t, band):
        for y in years:
            for c in PARTS:
                frame[f'share_{c}_{y}'] = frame[f'{c}_{y}'] / frame[f'commuters_{y}']
        if len(years) == 2:
            frame['commuters_change_pct'] = 100 * (frame.commuters_2021 / frame.commuters_2011 - 1)
            for c in PARTS:
                frame[f'share_{c}_change_pts'] = 100 * (frame[f'share_{c}_2021'] - frame[f'share_{c}_2011'])
    t = t.join(mun[['comune', 'car_minutes_to_rome_city', 'car_minutes_to_rieti_city', 'distance_band', 'variazione_pct_popolazione_2021_2025']])
    t.index.name = 'pro_com_t'
    t.sort_values(f'commuters_{years[-1]}', ascending=False).to_csv(OUT / f'{motive}_commuting_municipal_2011_2021.csv')
    band.to_csv(OUT / f'{motive}_commuting_bands_2011_2021.csv')

MODE = {'01': 'train', '02': 'tram', '03': 'metro', '04': 'urban bus', '05': 'coach / extra-urban bus', '06': 'company or school bus',
        '07': 'car, driver', '08': 'car, passenger', '09': 'motorcycle', '10': 'bicycle', '11': 'other', '12': 'on foot'}
DUR = {'1': '<=15 min', '2': '16-30 min', '3': '31-60 min', '4': '>60 min'}
DEP = {'1': 'before 7:15', '2': '7:15-8:14', '3': '8:15-9:14', '4': 'after 9:14'}
l_res = L[L.prov.eq(RI)]
detail = []
for var, lab in [('mode', MODE), ('duration', DUR), ('depart', DEP)]:
    p = l_res.groupby(['motive', 'dest', var]).n.sum()
    p = (p / p.groupby(level=[0, 1]).transform('sum')).rename('share').reset_index()
    detail.append(p.assign(variable=var, category=p[var].map(lab), motive=p.motive.map(MOTIVE)).drop(columns=var))
pd.concat(detail).to_csv(OUT / 'commuting_mode_time_2011.csv', index=False)
sx = s_res[s_res.motive.eq('2')].assign(sex=lambda x: x.sex.map({'1': 'men', '2': 'women'}))
sex = sx.groupby('sex').apply(lambda g: pd.Series(dict(resident_workers=g.n.sum(),
        share_outside_municipality=g[g.place.ne('1')].n.sum()/g.n.sum(), share_rome_province=g[g.provd.eq(RM)].n.sum()/g.n.sum())))
lw = l_res[l_res.motive.eq('2')].assign(sex=lambda x: x.sex.map({'1': 'men', '2': 'women'}))
sex['share_over_60_min'] = lw.groupby('sex').apply(lambda g: g[g.duration.eq('4')].n.sum()/g.n.sum())
sex.to_csv(OUT / 'commuting_sex_2011.csv')

# --- Figure -------------------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4), gridspec_kw={'width_ratios': [1.15, 1]})
ax = axes[0]
sc = ax.scatter(mun.car_minutes_to_rome_city, 100*mun.share_rome_province, s=6+4*np.sqrt(mun.resident_workers),
                c=mun.variazione_pct_popolazione_2021_2025, cmap='RdYlBu', vmin=-8, vmax=8, edgecolor='#555', lw=.4)
for code, off in [('057027', (8, 2)), ('057064', (7, 3)), ('057029', (-8, 8)), ('057059', (-14, -16)), ('057053', (8, -2)), ('057016', (6, 6))]:
    r = mun.loc[code]
    ax.annotate(r.comune, (r.car_minutes_to_rome_city, 100*r.share_rome_province), xytext=off, textcoords='offset points', fontsize=8.5)
ax.set_xlabel('Car travel time to Rome city, minutes (ISTAT road matrix)')
ax.set_ylabel('Resident workers employed in Rome province, %')
ax.set_title('Rome is a daily labour market for the Sabina', loc='left', fontsize=11.5)
fig.colorbar(sc, ax=ax, shrink=.75, label='Population change 2021-25, % (clipped ±8)')
ax = axes[1]
order = ['same municipality', 'other Rieti municipality', 'Rome province', 'other Italian province']
colors = ['#406c83', '#8fb0c0', '#bd633b', '#d5a348']
bars = {f'{m.capitalize()} {y}': flows[flows.year.eq(y) & flows.motive.eq(m)]
        for y, m in sorted(F, key=lambda k: (k[1] == 'study', -k[0]))}
for i, (lab, f) in enumerate(bars.items()):
    v = f.set_index('destination').people.reindex(order).fillna(0)
    v = 100 * v / v.sum()
    left = 0
    for k, c in zip(order, colors):
        ax.barh(i, v[k], left=left, color=c, label=k if i == 0 else None)
        if v[k] > 6: ax.text(left + v[k]/2, i, f'{v[k]:.0f}%', ha='center', va='center', color='white', fontsize=9.5)
        left += v[k]
ax.set_yticks(range(len(bars)), list(bars)); ax.invert_yaxis(); ax.set_xlim(0, 100)
ax.set_xlabel('Share of daily commuters resident in Rieti province, %')
ax.set_title('Where residents go to work and study', loc='left', fontsize=11.5)
ax.legend(ncol=2, fontsize=8.5, frameon=False, loc='upper center', bbox_to_anchor=(.5, -.18))
fig.text(.02, .015, 'Source: ISTAT work commuting matrix 2021 (model-based); ISTAT census commuting matrix 2011; ISTAT inter-municipal road matrix. '
         '2011 and 2021 use different definitions.', fontsize=8, color='#555555')
fig.tight_layout(rect=(0, .04, 1, 1))
fig.savefig(FIG / '05_commuting.png', dpi=200, bbox_inches='tight')
fig.savefig(FIG / '05_commuting.svg', bbox_inches='tight')

print(flows.to_string())
print(pd.read_csv(OUT / 'commuting_bands_2021.csv').round(3).to_string())
print(corr.round(3).T)
print(sex.round(3))
