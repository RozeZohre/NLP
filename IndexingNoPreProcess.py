import lucene
import os
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory
import re

# Initialize Lucene VM
env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Index directory setup
index_path = os.path.join("TRECAP88-90", "indexed2")
fsDir = MMapDirectory(Paths.get(index_path))

# Index writer configuration
writerConfig = IndexWriterConfig(StandardAnalyzer())
writer = IndexWriter(fsDir, writerConfig)

# Define field type for content
contentFieldType = FieldType()
contentFieldType.setStored(True)  # Store the content in the index
contentFieldType.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

# Define field type for document ID
docIdFieldType = FieldType()
docIdFieldType.setStored(True)  # Store the document ID in the index
docIdFieldType.setIndexOptions(IndexOptions.NONE)  # Do not index the document ID

# Function to add a document to the index
def add_document(writer, doc_id, content):
    doc_id_field_type = FieldType()
    doc_id_field_type.setStored(True)
    doc_id_field_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    # Remove spaces from the doc_id
    doc_id = doc_id.replace(" ", "")

    doc = Document()
    doc.add(Field('documentI', doc_id, doc_id_field_type))  # Add the document ID field
    doc.add(Field('content', content, contentFieldType))
    writer.addDocument(doc)
    print(f"Document ID: {doc_id} - Content added to the index.")
    print(f"Document ID: {content} - Content added to the index.")
# Specify the directory path
directory_path = 'TRECAP88-90/PretrainedFiles2'

# Get the list of files in the directory
files = os.listdir(directory_path)

# Process all files if files exist
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        # Read the content of the file
        content = file.read()

        # Use the regular expression pattern to extract Document ID
        pattern = re.compile(r'\bAP\d{6}-\d{4}\b')
        match = re.search(pattern, content)

        # Extract the Document ID
        doc_id = match.group().replace(" ", "") if match else ''

        # Add the document to the Lucene index
        add_document(writer, doc_id, content)
        
# Close the Lucene index writer
writer.close()
