import os
import xml.etree.ElementTree as ET
import nltk
from nltk.tokenize import words_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

def process_text(text):

    # tokenization
    words = words_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = words
    tokens = [word for word in tokens if word.lower() not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)

def process_doc(doc_element, pretrained_folder_path):
    # Extract text content from XML elements within the <DOC> section
    all_text = ""
    for element in doc_element.iter():
        if element.text and not any(e.tag in element.tag for e in element):
            all_text += element.text + " "

    # Process text (remove stop words, lemmatization)
    processed_text = process_text(all_text)

    # Save the processed text
    doc_id = doc_element.findtext("DOCNO").strip()
    pretrained_file_path = os.path.join(pretrained_folder_path, f"{doc_id}_pretrained.txt")
    with open(pretrained_file_path, "w", encoding="utf-8") as pretrained_file:
        pretrained_file.write(processed_text)

def process_file(file_path, pretrained_folder_path):
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Find all occurrences of <DOC> and </DOC> tags
        start_indices = [pos for pos, char in enumerate(file_content) if file_content.startswith("<DOC>", pos)]
        end_indices = [pos + len("</DOC>") for pos, char in enumerate(file_content) if file_content.startswith("</DOC>", pos)]

        # Process each <DOC> section separately
        for start_index, end_index in zip(start_indices, end_indices):
            xml_content = file_content[start_index:end_index]
            tree = ET.ElementTree(ET.fromstring(xml_content))
            root = tree.getroot()

            # Process each <DOC> section
            for doc_element in root.iter("DOC"):
                process_doc(doc_element, pretrained_folder_path)
    except ET.ParseError as parse_error:
        print(f"Skipping file {file_path} due to XML parsing error: {parse_error}")
    except Exception as e:
        print(f"Skipping file {file_path} due to an unexpected error: {e}")
        

def process_folder(folder_path, pretrained_folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        process_file(file_path, pretrained_folder_path)

# Define paths
project_folder_path = "TRECAP88-90"
data_folder_path = os.path.join(project_folder_path, "Data")
pretrained_folder_path = os.path.join(project_folder_path, "PretrainedFiles")
print(f"data_folder_path:{data_folder_path}")

# Ensure the PretrainedFiles folder exists, create it if not
if not os.path.exists(pretrained_folder_path):
    os.makedirs(pretrained_folder_path)

# Start processing the data folder
for folder_name in os.listdir(data_folder_path):
    folder_path = os.path.join(data_folder_path, folder_name)
    process_folder(folder_path, pretrained_folder_path)

print("Preprocessing completed.")
