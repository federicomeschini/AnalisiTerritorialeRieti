# Rieti: validated reading of the supplied 2022 MR-SAM

**Revised 30 September 2026.** This technical note supports the [territorial analysis](../analisi_territoriale_rieti_per_policy_makers.md). The earlier interpretation is preserved in [the source archive](../analysis/sources/analisi_sam_before_validation.md). Original matrix and numerical output CSVs are unchanged.

## What the matrix can support

The SAM identifies hypotheses about productive structure and intersectoral relationships. It is not a census of firms' transactions, an observed export series or a forecast. External checks support a specialised manufacturing narrative, but reveal material differences in sector magnitudes. In particular, the previous claims of a large direct agricultural export base and demonstrated near-zero local supply-chain retention should not be used in a policy presentation.

There are **107 territorial codes**, **6,569 production accounts**, and seven national accounts, making **6,576 accounts** in total. Rieti (`ITI42`) has 60 sector accounts; there are 63 distinct sector aggregates across the full matrix. The previous count of 108 territories was incorrect.

Rows receive and columns spend. The monetary convention in the existing script is millions of euros. The parquet supplies schema metadata, but no substantive release methodology or units statement. The convention is plausible in aggregate, not yet documented by the producer.

## Accounting scale and numerical verification

| Rieti 2022 accounting total | €m, assumed units |
|---|---:|
| Gross output | 6,503.7 |
| Intermediate inputs | 3,418.6 |
| Labour plus capital value added | 2,965.8 |
| Labour compensation | 1,334.6 |
| Capital income | 1,631.2 |
| Tax account payments | 119.4 |

Gross output is not GDP. The interpretation of tax payments and valuation requires the release documentation; adding the tax account to labour and capital is not automatically an official provincial GDP calculation.

The independent check rereads Rieti's rows across every matrix column. Row receipts and column expenditure agree within very small numerical residuals: maximum sector relative error is below one part per million. The saved sector output CSV also agrees with the reread columns. This verifies arithmetic and extraction, **not empirical territorial allocation**. [Balance check](../analysis/output/sam_balance_check.csv).

The SAM is about 6.1% below the archived Chamber-hosted 2022 value-added estimate. Broad sector allocations also differ. Use the [main analysis's same-year comparison](../analisi_territoriale_rieti_per_policy_makers.md) and [validation appendix](../analysis/validation_and_sources.md), rather than interpreting internal balance as external validation.

## Productive structure: model estimates to investigate

| Activity | Output €m | Value added €m | Output LQ vs Lazio |
|---|---:|---:|---:|
| Construction | 766.5 | 231.1 | 1.85 |
| Warehousing and transport support | 608.3 | 235.2 | 3.02 |
| Real estate | 451.2 | 373.8 | 1.24 |
| Human health | 442.8 | 214.6 | 1.32 |
| Crop and animal production | 332.5 | 191.4 | 6.05 |
| Pharmaceuticals | 249.5 | 87.6 | 3.56 |
| Food, beverages and tobacco | 234.1 | 46.3 | 1.91 |
| Machinery | 139.2 | 38.3 | 5.17 |
| Electronics and optical products | 130.2 | 46.4 | 5.76 |

LQ compares a sector's share of Rieti output with its share across all five Lazio provinces. It does not measure productivity, profitability, employment concentration or recent growth. Lazio's Rome-heavy mix affects the comparison.

The strongest uses are to identify activities for employer interviews and supplier mapping, and to relate the productive system to demographic and service needs. Agriculture and processing remain plausible commercial-development hypotheses, but their modelled international sales cannot be taken as demonstrated demand. Construction is a large modelled activity; that does not establish durable future demand or the location of investment expenditure. Health output associated with the government account does not directly measure local health budgets or access to care.

## External trade check

The main analysis compares five sectors with the Chamber/ISTAT 2022 product export tables. Machinery is close; pharmaceuticals, electronics, food and agriculture differ materially. Agriculture has a broader official comparator than the SAM crop/livestock sector, yet the model amount is vastly larger. Accounting coverage, valuation, territorial attribution and model construction must be reconciled before reusing those magnitudes.

The model's total rest-of-world sales of €729.6m include activities outside customs goods coverage. Comparing that total alone with customs exports cannot validate the model. The [sector-level comparison](../analysis/output/sam_official_export_crosscheck.csv) is more informative, while still requiring a classification bridge.

## Interprovincial connections: an allocation result, not observed procurement

| Intermediate purchase origin | €m | Share of intermediate inputs |
|---|---:|---:|
| Rieti | 5.9 | 0.17% |
| Other Lazio | 456.2 | 13.34% |
| Rest of Italy | 2,401.1 | 70.24% |
| Rest of world | 555.4 | 16.25% |

These numbers reproduce the supplied matrix. The extremely small provincial block is a validation priority. Without construction documentation and independent purchasing evidence, it is not defensible to call it a demonstrated territorial weakness or to infer that virtually all indirect benefits accrue elsewhere.

The estimated leading intermediate sales destinations are Rome (€331.8m), Milan (€278.3m) and Naples (€123.3m). These are modelled commercial links, not measured freight flows or commuting patterns. National household, government and capital-formation accounts are not geographically assigned and cannot be read as expenditure physically located in Rieti.

## Multipliers: national technology, limited territorial interpretation

The original script aggregates the full matrix into a 63-sector national input-output table and calculates its Leontief inverse. The resulting Type-I coefficients describe direct and indirect production under **average national technology**, fixed input proportions and unconstrained supply.

| Sector | Italian output per €1 final demand | Italian value added per €1 final demand |
|---|---:|---:|
| Electricity, gas and steam | 2.55 | 0.77 |
| Construction | 2.35 | 0.81 |
| Food, beverages and tobacco | 2.07 | 0.63 |
| Warehousing and transport support | 2.05 | 0.83 |
| Machinery | 2.00 | 0.65 |
| Crop and animal production | 1.85 | 0.90 |
| Electronics and optical products | 1.70 | 0.63 |
| Pharmaceuticals | 1.56 | 0.59 |

These are not the full interregional response to a shock specifically located in Rieti. They exclude household-induced consumption and do not quantify jobs, net additional benefit, fiscal return, displacement or project profitability. Output and value added are different accounting measures and must not be added together.

The local inverse uses only Rieti's sector block and produces output coefficients near 1.00. It omits supply-chain paths that leave Rieti and later re-enter it. It therefore cannot establish total provincial retention even if the input allocation were correct.

A €1m logistics-demand illustration would give about €2.05m gross Italian production under this national-sector technology, including the initial demand. It is not a predicted €2.05m benefit to Rieti or a return on €1m of public expenditure. A funded project has its own expenditure mix, imports, capacity constraints and counterfactual.

## How this changes project screening

The original CSV contains two analyst-designed weighted opportunity scores. They remain available for traceability, but should not rank investment allocations: results depend on unvalidated sector trade estimates, subjective weights and the chosen benchmark. No sector growth time series is supplied by the SAM.

Use a demand-led process instead: establish named buyers or employers, test the specific constraint, identify feasible local capabilities, assess additionality and costs, and select outcomes that institutions can measure. Territorial services require access and equity criteria alongside economic criteria. A higher national multiplier alone is not a reason to prioritise one project over another.

## Files and reproduction

- [Sector indicators](output/rieti_sectoral_indicators_2022.csv)
- [Macro summary](output/rieti_macro_summary_2022.csv)
- [Intermediate destinations](output/rieti_intermediate_destinations_2022.csv)
- [Original SAM calculation script](scripts/analyze_rieti_mrsam.py)
- [Independent territorial evidence and validation script](../analysis/scripts/build_territorial_evidence.py)
- [Official-source register and interpretation limits](../analysis/validation_and_sources.md)

Run `python SAM/scripts/analyze_rieti_mrsam.py` to rebuild the original SAM outputs, or `python analysis/scripts/build_territorial_evidence.py` for the independent checks and integrated territorial evidence. No claim here substitutes for obtaining the matrix's release documentation.
