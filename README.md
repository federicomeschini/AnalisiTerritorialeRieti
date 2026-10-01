# Analisi territoriale Rieti

Territorial analysis of the Province of Rieti (Lazio) for policy makers: demography, commuting, labour market, exports, skills and graduates, and energy.

- Report (English): [analisi_territoriale_rieti_per_policy_makers.md](analisi_territoriale_rieti_per_policy_makers.md)
- Report (Italian): [analisi_territoriale_rieti_per_policy_makers_it.md](analisi_territoriale_rieti_per_policy_makers_it.md)
- Sources, checks and caveats: [analysis/validation_and_sources.md](analysis/validation_and_sources.md)
- SAM technical note: [SAM/analisi_sam_rieti_2022.md](SAM/analisi_sam_rieti_2022.md)

## Web site

The policy-maker site (Italian, OpenEconomics brand) is served by GitHub Pages from the repository root: `index.html` plus one page per topic (`persone.html`, `economia.html`, `energia.html`, `europa.html`, `proposte.html`) and shared files in `assets/`. Rebuild everything with `python web/build_site.py`; content blocks, styles and charts live in `web/src/`. The build needs the OpenEconomics front-end brand kit zip (set `OE_BRAND_ZIP` if it is not on the Desktop).

## Rebuilding the tables and figures

```
python analysis/scripts/build_territorial_evidence.py
python analysis/scripts/build_commuting_evidence.py
python analysis/scripts/build_skills_evidence.py
python analysis/scripts/fetch_istat_study_matrix.py   # 2021 study-commuting matrix, when esploradati.istat.it is online
```

Dependencies: pandas, numpy, pyarrow, matplotlib, openpyxl, pypdf.

## Data not included

Two internal inputs are not published in this repository:

- `SAM/mrsam_euita_2022_3oe_wide.parquet` (multi-regional social accounting matrix, 2022)
- `municipality_integrated_energy_risk_latest_inputs.csv` (municipal energy-risk index)

`build_territorial_evidence.py` and `SAM/scripts/analyze_rieti_mrsam.py` need them to run; the derived tables they produced are included in `analysis/output` and `SAM/output`. The commuting and skills scripts run from the public sources in `analysis/sources`.
