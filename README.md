# BioValidator

Automation system for bioinformatic pipelines

### Algorithm for Accessing Open Data

1. Go to the website [https://www.ncbi.nlm.nih.gov/sra](https://www.ncbi.nlm.nih.gov/sra).
2. Enter the sample name in the search field (e.g., СOLO829).
3. In the filter options:
   - In field **File Type** choose **fastq**.
4. Go to the search result.
5. In the **Runs** section:
   - Select one of the runs.
6. Navigate to the **FASTA/FASTQ download** section.
7. Download options:
   - If the run size does not exceed the 5 Gbases limit, download it in fastq format.
   - If it exceeds the limit, download it using the SRA Toolkit.

### Principal Architecture Design

![image](https://github.com/user-attachments/assets/e343b7e4-9e71-4aa3-86ca-50d6b394ccbb)

### Deploying

Build docker images:

```bash
ENV_FILE=.env-dev COMPOSE_FILE=docker-compose.frontend.yml ./scripts/build.sh
```

Deploy application with docker compose:

```bash
ENV_FILE=.env-dev COMPOSE_FILE=docker-compose.frontend.yml ./scripts/deploy.sh
```

### Development

Lint backend):

```bash
ruff check backend/ scripts/
```

Format backend:

```bash
ruff check --fix --unsafe-fixes backend/ scripts/
```

Run backend tests (run it inside backend directory):

```bash
poetry run pytest tests/tests_unit
```
