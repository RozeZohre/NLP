import os
import shutil
import xml.etree.ElementTree as ET
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

def process_text(text):
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens if word.lower() not in stop_words]

    # Stemming
    # stemmer = PorterStemmer()
    # tokens = [stemmer.stem(word) for word in tokens]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)

def process_folder(folder_path, pretrained_folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            print(f"\n\nTree {tree}\n\n")
            root = tree.getroot()
            print(f"\n\nRoot element: {root}\n\n")

            # Process each <DOC> section separately
            for doc_element in root.iter("DOC"):
                # Extract text content from XML elements within the <DOC> section
                all_text = ""
                for element in doc_element.iter():
                    if element.text and not any(e.tag in element.tag for e in element):
                        all_text += element.text + " "

                # Process text (remove stop words, stemming, lemmatization)
                processed_text = process_text(all_text)

                # Save the processed text
                doc_id = doc_element.findtext("DOCNO").strip()
                pretrained_file_path = os.path.join(pretrained_folder_path, f"{doc_id}_pretrained.txt")
                with open(pretrained_file_path, "w", encoding="utf-8") as pretrained_file:
                    pretrained_file.write(processed_text)

        except ET.ParseError as parse_error:
            print(f"Skipping file {file_path} due to XML parsing error: {parse_error}")

# Define paths
project_folder_path = "TRECAP88-90"
data_folder_path = os.path.join(project_folder_path, "DataForQuery")
pretrained_folder_path = os.path.join(project_folder_path, "PretrainedFilesForQuery")
print ()
# Ensure the PretrainedFiles folder exists, create it if not
if not os.path.exists(pretrained_folder_path):
    os.makedirs(pretrained_folder_path)

# Start processing the data folder
for folder_name in os.listdir(data_folder_path):
    folder_path = os.path.join(data_folder_path, folder_name)
    process_folder(folder_path, pretrained_folder_path)
