from db.initdb import init, get_engine
from db.db_interface import add_sample, add_reference, add_mutations
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import pandas as pd


def test_add_mutations() -> None:
    maf_file_path = Path('./data/test_maf_output/HG00098.maf')
    mutations_file = pd.read_csv(maf_file_path, sep='\t')
    mutations_data = mutations_file[
        ['Hugo_Symbol', 'Variant_Type', 'Reference_Allele', 'Chromosome', 'Start_Position', 'End_Position']
    ]

    init()
    engine = get_engine()
    Session = sessionmaker(engine)

    sample_name, _ = maf_file_path.name.split(".", maxsplit=1)

    with Session() as session:
        sample = add_sample(session, sample_name)

    # with Session.begin() as session:
        reference = add_reference(session, reference_name=sample_name, sample_id=sample.id)

    # with Session.begin() as session:
        add_mutations(session, mutations_data=mutations_data, reference_id=reference.id)


test_add_mutations()