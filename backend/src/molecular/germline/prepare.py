# from pathlib import Path
from io import BytesIO
from typing import BinaryIO

import pandas as pd

# USE_GENE_STORAGE = CONFIG["common"]["use_gene_storage"]


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
    # add hg38 or another version

    # if USE_GENE_STORAGE and "Hugo_Symbol" in data:
    #     gene_storage_requester = GeneStorageRequester(GENE_STORAGE_HOST)
    #     genes = gene_storage_requester.get_genes(set(data["Hugo_Symbol"]))
    #     data["Hugo_Symbol"] = data["Hugo_Symbol"].apply(
    #         lambda x: genes[x].name
    #         if x in genes.keys() and genes[x].name != genes[x].nameQuery
    #         else x
    #     )

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


def validate_mutations(content: bytes) -> None:
    ...


def calculate_mutations() -> None:
    ...
