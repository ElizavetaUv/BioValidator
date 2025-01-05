from src.entities import MolecularType

SAMPLES_OBJECTS = "samples"


def get_molecular_file_path(sample_name: str, molecular_type: MolecularType) -> str:
    return f"{SAMPLES_OBJECTS}/{sample_name}/{molecular_type.value}"
