# Validation and source register

Checked 30 September 2026. This appendix accompanies the [revised territorial analysis](../analisi_territoriale_rieti_per_policy_makers.md). Original data files have not been edited. Recalculated values, official extracts, source hashes and figures are under `analysis/`.

## Overall verdict

**The inputs are usable selectively, not uniformly validated.** Demographic totals and reconstructed age ratios support the territorial narrative. SAM arithmetic is internally coherent to a small numerical tolerance, but economic accounting consistency does not establish the accuracy of provincial allocations. Official same-year exports contradict several of the previous sector claims. Energy generation needs a separate official source because the index is neither a generation inventory nor a resource-potential assessment.

## 1. Municipal dataset audit

Source: `New_Query_2026_09_30_10_19_18.csv`, 497 unique municipality codes. No original data dictionary or extraction query was supplied.

| Field / previous claim | Verification | Decision |
|---|---|---|
| Rieti municipality coverage | 73 unique codes; full one-to-one match with Rieti energy rows. | Use. Other provinces remain dataset comparators, not a national sample. |
| Population labelled 2025 | Rieti total exactly matches ISTAT end-2024; Lazio provincial totals in the file also match the focus report. | Label start-2025 / end-2024, not end-2025. |
| Population labelled 2021 | Rieti total matches ISTAT end-2020, rather than end-2021. FR, LT and VT also match end-2020. | The four-year change is start-2021 to start-2025. Do not splice it into a calendar-year series without correcting dates. |
| Ageing index | Municipal ratios reproduce from age shares. Correct provincial aggregation agrees with ISTAT after rounding. | Replace the old weighted-ratio calculation. |
| Mean age | Population-weighted dataset mean is 48.23; ISTAT reports 48.7. | Definition unresolved; do not present the dataset mean as an official age estimate. A half-year age convention is a possible explanation, not verified metadata. |
| Migration field | Municipal sum does not reconcile to the official demographic balance. | Use the official natural/internal/international/statistical components instead. |
| Employment and unemployment | Municipal rate denominators, source universe and estimation method are absent. The old Rieti employment average happens to round to the published 2023 rate; its unemployment average does not. | Use published provincial series; numerical agreement of one average is not validation of the method. |
| Mean income | Population weights are not taxpayer weights. Income definition and tax-year convention are absent. | Exclude the provincial ranking; do not call it GDP, wages or household disposable income. |
| Firms per 1,000 residents | Reference population, register coverage, active/registered status and firm/local-unit distinction are unknown. | Exclude the headline comparative ranking. Obtain counts and consistent denominators. |
| Municipal finance | 92 of 497 education-expenditure values and 260 culture values are missing; cash/accrual, consolidation and accounting coverage are undocumented. | Do not infer service quality, fiscal weakness or investment effort from these columns. Missing is not zero. |
| Land-use percentages | Examples include 100% urban / 0% nature for Paganico Sabino, and very low nature values for Amatrice and Accumoli. Agriculture and nature appear overlapping in many rows. | Quarantine for land allocation and renewable potential. Resolve category definitions, denominator, units and geometry join. Do not manufacture a corrected land-cover series. |
| Corrected distance to Rome | Explicit altitude penalty is embedded; no road network or service timetable is supplied. | Exploratory proxy only; not travel time, official functional areas or SNAI classification. |

Population and age references: [ISTAT Lazio 2024, tables 1, 2 and 6](https://www.istat.it/wp-content/uploads/2026/04/12_Focus_Censimento_Popolazione_Lazio_2024.pdf); [ISTAT Lazio 2021, table 1](https://www.istat.it/wp-content/uploads/2023/09/Lazio-Focus2021-Censimantopermanente.pdf). Cross-checks establish consistency at the stated aggregate level; they do not independently verify every municipal row.

### Aggregation rules

- Population, area and reconstructed age-group counts: sum across municipalities.
- Population growth: `100 × (sum(P_end) / sum(P_start) − 1)`, not average municipal percentage growth.
- Density: total residents / total km².
- Older population: `P × pct_65plus / 100`; working-age population: `P × pct_15_64 / 100`; children aged 0–14: the residual.
- Ageing index: `100 × sum(65+) / sum(0–14)`. Structural dependency: `100 × sum(0–14 and 65+) / sum(15–64)`.
- The original `pct_0_2` field is not the denominator of the ageing index.
- A provincial employment rate needs employed residents and the corresponding working-age population. Unemployment needs unemployed people and the labour force. A population-weighted average of the supplied rates is not an acceptable substitute.

The distance bands use `<55`, `55–85 inclusive`, and `>85`. Sensitivity checks use 50/55/60 km and 80/85/90 km splits. The growth/decline contrast is robust to these alternatives; neither the thresholds nor the resulting groups acquire official planning status.

## 2. SAM validation

The actual parquet contains **6,576 accounts: 6,569 production accounts across 107 territorial codes and seven national accounts**. Rieti has 60 production accounts; the matrix-wide sector union has 63 aggregates. The previous note incorrectly stated 108 territories.

The reproducible check rereads Rieti columns, totals the corresponding rows across the full matrix and compares the saved sector output CSV. The maximum row/column difference is approximately **0.000257 million euros**, or **0.000068%** of the relevant output. Total Rieti row receipts exceed column expenditure by about €1,229 under the assumed units. These are very small numerical residuals, not an economically material imbalance. Results are in [sam_balance_check.csv](output/sam_balance_check.csv).

The parquet metadata contains pandas schema information but no release methodology, monetary-unit statement, price-base explanation or allocation documentation. The million-euro convention is inherited from the original script and supported by a plausible aggregate scale; it remains a convention to confirm with the data producer.

### External consistency

The [same-year export comparison](output/sam_official_export_crosscheck.csv) contrasts model industry sales with Chamber/ISTAT product-based trade. Matching concepts perfectly is not possible from the supplied documentation. Nevertheless, food and primary-agriculture differences are too large to ignore, while machinery is numerically close. The conclusions are **sector-specific**, not “the SAM is validated” or “the SAM is useless.”

For value added, the [2022 Chamber-hosted tables](https://www.chpe.camcom.it/output_allegato.php?id=745843) supply a same-year scale check and broad sector comparison. The SAM aggregate is reasonably close in scale but not equal; construction and agriculture allocations differ materially. These are comparisons to an archived statistical-estimate vintage, not certification against a fully reconciled current national-accounts release.

### Interpretation to retain

Use the SAM to formulate hypotheses about scale, specialisation and supply-chain roles. Its local input share is an **unverified allocation result**, not direct procurement evidence. Sector scores are analyst-designed screens; they are not objective investment rankings or growth forecasts.

National multipliers use the 63-sector aggregate technology. They do not calculate the full interregional response to demand originating specifically in a Rieti sector. The Rieti-only inverse omits paths leaving and re-entering the province. Neither coefficient measures net fiscal returns, opportunity costs or distributional benefits.

National household, government and capital-formation accounts must not be mapped automatically to spending located in Rieti. No employment multiplier has been validated. Original numerical outputs remain unchanged.

## 3. Energy index validation

The supplied file contains 7,890 unique municipality codes and a single reference-year field, 2022. It has 73 Rieti rows and 378 Lazio rows. The filename's “latest inputs” does not establish that every underlying series shares that year; no component source-vintage dictionary was supplied.

Employee weights describe the workplace employment universe in this file. High-risk exposure is the sum of employees in municipalities whose quintile is 4 or 5, divided by total employees. It is not a count of individually audited firms or workers. The weighted average of municipal percentiles is not a reranked provincial percentile.

All Rieti solar/wind coverage variables are spatially constant. They cannot support a municipal map of generation adequacy, physical potential or grid constraints. The non-electric component dominates the raw score; renewable electricity interventions cannot simply be translated into an equal reduction of the whole index.

Observed generation is instead taken from Terna and GSE. Generation, annual consumption, installed capacity, self-consumption and energy bills have different denominators. The PV scenarios are explicit arithmetic assumptions, not an engineering feasibility result. No costs, savings, emissions reductions or investable site capacity are claimed.

## 4. Official publications also need vintage and table checks

The analysis uses one consistent fifth-report vintage for the employment series and the 2024–25 export comparison. Earlier trade publications contain different values for overlapping years. Those should not be silently joined to create a long series. The 2022 comparison is explicitly labelled as an older vintage and used for model validation only.

Some institutional publications contain apparent errors. For example, the regional DEFR's 2023 employment table reproduces activity-rate values under an employment heading; the fifth Chamber report's 2021 employment-rate entries also conflict with the surrounding series. Neither is used. The retained labour trend starts in 2022 and the selected export sector columns were checked visually against the PDFs.

The early local Chamber news release and the currently downloadable 2023–24 value-added tables disagree materially. The revised brief uses the latter for the prosperity benchmark and nominal within-release change. **No real growth or revision bridge is inferred from differences across releases.** Archive filenames identify the reporting period, not necessarily the download/publication year.

References for these checks: [CCIAA fifth report](https://www.rivt.camcom.it/files/quintorapportoeconomiaaltolazio-_11821.pdf), [Regione Lazio DEFR 2026–28, table S1.23](https://www.regione.lazio.it/sites/default/files/2026-01/DEFR-2026-2028.pdf), [earlier Chamber release](https://www.rivt.camcom.it/it/news/giornata-delleconomia-rieti_2505.htm), [Chamber statistical download page](https://www.chpe.camcom.it/pagina182570_statistiche-su-valore-aggiunto.html/).

## 5. Source register and reproducibility

All sources accessed 30 September 2026. PDF page numbers below count the cover as page 1, even when the printed page number differs.

| Source / period | Location used | Saved evidence / use |
|---|---|---|
| [ISTAT Lazio Census 2024](https://www.istat.it/wp-content/uploads/2026/04/12_Focus_Censimento_Popolazione_Lazio_2024.pdf) | Tables 1, 2, 6; PDF pp.2, 5 | Population, demographic balance and age-index benchmark. Linked original. |
| [ISTAT Lazio Census 2021](https://www.istat.it/wp-content/uploads/2023/09/Lazio-Focus2021-Censimantopermanente.pdf) | Table 1; PDF p.2 | End-2020 / end-2021 distinction and 2011 benchmark. Linked original. |
| [CCIAA fifth report, 2025](https://www.rivt.camcom.it/files/quintorapportoeconomiaaltolazio-_11821.pdf) | PDF pp.44, 54, 59 | `sources/cciaa_rapporto_2025.pdf`; labour and exports; current trade vintage. |
| [ISTAT work-commuting matrix 2021](https://www.istat.it/notizia/matrice-di-pendolarismo-per-lavoro/), [methodology](https://www.istat.it/wp-content/uploads/2025/10/Nota-metodologica-Pendolarismo-per-lavoro-2021.pdf) | Full release: origin, destination, count | `matrix_pendoLAVORO_2021.txt`. Model-based from administrative workplace records; at least 3 days a week; no sex, mode or time. Workplaces can be an employer's address, so long-distance flows need care. |
| [ISTAT census commuting matrix 2011](https://www.istat.it/notizia/matrici-di-contiguita-distanza-e-pendolarismo/) | Record types S (counts) and L (mode, time) | `sources/istat_pendolarismo/matrici_pendolarismo_2011.zip`. Census declarations of daily trips; study includes nursery; not strictly comparable with 2021. |
| [ISTAT inter-municipal road matrix, Lazio](https://www.istat.it/notizia/matrici-di-contiguita-distanza-e-pendolarismo/) | R12_RI.csv: TEP_TOT, KM_TOT | `sources/istat_pendolarismo/Lazio.zip`. Town-hall to town-hall car times with traffic, 2021 municipalities; not public-transport or door-to-door times. |
| [ISTAT study-commuting matrix 2021](https://www.istat.it/notizia/matrice-di-pendolarismo-per-studio/), [methodology](https://www.istat.it/wp-content/uploads/2026/09/Nota-metodologica-Pendolarismo-per-studio-2021-.pdf) | Not yet downloaded | Published only on esploradati.istat.it, which refused connections on 30/09/2026. Excludes employed students; no school level. Fetch with `scripts/fetch_istat_study_matrix.py`. |
| [ISTAT BES dei territori 2025](https://www.istat.it/notizia/bes-dei-territori-edizione-2025/) | `Indicatori_per_provincia_sesso` | `sources/skills/istat_bes_territori_2025.zip`. Codes with a `-N22` suffix mark the 2022 labour-survey break. Graduate migration (11RIC025): Italian citizens, registry moves; 2023 provisional; Italy counts only moves abroad. |
| [ISTAT POSAS population by age](https://demo.istat.it/) | 1 January 2019 and 2026 | `sources/skills/istat_posas_*.zip`. 2026 is an estimate. |
| [MUR-USTAT enrolments](https://dati-ustat.mur.gov.it/dataset/iscritti) | Files 07, 13, 14a, 2024/25 | `sources/skills/ustat_*.csv`. File 14a excludes online universities and cells under 5. |
| [Excelsior 2025, Rieti, Lazio, Italy](https://excelsior.unioncamere.net/) | Rieti tables 4, 8, 12, 15 | `sources/skills/excelsior_*.xlsx`. Hiring intentions, not realised hires. Table numbers differ between the three workbooks; the script finds tables by title. Chemical-plant operators' hard-to-fill share is suppressed. |
| [MIM open data, schools](https://dati.istruzione.it/opendata/) | Students by track 2024/25; school registry 2025/26 | `sources/skills/mim_*.csv`. State schools only. |
| [Farmindustria, Indicatori Farmaceutici 2025](https://www.farmindustria.it/app/uploads/2022/03/IndicatoriFarmaceutici2025_Def_05082025.pdf) | Tav. 105, p.87 | `sources/skills/farmindustria_indicatori_2025.pdf`. Association processing of ISTAT data: Rieti 2nd by pharmaceutical share of manufacturing employment, outside the top 25 by headcount. |
| [Regione Lazio, ITS call 2026](https://www.regione.lazio.it/sites/default/files/documentazione/2026/DD-G11637-19-08-2026-allegato1-avviso.pdf) | pp.9, 13–14 | `sources/skills/lazio_avviso_its_2026.pdf`. 80 courses, about €330,000 each; deadline 22/09/2026. |
| Company and press sources (Takeda, SEKO, EMEC, Microdos, union statements) | Linked in report section 5 | Headcounts are company or press figures, not official statistics. No Takeda headcount after 2024 is published. |
| [CCIAA third report, 2023](https://www.rivt.camcom.it/files/terzorapportoeconomiaaltolazio-_9755.pdf) | PDF p.60, 2022 column | `sources/cciaa_rapporto_2023.pdf`; same-year SAM export comparison. |
| [CCIAA fourth report, 2024](https://www.rivt.camcom.it/files/quartorapportoeconomiaaltolazio-_10801.pdf) | Consulted for earlier vintage | Archived for traceability; not spliced into the latest series. |
| [Chamber-hosted value-added tables 2022](https://www.chpe.camcom.it/output_allegato.php?id=745843) | Province / industry workbook, Rieti row | `sources/tagliacarne_2022_download.zip`; same-year SAM macro and sector checks. |
| [Chamber-hosted value-added tables 2023–24](https://www.chpe.camcom.it/output_allegato.php?id=1425923) | Province / industry and per-capita workbooks | `sources/tagliacarne_2024_download.zip`; prosperity and nominal change, using one release. |
| [Regione Lazio Labour Market Report 2025](https://www.regione.lazio.it/sites/default/files/2025-12/Rapporto-mercato-lavoro-2025.pdf) | Table 1.1, 2024 | Gender employment gap; linked original. |
| [GSE PV report 2023](https://www.gse.it/documenti_site/Documenti%20GSE/Rapporti%20statistici/Solare%20Fotovoltaico%20-%20Rapporto%20Statistico%202023.pdf) | Provincial capacity and generation tables | `sources/gse_fotovoltaico_2023.pdf`; earlier PV deployment. |
| [GSE PV report 2024](https://www.gse.it/documenti_site/Documenti%20GSE/Rapporti%20statistici/Solare%20Fotovoltaico%20-%20Rapporto%20Statistico%202024.pdf) | PDF pp.15, 28 | `sources/gse_fotovoltaico_2024.pdf`; capacity and generation peers. |
| [Terna Regional Statistics 2024](https://download.terna.it/terna/Statistiche%20Regionali_2024_8de8598cb39d81e.pdf) | PDF pp.150–151, tables 5–6 | `sources/terna_regioni_2024.pdf`; total and renewable generation. |
| [CCIAA Pump Valley investigation](https://www.rivt.camcom.it/it/news/rieti-boom-export-manifatturiero-e-spiragli-di-luce-da-costruzioniturismo-e-attivita-professionali_1951.htm) | Institutional release, 11 July 2023 | Independent support for industrial capability; not current firm-level measurement. |

Run `python analysis/scripts/build_territorial_evidence.py` from the project directory. Dependencies: pandas, numpy, pyarrow, matplotlib and openpyxl. This reads local inputs and archived spreadsheets; it does not query live sources or update the original SAM model. Selected PDF observations are transcribed with URLs and page references in the script. The [manifest](output/input_manifest.csv) hashes the input data and downloaded PDF/ZIP sources.

Outputs include demographic peers and distance sensitivity, all Rieti municipality rows, energy summaries, official labour/trade/value-added extracts, the SAM cross-check, illustrative PV scenarios and four PNG/SVG figures. The [earlier main draft](sources/analisi_territoriale_before_revision.md) is preserved for comparison.

Commuting and skills evidence: run `python analysis/scripts/build_commuting_evidence.py` and `python analysis/scripts/build_skills_evidence.py`. Outputs are the `commuting_*`, `work_commuting_*`, `study_commuting_*`, `bes_*`, `young_adults_*`, `university_*`, `excelsior_*` and `secondary_school_*` tables in `analysis/output`, and figures 5 and 6.
