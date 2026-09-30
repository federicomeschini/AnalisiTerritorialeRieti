# Rieti territorial analysis from the 2022 MR-SAM

## Executive reading

Rieti is not a small, closed local economy in this matrix. It is a **highly externalised production platform**: it combines a few unusually strong tradable activities—agriculture, pharmaceuticals, machinery, electronics and logistics—with large locally delivered activities such as construction, health, real estate and public services.

The most consequential finding is the very weak within-province production loop. Only **€5.9m**, or **0.17%**, of Rieti firms' intermediate inputs are sourced from another Rieti sector in the model. This is a signal of an economy whose suppliers, buyers and value chains are organised largely beyond the provincial boundary. It creates a clear development question: where can Rieti retain more value locally without trying to replace efficient external supply chains?

## Investment priorities for a policymaker

The purpose of this analysis is not simply to describe Rieti's economy. It is to identify where public investment, convening power and regulation can plausibly create the greatest additional value. The SAM supports a **portfolio**, rather than one all-purpose ranking: export transformation, enabling infrastructure and essential territorial services have different public objectives.

| Priority | Evidence from the SAM | Policy investment thesis | What success should look like |
|---|---|---|---|
| **1. Logistics, warehousing & transport support** | €608m output; LQ 3.02; 81% of sales serve external intermediate markets or exports; national output multiplier 2.05. | Treat the sector as a platform for local producers, not only transit: logistics real estate, digital freight, cold chain, intermodal access and specialist skills. | More local firms using logistics services; shorter/more reliable freight journeys; logistics jobs and supplier contracts retained locally. |
| **2. Agri-food value chain** | Crops/livestock: €332m output, LQ 6.05 and €50m ROW exports. Food: €234m output, multiplier 2.07 and €73m ROW exports. | Move beyond primary production through processing, packaging, certification, storage, water efficiency and route-to-market support. | Higher share of local agricultural output processed in the province; export value per tonne; new food-processing firms and wages. |
| **3. Advanced export manufacturing** | Pharmaceuticals, machinery and electronics together: €519m output and about €306m ROW exports; LQs 3.56, 5.17 and 5.76. | Create a targeted industrial-innovation offer: reliable utilities, technical skills, testing/R&D links, supplier qualification and export support. | Private investment leveraged; skilled jobs; R&D/technology-transfer projects; local supplier spend and export growth. |
| **4. Green construction, energy and renovation** | Construction is the largest sector (€766m), with a 2.35 national output multiplier; electricity/gas has the highest sector multiplier (2.55). | Focus public capital on deep retrofit, seismic safety, renewable/efficiency installations and skills—not undifferentiated construction demand. | Buildings renovated; energy saved; resilient public assets; construction SMEs gaining green capabilities. |
| **5. Health, care and education as territorial infrastructure** | Health: €443m output and €301m government demand; social care: €104m; education: €112m. | Use facilities, workforce and smart procurement to improve access in a dispersed territory and support ageing-in-place. This is a resilience/equity priority, not an export bet. | Travel time to care; unmet need; care workforce stability; digital/territorial service coverage. |
| **6. Workforce and producer-service capacity** | Employment activities have LQ 3.66; architecture/engineering has €101m output, 92% external-market exposure and a 1.79 multiplier. | Build the cross-cutting skills, engineering, project-management and recruitment capability required by the five priorities above. | Apprenticeships and technical completions; firms reporting skills availability; local professional-service procurement. |

### A transparent economic-transformation screen

The sector CSV contains `economic_transformation_priority_score_0_100`. It is a screening tool for productive investment, composed of output scale (20%), specialisation against Lazio (25%), external-market reach (25%), national output multiplier (15%) and national value-added multiplier (15%). The LQ contribution is capped at 3 so that a tiny niche cannot dominate merely because it is unusually concentrated.

The highest-scoring directly productive activities are warehousing/transport support (**87.5**), crops/livestock (**83.5**), machinery (**82.3**), electronics (**78.9**) and pharmaceuticals (**77.7**). The score intentionally does not decide the case for health, care or public services: those should be assessed with access, equity and resilience criteria, not export metrics.

Use the score to select sectors for due diligence, not as an automatic grant allocation formula. Before funding a project, test additionality, demand, land/infrastructure constraints, the beneficiary firms and the cost per outcome.

## What the matrix contains

The source file has 108 Italian NUTS-3 territories, 60 NACE aggregates for each territory, and seven national institutional accounts (households, government, capital formation, labour, capital, taxes and rest of world). Rieti is `ITI42`.

Rows are receiving accounts and columns are spending accounts. The table is balanced for Rieti: sector-column expenditure, including intermediate purchases, labour, capital and taxes, equals sector output. The monetary scale is consistent with **€ millions**; this should be checked against the original data release documentation before publication.

This is an estimated interregional SAM/MRIO, not a census of individual firm transactions. Its flow estimates are excellent for identifying structural hypotheses, but especially the small within-Rieti flows should be validated with local business, procurement and freight evidence before being used as a policy target.

## Size of the economy

| 2022 indicator | €m |
|---|---:|
| Gross output | 6,503.7 |
| Intermediate inputs | 3,418.6 |
| Value added (labour + capital income) | 2,965.8 |
| Labour compensation | 1,334.6 |
| Capital income | 1,631.2 |
| Product taxes | 119.4 |

The value-added-to-output ratio is about **45.6%**. This is an accounting ratio, not a GDP estimate, although the value-added total is the relevant territorial value-creation measure in the SAM.

## A province connected outward

### Where Rieti firms buy intermediate inputs

| Source | €m | Share of intermediate inputs |
|---|---:|---:|
| Rieti | 5.9 | 0.17% |
| Other Lazio provinces | 456.2 | 13.34% |
| Rest of Italy | 2,401.1 | 70.24% |
| Rest of world/import account | 555.4 | 16.25% |

### Where Rieti production is delivered

| Destination/account | €m | Share of gross output |
|---|---:|---:|
| Rieti intermediate demand | 5.9 | 0.09% |
| Other Lazio intermediate demand | 391.0 | 6.01% |
| Rest-of-Italy intermediate demand | 2,801.1 | 43.07% |
| Household final demand (national account) | 1,282.6 | 19.72% |
| Government final demand (national account) | 777.7 | 11.96% |
| Capital formation (national account) | 515.8 | 7.93% |
| Rest-of-world exports | 729.6 | 11.22% |

The leading intermediate-demand destinations are **Roma (`ITI43`, €331.8m)**, **Milano (`ITC4C`, €278.3m)** and **Napoli (`ITF33`, €123.3m)**. This makes Rieti's production system far more connected to national urban and industrial nodes than a simple “peripheral province” narrative would imply.

National household, government and capital-formation accounts are not geographically assigned inside the file. They must not be interpreted as final demand physically located in the province of Rieti.

## The sectoral story

`LQ` below is an **output-structure location quotient against all five Lazio provinces**: a value above 1 means Rieti's share of that activity in its output mix is above the corresponding Lazio share. It is not an employment LQ.

| Sector | Gross output €m | Value added €m | Output LQ vs Lazio | What stands out |
|---|---:|---:|---:|---|
| Construction | 766.5 | 231.1 | 1.85 | Largest output sector; €353.3m is assigned to capital formation. |
| Warehousing & transport support | 608.3 | 235.2 | 3.02 | Strong logistics anchor; €490.5m of sales are to external intermediate markets or rest-of-world exports. |
| Real estate | 451.2 | 373.8 | 1.24 | Highest large-sector value added; €261.0m goes to national household demand. |
| Human health | 442.8 | 214.6 | 1.32 | Major territorial service base; €300.9m goes to government final demand. |
| Crop & animal production | 332.5 | 191.4 | 6.05 | Major comparative specialisation; €49.7m rest-of-world exports. |
| Public administration & defence | 288.2 | 180.7 | 0.30 | Large in absolute terms but underrepresented in the Lazio production mix. |
| Retail | 286.6 | 167.5 | 1.36 | Important resident-facing economy, with €198.1m in household demand. |
| Pharmaceuticals | 249.5 | 87.6 | 3.56 | Clear tradable specialisation; €156.8m rest-of-world exports. |
| Food, beverages & tobacco | 234.1 | 46.3 | 1.91 | Agri-food conversion base; €72.7m rest-of-world exports. |
| Electricity, gas & steam | 212.5 | 56.7 | 0.26 | Large but not a relative specialisation; sells strongly beyond Lazio. |
| Machinery & equipment | 139.2 | 38.3 | 5.17 | Tradable manufacturing niche; €88.6m rest-of-world exports. |
| Electronics & optical products | 130.2 | 46.4 | 5.76 | High specialisation; €60.4m rest-of-world exports. |

### Four distinct territorial roles

1. **Export-oriented production** — Pharmaceuticals, machinery, electronics, food and agriculture combine high specialisation with international sales. These are the most plausible candidates for an export-and-supply-chain strategy.
2. **National logistics platform** — Warehousing and transport support is both large and specialised. About 81% of its output is directed to external intermediate markets or exports; its priority is connectivity, logistics labour, digital freight services and links with local producers.
3. **Investment and built-environment economy** — Construction is Rieti's biggest output activity and receives €353.3m from the capital-formation account. It is a useful indicator of investment exposure, but the national capital-formation account prevents assigning that spending to projects physically in Rieti without another dataset.
4. **Territorial anchor services** — Health, public administration, education, real estate and retail are the large place-based stabilisers. Health in particular is more concentrated than the Lazio norm and substantially government-funded in the SAM.

## Sectoral multipliers: national impact and Rieti retention

The detailed table now includes two complementary Type-I multiplier measures for every sector.

- **National Type-I output multiplier**: total gross output generated anywhere in Italy by €1 of additional final demand for the sector, including direct and indirect production effects.
- **National Type-I value-added multiplier**: Italian value added generated per €1 of that additional final demand.

They are calculated by collapsing the full interregional matrix into a 63-sector Italian input-output system and inverting its Leontief matrix. This preserves sectoral technology and national supply-chain effects, but it **does not assign the indirect impact to individual provinces**. It is therefore the right measure for the economic scale of an intervention, while the Rieti-local measure is the right diagnostic for local retention.

| Rieti sector | National output multiplier | National VA generated per €1 demand | Rieti-local output multiplier | Interpretation |
|---|---:|---:|---:|---|
| Electricity, gas & steam | 2.55 | €0.77 | 1.001 | Largest national output ripple in the Rieti sector mix. |
| Construction | 2.35 | €0.81 | 1.001 | Investment/construction demand has a large Italian supply-chain effect. |
| Food, beverages & tobacco | 2.07 | €0.63 | 1.001 | Strong propagation case for agri-food processing investments. |
| Warehousing & transport support | 2.05 | €0.83 | 1.001 | Especially attractive mix of scale and value-added propagation. |
| Machinery & equipment | 2.00 | €0.65 | 1.001 | A tradable niche with material national linkages. |
| Crop & animal production | 1.85 | €0.90 | 1.001 | High value-added intensity alongside agricultural specialisation. |
| Electronics & optical products | 1.70 | €0.63 | 1.001 | High-LQ manufacturing with meaningful national propagation. |
| Human health | 1.63 | €0.75 | 1.001 | Service-sector effects are smaller than construction/logistics, but remain substantial. |
| Pharmaceuticals | 1.56 | €0.59 | 1.001 | Export-oriented sector; much of its indirect activity is outside Rieti. |
| Real estate | 1.22 | €0.92 | 1.000 | High value added, but relatively limited upstream output propagation. |

For example, a €1m final-demand expansion in Rieti logistics is associated with about **€2.05m of total Italian output** and **€0.83m of Italian value added** under the national technology assumptions. The Rieti-local output effect remains approximately €1.00m because the matrix records very few provincial intermediate purchases.

These are **Type-I production multipliers**: they exclude household-income-induced consumption, employment effects and fiscal feedbacks. They should be used as scenario coefficients—not as forecasts—and are most defensible for marginal changes small relative to sector size.

## The local-retention challenge

The local 60×60 production block is exceptionally small: its largest flows are only €0.62m (construction to construction), €0.45m (warehousing to warehousing), €0.17m (health to health) and €0.15m (electricity to electricity). A local-only Type-I output multiplier computed from that block is therefore approximately **1.00** for every sector.

This should be read as a diagnostic: the SAM has little within-Rieti intermediate circulation, so a standard “buy local” multiplier story cannot be assumed. It does **not** mean investment in Rieti has no broader impact; it means most of that effect is modelled elsewhere in Lazio, Italy or abroad.

The practical opportunity is not indiscriminate import substitution. It is to identify a small number of inputs or services where Rieti can build viable local capacity:

- producer services and maintenance around logistics, construction and health;
- agri-food processing, packaging, cold chain and quality certification;
- specialised business services for the pharmaceutical, machinery and electronics activities;
- procurement and supplier-development programmes that make local firms visible to the large anchor sectors.

## A multiplier-enabled screen for growth opportunities

The SAM does **not** contain a time series, so it cannot demonstrate that a sector has recently grown or forecast its future growth rate. It can, however, identify sectors where a marginal expansion has a strong combination of existing specialisation, external-market reach, meaningful scale and national supply-chain propagation.

The accompanying sector CSV now supplies `demand_expansion_propagation_score_0_100`. It is a transparent **opportunity screen, not a forecast**: 15% output scale, 20% specialisation, 25% external-market reach, 20% national Type-I output multiplier and 20% national Type-I value-added multiplier. The two multiplier components therefore account for 40% of the score. As for the existing transformation score, the LQ contribution is capped to prevent very small niches from dominating.

| Sector | Opportunity score | National output multiplier | National VA per €1 demand | Why it is a growth candidate |
|---|---:|---:|---:|---|
| Warehousing & transport support | **85.2** | 2.05 | €0.83 | Large, specialised and highly external-facing; the clearest platform sector for an investment-and-supplier strategy. |
| Crop & animal production | **81.1** | 1.85 | €0.90 | Exceptional specialisation and high value-added propagation; strongest when tied to processing rather than treated as primary production alone. |
| Machinery & equipment | **79.6** | 2.00 | €0.65 | High-LQ export manufacturing with material national production effects. |
| Electronics & optical products | **75.3** | 1.70 | €0.63 | A compact but highly specialised tradable niche; prioritise skills, supplier qualification and reliable utilities. |
| Pharmaceuticals | **73.1** | 1.56 | €0.59 | Large international sales and clear specialisation; multiplier effects are lower than logistics or food, so the investment case rests also on export capability and skilled jobs. |
| Food, beverages & tobacco | **66.1** | 2.07 | €0.63 | The strongest agri-food transformation bridge: comparatively high output propagation alongside a material export base. |

The score usefully distinguishes three roles that should not be conflated:

1. **Direct growth engines** — logistics, agriculture/food and the three advanced-manufacturing activities combine a credible market base with propagation effects.
2. **Multiplier-rich enablers** — construction (output multiplier **2.35**, VA **€0.81** per €1) and electricity/gas (the highest output multiplier, **2.55**) can generate substantial Italian supply-chain activity, but construction's market reach is lower and electricity/gas is underrepresented in Rieti's output mix (LQ **0.26**). They are better framed as enabling infrastructure and resilience priorities than as stand-alone export-growth bets.
3. **Small, high-scoring niches** — postal/courier services, employment activities, wood products and some materials sectors can appear high in a formula because of external sales and specialisation. They should enter the pipeline only after firm-level validation of scale, demand and additionality.

### What a €10m demand-expansion scenario implies

The figures below are scenario coefficients, not forecasts. They show the total direct-plus-indirect activity expected **anywhere in Italy** from €10m of additional final demand in the Rieti sector, using national technology. They do not imply that the indirect production or value added stays in Rieti.

| Sector | Total Italian output associated with €10m demand | Total Italian value added associated with €10m demand |
|---|---:|---:|
| Electricity, gas & steam | €25.48m | €7.75m |
| Construction | €23.54m | €8.07m |
| Food, beverages & tobacco | €20.72m | €6.29m |
| Warehousing & transport support | €20.53m | €8.35m |
| Machinery & equipment | €20.00m | €6.50m |
| Crop & animal production | €18.47m | €8.98m |
| Electronics & optical products | €17.00m | €6.29m |
| Pharmaceuticals | €15.64m | €5.87m |

The key policy implication is to support sectors where **market opportunity and multiplier effects coincide**, then add a local-retention test. For each candidate project, identify the 10–20 largest input categories and ask which one can be supplied or transformed competitively in Rieti. Given the SAM's near-zero local multiplier, this step is essential: otherwise a strong national ripple can be mistaken for local value retention.

## Recommended next analytical steps

1. **Validate the anchor activities** with local unit-level sources: ASIA/ATECO firm and employment data, Chamber of Commerce records, health-system procurement, freight data and interviews with leading employers.
2. **Map the 10–20 largest outside suppliers** to each priority chain. The SAM identifies where leakages are material, but not the individual firms or whether local substitution is feasible.
3. **Build a targeted regional input-output scenario** for a logistics investment, an agri-food processing facility, or an expansion in pharma/mechanics. Keep the full Italy linkages rather than applying the near-zero local multiplier.
4. **Add municipal geography** (population, commuting, land use, broadband, road/rail travel times and business locations) to distinguish the Rieti urban area, the Salto-Cicolano area, the Velino corridor and mountain municipalities.

## Reproducible outputs

- [Full 60-sector indicator table](/C:/Users/FedericoMeschini/OneDrive%20-%20OpenEconomics%20S.r.l/Desktop/Analisi%20territoriale%20Rieti/output/rieti_sectoral_indicators_2022.csv)
- [Intermediate-demand destinations by NUTS-3 code](/C:/Users/FedericoMeschini/OneDrive%20-%20OpenEconomics%20S.r.l/Desktop/Analisi%20territoriale%20Rieti/output/rieti_intermediate_destinations_2022.csv)
- [Rieti macro summary](/C:/Users/FedericoMeschini/OneDrive%20-%20OpenEconomics%20S.r.l/Desktop/Analisi%20territoriale%20Rieti/output/rieti_macro_summary_2022.csv)
- [Reproducible analysis script](/C:/Users/FedericoMeschini/OneDrive%20-%20OpenEconomics%20S.r.l/Desktop/Analisi%20territoriale%20Rieti/scripts/analyze_rieti_mrsam.py)
