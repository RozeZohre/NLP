import os

input_directory = 'TRECAP88-90/jugementsDePertinence'
output_file_path = 'TRECAP88-90/jugementsDePertinence/judgments'

# List of input files
input_files = ['qrels.1-50.AP8890.txt', 'qrels.51-100.AP8890.txt', 'qrels.101-150.AP8890.txt']

# Open the output file for writing
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for input_file in input_files:
        input_file_path = os.path.join(input_directory, input_file)
        with open(input_file_path, 'r', encoding='utf-8') as input_content:
            # Read the content of each input file and write it to the output file
            output_file.write(input_content.read())

print(f'Merged content from {len(input_files)} files into {output_file_path}.')

