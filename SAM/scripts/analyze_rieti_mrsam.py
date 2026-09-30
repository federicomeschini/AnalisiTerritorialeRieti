"""Create reproducible Rieti sector indicators from the 2022 MR-SAM.

The source is a wide matrix.  Rows are receiving accounts and columns are
spending accounts; the 60 ITI42 production columns are Rieti industries.
Monetary values in this release are treated as millions of euro.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mrsam_euita_2022_3oe_wide.parquet"
OUTPUT = ROOT / "output"
RIETI = "ITI42"
LAZIO = {"ITI41", "ITI42", "ITI43", "ITI44", "ITI45"}
FINAL_ACCOUNTS = {"HH", "GOV", "CF", "ROW"}


def territory(code: str) -> str:
    """Return the territorial part of a matrix account label."""
    return code.split("__", maxsplit=1)[0]


def sector_code(code: str) -> str:
    """Return the NACE aggregate and account type, excluding territory."""
    return "__".join(code.split("__")[1:])


def national_type_i_multipliers(
    parquet: pq.ParquetFile, columns: list[str], labels: pd.Series
) -> tuple[pd.Series, pd.Series]:
    """Return national-technology output and value-added Type-I multipliers.

    The underlying interregional table is collapsed to its 63 NACE aggregates
    before inverting the Leontief system. This preserves Italian sectoral
    technology and all direct/indirect national effects while avoiding a
    misleadingly expensive dense inverse of the 6,569-industry MRIO. It is
    deliberately a *national* multiplier, not a claim about Rieti retention.
    """
    production_rows = np.flatnonzero(~labels.str.startswith("IT__"))
    row_sectors = np.array(
        [sector_code(account) for account in labels.iloc[production_rows]]
    )
    production_columns = [
        column for column in columns if column != "row_label" and not column.startswith("IT__")
    ]
    column_sectors = np.array([sector_code(account) for account in production_columns])
    sectors = sorted(set(row_sectors) | set(column_sectors))
    sector_index = {sector: index for index, sector in enumerate(sectors)}
    transactions = np.zeros((len(sectors), len(sectors)))
    output = np.zeros(len(sectors))
    value_added = np.zeros(len(sectors))
    labour_position = int(np.flatnonzero(labels == "IT__LAB__L")[0])
    capital_position = int(np.flatnonzero(labels == "IT__CAP__K")[0])

    for start in range(0, len(production_columns), 300):
        batch = production_columns[start : start + 300]
        values = parquet.read(columns=batch).to_pandas().fillna(0.0)
        product_values = values.iloc[production_rows].to_numpy()
        rows_aggregated = pd.DataFrame(product_values, index=row_sectors).groupby(
            level=0, sort=False
        ).sum()
        batch_sectors = np.array([sector_code(account) for account in batch])
        for sector in set(batch_sectors):
            positions = np.flatnonzero(batch_sectors == sector)
            index = sector_index[sector]
            transactions[:, index] += (
                rows_aggregated.reindex(sectors, fill_value=0.0)
                .iloc[:, positions]
                .sum(axis=1)
                .to_numpy()
            )
            output[index] += values.iloc[:, positions].sum(axis=0).sum()
            value_added[index] += (
                values.iloc[labour_position, positions].sum()
                + values.iloc[capital_position, positions].sum()
            )

    technical_coefficients = transactions / output[None, :]
    leontief = np.linalg.inv(np.eye(len(sectors)) - technical_coefficients)
    output_multiplier = pd.Series(leontief.sum(axis=0), index=sectors)
    value_added_multiplier = pd.Series(
        (value_added / output) @ leontief, index=sectors
    )
    return output_multiplier, value_added_multiplier


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    parquet = pq.ParquetFile(SOURCE)
    columns = parquet.schema_arrow.names
    labels = parquet.read(columns=["row_label"]).to_pandas()["row_label"]

    rieti_columns = sorted(c for c in columns if territory(c) == RIETI)
    lazio_columns = [c for c in columns if territory(c) in LAZIO]
    rieti_indices = np.flatnonzero(labels.str.startswith(f"{RIETI}__"))
    rieti_row_labels = labels.iloc[rieti_indices].tolist()
    # Ensure that row and column accounts have the same sector order.
    rieti_row_order = [rieti_row_labels.index(c) for c in rieti_columns]

    # Inputs, value added and gross output. Sparse zeros are stored as nulls.
    rieti = (
        parquet.read(columns=["row_label", *rieti_columns])
        .to_pandas()
        .set_index("row_label")
        .fillna(0.0)
    )
    lazio = (
        parquet.read(columns=["row_label", *lazio_columns])
        .to_pandas()
        .set_index("row_label")
        .fillna(0.0)
    )
    production_rows = rieti.index[~rieti.index.str.startswith("IT__")]
    origin = production_rows.str.split("__").str[0]

    def purchases_from(territories: set[str]) -> pd.Series:
        return rieti.loc[production_rows[origin.isin(territories)]].sum(axis=0)

    gross_output = rieti.sum(axis=0)
    local_inputs = purchases_from({RIETI})
    lazio_inputs = purchases_from(LAZIO - {RIETI})
    italy_inputs = purchases_from(set(origin.unique()) - LAZIO)
    imported_inputs = rieti.loc["IT__ROW__R"]
    intermediate_inputs = local_inputs + lazio_inputs + italy_inputs + imported_inputs
    labour = rieti.loc["IT__LAB__L"]
    capital = rieti.loc["IT__CAP__K"]
    taxes = rieti.loc["IT__TAX__T"]

    # Deliveries from Rieti's production rows to every destination. Reading the
    # wide source in batches keeps memory use modest despite its 6,577 columns.
    sales = pd.DataFrame(
        0.0,
        index=rieti_columns,
        columns=[
            "sales_rieti",
            "sales_other_lazio",
            "sales_rest_italy",
            "sales_households",
            "sales_government",
            "sales_capital_formation",
            "sales_row_exports",
        ],
    )
    destination_provinces: dict[str, float] = {}
    for start in range(1, len(columns), 300):
        batch = columns[start : start + 300]
        values = parquet.read(columns=batch).to_pandas().iloc[rieti_indices]
        values = np.nan_to_num(values.to_numpy()[rieti_row_order, :])
        for column_index, destination in enumerate(batch):
            destination_territory = territory(destination)
            value = values[:, column_index]
            if destination_territory == RIETI:
                sales["sales_rieti"] += value
            elif destination_territory in LAZIO:
                sales["sales_other_lazio"] += value
            elif destination_territory != "IT":
                sales["sales_rest_italy"] += value
            else:
                account = destination.split("__")[1]
                account_columns = {
                    "HH": "sales_households",
                    "GOV": "sales_government",
                    "CF": "sales_capital_formation",
                    "ROW": "sales_row_exports",
                }
                if account in account_columns:
                    sales[account_columns[account]] += value
            if destination_territory != "IT":
                destination_provinces[destination_territory] = (
                    destination_provinces.get(destination_territory, 0.0) + value.sum()
                )

    # Output-structure location quotient against the aggregate of the five
    # Lazio provinces. It is not an employment LQ.
    lazio_output = lazio.sum(axis=0)
    rieti_sector_codes = [sector_code(c) for c in rieti_columns]
    lazio_by_sector = pd.Series(0.0, index=rieti_sector_codes)
    for column, value in lazio_output.items():
        code = sector_code(column)
        if code in lazio_by_sector.index:
            lazio_by_sector.loc[code] += value
    output_lq = (gross_output / gross_output.sum()) / (
        lazio_by_sector.to_numpy() / lazio_by_sector.sum()
    )

    # A local-only Type-I multiplier is deliberately supplied as a diagnostic.
    # It excludes inputs sourced beyond Rieti, so it shows territorial retention
    # rather than an Italy-wide macro multiplier.
    local_transactions = rieti.loc[rieti_columns, rieti_columns].to_numpy()
    local_a = local_transactions / gross_output.to_numpy()[None, :]
    local_leontief = np.linalg.inv(np.eye(len(rieti_columns)) - local_a)
    local_multiplier = local_leontief.sum(axis=0)
    local_value_added_multiplier = (
        (labour + capital).to_numpy() / gross_output.to_numpy()
    ) @ local_leontief
    national_output_multiplier, national_value_added_multiplier = national_type_i_multipliers(
        parquet, columns, labels
    )

    detail = pd.DataFrame(
        {
            "nace_aggregate": rieti_sector_codes,
            "gross_output_mEUR": gross_output.values,
            "value_added_mEUR": (labour + capital).values,
            "labour_compensation_mEUR": labour.values,
            "capital_income_mEUR": capital.values,
            "taxes_mEUR": taxes.values,
            "local_input_mEUR": local_inputs.values,
            "other_lazio_input_mEUR": lazio_inputs.values,
            "rest_italy_input_mEUR": italy_inputs.values,
            "import_input_mEUR": imported_inputs.values,
            "local_input_share_pct": 100 * local_inputs.values / intermediate_inputs.values,
            "sales_rieti_mEUR": sales["sales_rieti"].values,
            "sales_other_lazio_mEUR": sales["sales_other_lazio"].values,
            "sales_rest_italy_mEUR": sales["sales_rest_italy"].values,
            "sales_households_mEUR": sales["sales_households"].values,
            "sales_government_mEUR": sales["sales_government"].values,
            "sales_capital_formation_mEUR": sales["sales_capital_formation"].values,
            "sales_ROW_exports_mEUR": sales["sales_row_exports"].values,
            "output_LQ_vs_Lazio": output_lq,
            "national_type_I_output_multiplier": national_output_multiplier.loc[
                rieti_sector_codes
            ].values,
            "national_type_I_value_added_multiplier_EUR_per_EUR": national_value_added_multiplier.loc[
                rieti_sector_codes
            ].values,
            "rieti_local_type_I_output_multiplier": local_multiplier,
            "rieti_local_type_I_value_added_multiplier_EUR_per_EUR": local_value_added_multiplier,
        }
    )
    detail["external_intermediate_and_export_sales_mEUR"] = (
        detail["sales_other_lazio_mEUR"]
        + detail["sales_rest_italy_mEUR"]
        + detail["sales_ROW_exports_mEUR"]
    )
    detail["external_intermediate_and_export_sales_share_pct"] = (
        100
        * detail["external_intermediate_and_export_sales_mEUR"]
        / detail["gross_output_mEUR"]
    )
    # Policy screen for economic transformation. This is intentionally not a
    # social-need index (which would rank health/care differently). LQ is
    # capped at 3 so a very small niche cannot dominate the ranking.
    detail["priority_scale_component"] = detail["gross_output_mEUR"].rank(pct=True)
    detail["priority_specialisation_component"] = np.clip(
        np.log(detail["output_LQ_vs_Lazio"].clip(lower=1.0)) / np.log(3.0),
        0.0,
        1.0,
    )
    detail["priority_market_reach_component"] = (
        detail["external_intermediate_and_export_sales_share_pct"] / 100
    )
    detail["priority_national_output_multiplier_component"] = (
        detail["national_type_I_output_multiplier"] - 1.0
    ) / (detail["national_type_I_output_multiplier"].max() - 1.0)
    detail["priority_value_added_component"] = (
        detail["national_type_I_value_added_multiplier_EUR_per_EUR"]
        / detail["national_type_I_value_added_multiplier_EUR_per_EUR"].max()
    )
    detail["economic_transformation_priority_score_0_100"] = 100 * (
        0.20 * detail["priority_scale_component"]
        + 0.25 * detail["priority_specialisation_component"]
        + 0.25 * detail["priority_market_reach_component"]
        + 0.15 * detail["priority_national_output_multiplier_component"]
        + 0.15 * detail["priority_value_added_component"]
    )

    # This second screen deliberately gives 40% of the weight to national
    # Type-I propagation. It is an opportunity screen for a marginal demand
    # expansion, *not* a forecast of observed sector growth: the MR-SAM has
    # no time series on which to estimate growth rates. Its other components
    # test whether the activity is already specialised, reaches external
    # markets and is large enough to matter in Rieti.
    detail["demand_expansion_propagation_score_0_100"] = 100 * (
        0.15 * detail["priority_scale_component"]
        + 0.20 * detail["priority_specialisation_component"]
        + 0.25 * detail["priority_market_reach_component"]
        + 0.20 * detail["priority_national_output_multiplier_component"]
        + 0.20 * detail["priority_value_added_component"]
    )
    detail.sort_values("gross_output_mEUR", ascending=False).round(6).to_csv(
        OUTPUT / "rieti_sectoral_indicators_2022.csv", index=False
    )

    pd.Series(destination_provinces, name="intermediate_sales_mEUR").sort_values(
        ascending=False
    ).rename_axis("nuts3_code").round(6).to_csv(
        OUTPUT / "rieti_intermediate_destinations_2022.csv"
    )

    summary = pd.DataFrame(
        {
            "metric": [
                "gross_output_mEUR",
                "intermediate_inputs_mEUR",
                "value_added_mEUR",
                "labour_compensation_mEUR",
                "capital_income_mEUR",
                "taxes_mEUR",
                "local_intermediate_inputs_mEUR",
                "other_lazio_intermediate_inputs_mEUR",
                "rest_italy_intermediate_inputs_mEUR",
                "imported_intermediate_inputs_mEUR",
            ],
            "value": [
                gross_output.sum(),
                intermediate_inputs.sum(),
                (labour + capital).sum(),
                labour.sum(),
                capital.sum(),
                taxes.sum(),
                local_inputs.sum(),
                lazio_inputs.sum(),
                italy_inputs.sum(),
                imported_inputs.sum(),
            ],
        }
    )
    summary.round(6).to_csv(OUTPUT / "rieti_macro_summary_2022.csv", index=False)


if __name__ == "__main__":
    main()
