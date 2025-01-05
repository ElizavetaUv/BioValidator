

def drop_multi_allelic_calls():
    input_file_name = '/home/user877/study/BioValidator/data/NA12877.vcf'
    output_file_name = '/home/user877/study/BioValidator/data/NA12877_output.vcf'
    with open(input_file_name, "rt") as input_file:
        with open(output_file_name, "wt") as output_file:
            for row in input_file:
                values = row.split("\t")
                is_multi_allelic_call = values[-1].strip() in ["1|2", "2|1"]
                if is_multi_allelic_call:
                        output_file.write(row)
