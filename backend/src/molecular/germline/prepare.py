from io import BytesIO
from typing import BinaryIO

import pandas as pd


def validate_maf(
    maf_df: pd.DataFrame,
) -> None:
    ...


def parse_maf(
    content: BinaryIO,
    extract_glued: bool = True,
) -> pd.DataFrame:
    if isinstance(content, bytes):
        content = BytesIO(content,)

    maf_df = pd.read_csv(content, sep="\t", comment="#", low_memory=False)
    validate_maf(maf_df)

    snp = maf_df.loc[maf_df["Variant_Type"].isin(["SNP", "TNP", "DNP", "ONP"])]

    if extract_glued:
        glued_alterations_as_snp = extract_glued_alterations_as_snp(maf_df)
        snp = pd.concat([snp, glued_alterations_as_snp])

    return snp


def extract_glued_alterations_as_snp(maf_df: pd.DataFrame) -> pd.DataFrame:
    result = []
    for _, row in maf_df.loc[
        maf_df["Variant_Type"].isin({"TNP", "DNP", "ONP"})
    ].iterrows():
        for reference_allele, alternate_allele, coord in zip(
            row["Reference_Allele"],
            row["Allele"],
            range(row["Start_Position"], row["End_Position"] + 1),
        ):
            snp_data = row.to_dict()
            snp_data["Reference_Allele"] = reference_allele
            snp_data["Allele"] = alternate_allele
            snp_data["Start_Position"] = snp_data["End_Position"] = coord
            snp_data["Variant_Type"] = "SNP"
            result.append(snp_data)
    return pd.DataFrame(result)
