import os
import re

input_file_path = "TRECAP88-90/Topics-requetes/topics.101-150.txt"
output_directory = "TRECAP88-90/Topics-requetes/output"

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Read the input file
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Use regex to find and extract each <top>...</top> block
topic_blocks = re.findall(r'<top>.*?</top>', content, re.DOTALL)

# Process each topic block
for topic_block in topic_blocks:
    # Extract the topic number
    match = re.search(r'<num> Number: (\d+)', topic_block)
    if match:
        topic_number = match.group(1)
        
        # Create output file path based on the topic number with a .txt extension
        output_file_path = os.path.join(output_directory, f"topic_{topic_number}.txt")
        
        # Write the relevant content to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Write the extracted content to the text file
            output_file.write(topic_block)

print("Topics extracted and saved to individual text files.")
