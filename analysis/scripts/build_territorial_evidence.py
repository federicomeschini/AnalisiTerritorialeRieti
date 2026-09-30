"""Rebuild territorial tables and slide figures. Run from any working directory.

Dependencies: pandas, numpy, pyarrow, matplotlib, openpyxl. Inputs are read-only.
Official observations below are transcribed from the cited PDF tables; vintage
and page references are deliberately retained rather than silently spliced.
"""
from pathlib import Path
import json
import hashlib
import io
import zipfile
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/output'
FIG = ROOT / 'analysis/figures'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
D = pd.read_csv(ROOT / 'New_Query_2026_09_30_10_19_18.csv', dtype={'pro_com_t': str})
E = pd.read_csv(ROOT / 'municipality_integrated_energy_risk_latest_inputs.csv', dtype={'municipality_code': str})
assert D.pro_com_t.is_unique and E.municipality_code.is_unique
D['age65_count'] = D.popolazione_2025 * D.pct_65plus_2025 / 100
D['age15_64_count'] = D.popolazione_2025 * D.pct_15_64_2025 / 100
D['age0_14_count'] = D.popolazione_2025 - D.age65_count - D.age15_64_count
assert np.allclose(D.indice_vecchiaia_2025, 100 * D.age65_count / D.age0_14_count)
assert np.allclose(D.variazione_popolazione_2021_2025, D.popolazione_2025 - D.popolazione_2021)

def aggregate(g):
    pop = g.popolazione_2025.sum()
    return pd.Series(dict(municipalities=len(g), population_start2021=g.popolazione_2021.sum(),
        population_start2025=pop, change_people=pop-g.popolazione_2021.sum(),
        change_pct=100*(pop/g.popolazione_2021.sum()-1), area_km2=g.area_kmq.sum(),
        density=pop/g.area_kmq.sum(), age65_pct=100*g.age65_count.sum()/pop,
        age0_14_pct=100*g.age0_14_count.sum()/pop,
        ageing_ratio=100*g.age65_count.sum()/g.age0_14_count.sum(),
        dependency_ratio=100*(g.age65_count.sum()+g.age0_14_count.sum())/g.age15_64_count.sum(),
        mean_age=np.average(g.eta_media_2025, weights=g.popolazione_2025),
        incorrect_pop_weighted_ageing=np.average(g.indice_vecchiaia_2025, weights=g.popolazione_2025),
        municipalities_declining=int((g.popolazione_2025<g.popolazione_2021).sum())))

peers = pd.DataFrame({k:aggregate(g) for k,g in D.groupby('provincia')}).T
peers.index.name = 'province'
peers.to_csv(OUT/'demographic_peers.csv')
R = D[D.provincia.eq('RI')].copy()
R['distance_band'] = np.select([R.distanza_corretta_roma_km < 55, R.distanza_corretta_roma_km <= 85], ['<55','55-85'], default='>85')
zones = pd.DataFrame({k:aggregate(g) for k,g in R.groupby('distance_band')}).T
zones.to_csv(OUT/'distance_bands.csv', index_label='band')
R['change_pct_recomputed'] = 100*(R.popolazione_2025/R.popolazione_2021-1)
R.to_csv(OUT/'rieti_municipal_evidence.csv', index=False)
sens=[]
for threshold in [50,55,60,80,85,90]:
    for side,mask in [('below',R.distanza_corretta_roma_km < threshold),('at_or_above',R.distanza_corretta_roma_km >= threshold)]:
        sens.append(dict(threshold=threshold,side=side,**aggregate(R[mask]).to_dict()))
pd.DataFrame(sens).to_csv(OUT/'distance_threshold_sensitivity.csv',index=False)

er=E[E.province_code.eq('RI')].copy()
joined=R.merge(er,left_on='pro_com_t',right_on='municipality_code',how='left',validate='one_to_one')
assert joined.municipal_total_employees.notna().all()
energy=[]
for label,g in [('Rieti',er),('Lazio',E[E.region_code.astype(int).eq(12)])]:
    w=g.municipal_total_employees
    energy.append(dict(area=label,municipalities=len(g),employees=w.sum(),
        mean_municipal_percentile=np.average(g.integrated_energy_risk_percentile_0_100,weights=w),
        raw=np.average(g.iee_raw,weights=w),other=np.average(g.iee_other_energy_raw,weights=w),
        adjusted=np.average(g.iee_split_grid_price_calibrated_adj,weights=w),
        high_risk_employees=w[g.integrated_energy_risk_quintile.ge(4)].sum(),
        high_risk_employee_pct=100*w[g.integrated_energy_risk_quintile.ge(4)].sum()/w.sum()))
pd.DataFrame(energy).to_csv(OUT/'energy_summary.csv',index=False)
er.sort_values('municipal_total_employees',ascending=False).to_csv(OUT/'energy_municipalities.csv',index=False)

# CCIAA fifth report, PDF pp.44 and 54: one publication vintage for 2024-25.
cciaa='https://www.rivt.camcom.it/files/quintorapportoeconomiaaltolazio-_11821.pdf'
labour=pd.DataFrame([
    ['Rieti',58.4,61.8,62.7,60.8,60276,59024],
    ['Viterbo',58.4,58.0,63.9,62.3,127213,125874],
    ['Frosinone',56.2,55.5,57.8,59.5,175161,175975],
    ['Lazio',61.8,63.2,64.0,64.2,2415092,2430210],
    ['Italy',60.1,61.5,62.2,62.5,23932264,24117234]],
    columns=['area','employment_rate_2022','employment_rate_2023','employment_rate_2024','employment_rate_2025','employed_2024','employed_2025'])
labour['source_url']=cciaa
labour['pdf_page']=44
labour.to_csv(OUT/'official_labour.csv',index=False)
exports=pd.DataFrame([
    ['Rieti',591711719,878424596],['Viterbo',531702348,582318982],
    ['Lazio',32834549218,35993774218],['Italy',622606972878,643153265742]],columns=['area','eur_2024','eur_2025'])
exports['change_pct']=100*(exports.eur_2025/exports.eur_2024-1)
exports['source_url']=cciaa
exports['pdf_page']=54
exports.to_csv(OUT/'official_exports_2024_2025.csv',index=False)
sectors=pd.DataFrame([
    ['Pharmaceuticals','C21__I',405767820,703601579,387259971],
    ['Machinery','C28__I',113730867,112630584,88704507],
    ['Electronics','C26__I',36183551,31485981,23659790],
    ['Food beverages tobacco','C10-12__I',10460157,6556014,9991790],
    ['Agriculture forestry fishing','A01__A',34174,40123,71898]],
    columns=['sector','sam_code','eur_2024','eur_2025','eur_2022_older_vintage'])
sectors['source_2024_2025']=cciaa+'#page=59'
sectors['source_2022']='https://www.rivt.camcom.it/files/terzorapportoeconomiaaltolazio-_9755.pdf#page=60'
sectors['change_pct']=100*(sectors.eur_2025/sectors.eur_2024-1)
S=pd.read_csv(ROOT/'SAM/output/rieti_sectoral_indicators_2022.csv')
sectors=sectors.merge(S[['nace_aggregate','sales_ROW_exports_mEUR']],left_on='sam_code',right_on='nace_aggregate',validate='one_to_one')
sectors.to_csv(OUT/'sam_official_export_crosscheck.csv',index=False)

# Read the archived Chamber-hosted spreadsheets directly, retaining source vintage.
with zipfile.ZipFile(ROOT/'analysis/sources/tagliacarne_2024_download.zip') as archive:
    name=next(n for n in archive.namelist() if 'procapite e piazzamento per provincia' in n)
    raw=pd.read_excel(io.BytesIO(archive.read(name)),header=None)
    va=raw.iloc[3:].copy()
    va.columns=['area','year','VA_per_resident_eur','rank']
    va['area']=va.area.astype(str).str.strip()
    va=va[va.area.isin(['Rieti','Viterbo',"L'Aquila",'Terni','Frosinone','Lazio','Italia'])].copy()
    va['source_url']='https://www.chpe.camcom.it/output_allegato.php?id=1425923'
    va['archive_member']=name
    va.to_csv(OUT/'official_value_added_peers.csv',index=False)
    name=next(n for n in archive.namelist() if 'branca di attivit economica anni' in n)
    raw=pd.read_excel(io.BytesIO(archive.read(name)),header=None)
    rows=raw[raw[0].astype(str).str.strip().isin(['Rieti','Italia'])].copy()
    rows.columns=['area','year','agriculture','industry_ex_construction','construction','trade_transport_accommodation_information','finance_realestate_professional_support','other_services','total_mEUR']
    rows['source_url']='https://www.chpe.camcom.it/output_allegato.php?id=1425923'
    rows.to_csv(OUT/'official_value_added_2023_2024.csv',index=False)
with zipfile.ZipFile(ROOT/'analysis/sources/tagliacarne_2022_download.zip') as archive:
    name=next(n for n in archive.namelist() if 'branca' in n and '2022' in n)
    raw=pd.read_excel(io.BytesIO(archive.read(name)),header=None)
    rows=raw[raw[0].astype(str).str.strip().eq('Rieti')].copy()
    rows.columns=['area','agriculture','industry_ex_construction','construction','trade_transport_accommodation_information','other_services','total_mEUR']
    rows['year']=2022
    rows['source_url']='https://www.chpe.camcom.it/output_allegato.php?id=745843'
    rows['archive_member']=name
    rows.to_csv(OUT/'official_value_added_2022_older_vintage.csv',index=False)

# Re-read the supplied SAM columns; check balance from rows in all columns.
p=pq.ParquetFile(ROOT/'SAM/mrsam_euita_2022_3oe_wide.parquet')
names=p.schema_arrow.names
labels=p.read(columns=['row_label']).to_pandas().row_label
cols=[n for n in names if n.startswith('ITI42__')]
m=p.read(columns=['row_label',*cols]).to_pandas().set_index('row_label').fillna(0)
position=[int(np.flatnonzero(labels.eq(c))[0]) for c in cols]
row_sums=np.zeros(len(cols))
for i in range(1,len(names),300):
    row_sums+=p.read(columns=names[i:i+300]).to_pandas().iloc[position].fillna(0).sum(axis=1).to_numpy()
column_sums=m.sum(axis=0).to_numpy()
balance_error = abs(row_sums-column_sums)
pd.DataFrame({'account':cols,'column_output':column_sums,'row_receipts':row_sums,'difference':row_sums-column_sums}).to_csv(OUT/'sam_balance_check.csv',index=False)
print('SAM maximum balance error:', balance_error.max())
assert np.max(balance_error / column_sums) < 1e-6, 'SAM imbalance exceeds rounding tolerance'
saved=S.set_index('nace_aggregate').loc[[c.split('__',1)[1] for c in cols],'gross_output_mEUR'].to_numpy()
assert np.allclose(saved,column_sums,atol=1e-5)

pv=pd.DataFrame([['RI',6163,53,49.2],['TR',7643,175,181.9],['FR',12977,282,274.4],['VT',15836,1580,1378.5]],columns=['province','plants_2024','MW_2024','GWh_2024'])
pv['population_start2025']=pv.province.map(peers.population_start2025)
pv['kW_per_person']=1000*pv.MW_2024/pv.population_start2025
pv['source']='https://www.gse.it/documenti_site/Documenti%20GSE/Rapporti%20statistici/Solare%20Fotovoltaico%20-%20Rapporto%20Statistico%202024.pdf'
pv.to_csv(OUT/'official_pv_peers.csv',index=False)
scenarios=pd.DataFrame([(mw,yield_mwh,mw*yield_mwh/1000) for mw in [5,10,20] for yield_mwh in [1000,1400]],columns=['additional_MW_assumption','annual_MWh_per_MW_assumption','additional_GWh'])
scenarios['share_2024_PV_pct']=100*scenarios.additional_GWh/49.2
scenarios['share_2024_renewable_generation_pct']=100*scenarios.additional_GWh/290.5
scenarios.to_csv(OUT/'pv_illustrative_scenarios.csv',index=False)

audit=dict(dataset_rows=len(D),province_counts=D.provincia.value_counts().to_dict(),energy_rows=len(E),
    rieti_join_rows=len(joined),sam_rows=p.metadata.num_rows,sam_columns=len(names)-1,
    sam_provinces=len({c.split('__')[0] for c in names[1:] if not c.startswith('IT__')}),
    sam_sector_union=len({c.split('__',1)[1] for c in names[1:] if not c.startswith('IT__')}),
    sam_rieti_sectors=len(cols),sam_max_balance_error=float(abs(row_sums-column_sums).max()),
    sam_gross_output=float(column_sums.sum()),sam_local_inputs=float(m.loc[cols].sum().sum()),
    sam_metadata_keys=[k.decode() for k in (p.schema_arrow.metadata or {})],
    energy_coverage_unique_values=er.filter(regex='coverage|lambda').nunique().to_dict(),
    energy_coverage_first_values=er.filter(regex='coverage|lambda').iloc[0].to_dict(),
    missing_by_column=D.isna().sum().loc[lambda x:x.gt(0)].to_dict(),
    rieti_small_municipalities=int(R.popolazione_2025.lt(1000).sum()),
    rieti_small_municipalities_population=int(R.loc[R.popolazione_2025.lt(1000),'popolazione_2025'].sum()),
    rieti_migration_field_sum=int(R.saldo_migratorio_2025.sum()))
(OUT/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
manifest=[]
for file in [ROOT/'New_Query_2026_09_30_10_19_18.csv',ROOT/'municipality_integrated_energy_risk_latest_inputs.csv',ROOT/'SAM/mrsam_euita_2022_3oe_wide.parquet',*sorted((ROOT/'analysis/sources').glob('*.pdf')),*sorted((ROOT/'analysis/sources').glob('*.zip'))]:
    digest=hashlib.sha256()
    with file.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): digest.update(chunk)
    manifest.append(dict(path=str(file.relative_to(ROOT)),bytes=file.stat().st_size,sha256=digest.hexdigest()))
pd.DataFrame(manifest).to_csv(OUT/'input_manifest.csv',index=False)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name,foot):
    fig.text(.02,.015,foot,fontsize=8,color='#555555')
    fig.tight_layout(rect=(0,.065,1,.96))
    fig.savefig(FIG/(name+'.png'),dpi=200,bbox_inches='tight')
    fig.savefig(FIG/(name+'.svg'),bbox_inches='tight')
    plt.close(fig)

fig,ax=plt.subplots(figsize=(10,5.5))
q=peers.loc[['RI','AQ','TR','VT','FR']].sort_values('change_pct')
ax.barh(q.index,q.change_pct,color=['#bd633b' if k=='RI' else '#406c83' for k in q.index])
ax.set_yticks(range(len(q)),[{'RI':'Rieti','AQ':"L’Aquila",'TR':'Terni','VT':'Viterbo','FR':'Frosinone'}[k] for k in q.index])
ax.axvline(0,color='#555',lw=.7)
for i,v in enumerate(q.change_pct): ax.text(v+.025,i,f'{v:.2f}%',va='center',ha='left',color='white',fontsize=10)
ax.set(title='Population decline is shared; Rieti is not the fastest-shrinking peer',xlabel='Change between dataset start-2021 and start-2025 populations (%)')
save(fig,'01_demographic_peers','Source: supplied municipal dataset; provincial totals. RI endpoints match ISTAT end-2020/end-2024.')

fig,axes=plt.subplots(1,2,figsize=(12,5.8),gridspec_kw={'width_ratios':[1.3,1]})
s=axes[0].scatter(R.longitude,R.latitude,c=R.change_pct_recomputed,cmap='RdYlBu',vmin=-10,vmax=10,s=15+R.popolazione_2025/100,edgecolor='white',lw=.5)
for name in ['Rieti','Fara in Sabina','Borgorose','Amatrice','Leonessa']:
    row=R[R.comune.eq(name)].iloc[0]
    offset=(-6,6) if name=='Borgorose' else (4,6)
    axes[0].annotate(name,(row.longitude,row.latitude),xytext=offset,textcoords='offset points',fontsize=8,ha='right' if name=='Borgorose' else 'left')
axes[0].set(xlabel='Longitude',ylabel='Latitude',title='Municipal points: population change (%)')
axes[0].set_aspect(1/np.cos(np.deg2rad(42.3)))
fig.colorbar(s,ax=axes[0],shrink=.65,label='Change (%) · colour clipped at ±10')
z=zones.loc[['<55','55-85','>85']]
axes[1].bar(z.index,z.change_pct,color=['#406c83','#bd633b','#994d38'])
axes[1].axhline(0,color='#555',lw=.7)
axes[1].set(title='Exploratory distance bands',xlabel='Corrected distance to Rome (km)',ylabel='Population change (%)')
save(fig,'02_internal_geography','Source: supplied dataset, start-2021 to start-2025. Size reflects population; points and bands are not official functional areas.')

fig,axes=plt.subplots(1,2,figsize=(11,5.5))
for _,row in labour[labour.area.isin(['Rieti','Viterbo','Italy','Lazio'])].iterrows():
    axes[0].plot([2022,2023,2024,2025],[row[f'employment_rate_{y}'] for y in range(2022,2026)],marker='o',label=row.area)
axes[0].set(title='Resident employment rate, age 15–64',ylabel='%',xticks=[2022,2023,2024,2025]); axes[0].legend(frameon=False)
total=np.array([591711719,878424596])/1e6
pharma=np.array([405767820,703601579])/1e6
axes[1].bar(['2024','2025'],pharma,label='Pharmaceuticals',color='#406c83')
axes[1].bar(['2024','2025'],total-pharma,bottom=pharma,label='All other goods',color='#bd633b')
axes[1].set(title='Export growth is concentrated',ylabel='Goods exports (€m)');axes[1].legend(frameon=False)
save(fig,'03_exports_and_employment','Source: CCIAA fifth report (2025), PDF pp.44,54,59; ISTAT-based tables, accessed 30 September 2026.')

fig,axes=plt.subplots(1,2,figsize=(11,5.5))
bars=axes[0].bar(['Hydro','Solar PV','Bioenergy'],[220.7,49.2,20.6],color=['#406c83','#d5a348','#718668'])
axes[0].bar_label(bars,padding=3,fmt='%.1f')
axes[0].set(title='Hydro dominates renewable generation',ylabel='Gross renewable generation, 2024 (GWh)',ylim=(0,250))
bars=axes[1].bar(['Rieti','Terni','Frosinone','Viterbo'],pv.kW_per_person,color=['#bd633b','#406c83','#406c83','#406c83'])
axes[1].bar_label(bars,padding=3,fmt='%.2f')
axes[1].set(title='Solar deployment varies across peers',ylabel='Installed PV kW per resident, end-2024',ylim=(0,5.8))
save(fig,'04_energy_context','Sources: Terna regional statistics 2024, p.151; GSE solar report 2024, p.15; supplied population totals.')
print(f'Validated {len(D)} municipal rows; {len(R)} Rieti rows joined to energy; {len(cols)} SAM sectors checked.')
print('Demographic identities and SAM balance within rounding tolerance: passed.')
print('Tables, source hashes and four PNG/SVG figures written to analysis/.')
