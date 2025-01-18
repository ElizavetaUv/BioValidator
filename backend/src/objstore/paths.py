from src.entities import MolecularType

SAMPLES_OBJECTS = "samples"
REFERENCES_OBJECTS = "references"


def get_sample_molecular_file_path(sample_name: str, molecular_type: MolecularType) -> str:
    return f"{SAMPLES_OBJECTS}/{sample_name}/{molecular_type.value}"


def get_reference_molecular_file_path(reference_name: str, molecular_type: MolecularType) -> str:
    return f"{REFERENCES_OBJECTS}/{reference_name}/{molecular_type.value}"
