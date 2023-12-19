import lucene
import os
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory

# Initialize Lucene VM
env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Index directory setup
index_path = os.path.join("TRECAP88-90", "indexed")                                                                   
fsDir = MMapDirectory(Paths.get(index_path))

# Index writer configuration
writerConfig = IndexWriterConfig(StandardAnalyzer())
writer = IndexWriter(fsDir, writerConfig)

# Define field type for content
contentFieldType = FieldType()
contentFieldType.setStored(False)
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
    doc = Document()
    doc.add(Field('documentI', doc_id, doc_id_field_type))  # Add the document ID field
    doc.add(Field('content', content, doc_id_field_type))
    writer.addDocument(doc)
    #print (f"Document ID: {doc_id}\n\nDocument content: {content}")
    print (f"Document ID: {doc_id}\n")
  

# Iterate over all files in the specified directory
directory_path = 'TRECAP88-90/PretrainedFiles'
for root, dirs, files in os.walk(directory_path):

    for file_name in files:
        # print(file_name)
        file_path = os.path.join(root, file_name)
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            lines = file.read()
            if lines:
                doc_id = lines.split(' ') 
                doc_id = doc_id[0]
                # doc_id = lines[0:10].strip()  # Assuming the document ID is the first line
                content = ''.join(lines[1:])  # Co
                
                add_document(writer, doc_id, content)
    writer.close()
