import dramatiq

from src.db.initdb import sessionmaker
from src.db.repositories.metric import MetricRepository
from src.db.repositories.reference import ReferenceRepository
from src.db.repositories.sample import SampleRepository
from src.entities import MolecularType
from src.logger import logger
from src.molecular.germline.prepare import parse_maf
from src.molecular.germline.validation import GermlineValidation
from src.objstore.base import BaseStore
from src.objstore.paths import get_reference_molecular_file_path, get_sample_molecular_file_path
from src.worker.setup import OBJECT_STORE_KEY, SESSIONMAKER_KEY, WorkerGlobal


@dramatiq.actor(max_retries=0, store_results=True)
def calculate_metrics(sample_names: list[str], version: str) -> None:
    worker_global = WorkerGlobal()

    store: BaseStore = worker_global.get(OBJECT_STORE_KEY)
    sessionfactory: sessionmaker = worker_global.get(SESSIONMAKER_KEY)

    with sessionfactory() as session:
        for sample_name in sample_names:
            metrics_repo = MetricRepository(
                session
            )
            sample_repo = SampleRepository(
                session=session
            )
            sample = sample_repo.get(name=sample_name)

            molecular_file_path = get_sample_molecular_file_path(sample_name, MolecularType.GERMLINE)

            raw_maf = store.download_object(molecular_file_path)
            maf_df = parse_maf(raw_maf)
            del raw_maf

            validator = GermlineValidation(sample, version, maf_df)
            metrics = validator.validate()
            metrics_repo.add_metrics(
                sample_id=sample.id,
                metrics=metrics,
            )


@dramatiq.actor(max_retries=0, store_results=True)
def calculate_reference(reference_name: str, molecular_type: str) -> None:
    molecular_type = MolecularType(molecular_type)

    worker_global = WorkerGlobal()

    store: BaseStore = worker_global.get(OBJECT_STORE_KEY)
    sessionfactory: sessionmaker = worker_global.get(SESSIONMAKER_KEY)

    with sessionfactory() as session:
        reference_repo = ReferenceRepository(
            session
        )

        reference_path = get_reference_molecular_file_path(
            reference_name=reference_name,
            molecular_type=molecular_type,
        )
        logger.info(f"Write file reference: '{reference_name}' to the path: '{reference_path}'")
        file_content = store.download_object(reference_path)

        maf_df = parse_maf(file_content)

        reference_repo.add_mutations(
            name=reference_name,
            mutations_df=maf_df,
        )
