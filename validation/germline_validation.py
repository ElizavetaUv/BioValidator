
from dataclasses import dataclass
from typing import List

import pandas as pd
import db_interface
import model
from validation.objects import Sample, converter


@dataclass
class GermlineValidation :
    sample: Sample
    input_maf: pd.Dataframe # may be better to use Table

    def validate(self) -> List[model.Metric]: 
        ...


if __name__ == "__main__":
    # with session
    sample = converter(db_interface.get_sample(name)) # TODO get_sample add to db_interface, name is a str with sample name to be validated
    input_maf = parse(maf_path: Path) # TODO write parser to parse any maf to Dataframe
    germline_validation = GermlineValidation(sample, input_maf)
    metrics = germline_validation.validate()
    # with session
    db_interface.add_metrics(sample_name: str, metrics: List[Metric])
