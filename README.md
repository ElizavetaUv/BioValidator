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
