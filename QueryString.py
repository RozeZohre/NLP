import os

def create_text_file_with_xml_format(text_content):
    text_content_with_tags = f"<DOC>\n<TEXT>\n{text_content}\n</TEXT>\n</DOC>"

    output_directory = "TRECAP88-90/DataForQuery"
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, "QueryString.txt")
    with open(output_path, "w") as file:
        file.write(text_content_with_tags)
        print(output_directory)

# Ask for query type
query_type = input("Is it a 'short' query (s) or 'long' query (l)? ").lower()

# Process based on the query type
if query_type == 's':
    # For short query, receive a single string
    user_input = input("Enter the string for <TEXT>: ")
    create_text_file_with_xml_format(user_input)
elif query_type == 'l':
    # For long query, receive two strings and merge them
    first_string = input("Enter the first string for <TEXT>: ")
    second_string = input("Enter the second string for <TEXT>: ")
    merged_text = f"{first_string} {second_string}"
    create_text_file_with_xml_format(merged_text)
else:
    print("Invalid input. Please enter 's' for short query or 'l' for long query.")
