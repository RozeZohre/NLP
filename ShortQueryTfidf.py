import os
import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import FSDirectory
from java.nio.file import Paths
from org.apache.lucene.search.similarities import ClassicSimilarity  # Use ClassicSimilarity
from contextlib import closing
import re

# Initialize the Java VM
lucene.initVM()

index_path = Paths.get("TRECAP88-90/indexed")
topics_path = "TRECAP88-90/Topics-requetes/output"
output_path = "TRECAP88-90/collectiondedocuments/results.txt"

try:
    # Ensure the index directory contains Lucene segments
    if not os.path.exists(str(index_path)):
        raise FileNotFoundError(f"Index directory not found: {index_path}")

    with closing(DirectoryReader.open(FSDirectory.open(index_path))) as reader:
        # Use ClassicSimilarity for TF-IDF-like weighting
        searcher = IndexSearcher(reader)
        searcher.setSimilarity(ClassicSimilarity())  # Use ClassicSimilarity

        analyzer = StandardAnalyzer()

        # Open the output file for writing
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for filename in os.listdir(topics_path):
                if filename.endswith(".txt"):
                    # Build the full path to the text file
                    text_path = os.path.join(topics_path, filename)

                    try:
                        # Read the content of the text file
                        with open(text_path, 'r', encoding='utf-8') as file:
                            content = file.read()

                        # Use regex to extract the content inside the <num> and <dom> tags
                        num_match = re.search(r'<num> Number: (.+?)\n\n<dom> Domain:', content, re.DOTALL)

                        if num_match:
                            num_info = num_match.group(1).strip()

                            # Extract the domain information
                            domain_match = re.search(r'<dom> Domain: (.+?)\n\n<title> Topic:', content, re.DOTALL)
                            if domain_match:
                                domain_info = domain_match.group(1).strip()

                                # Combine num and domain info
                                query_string = f"{int(num_info)} {domain_info}"

                                # Perform the search
                                query = QueryParser("content", analyzer).parse(query_string)
                                hits = searcher.search(query, 1000)  # Return top 1000 results

                                # Write the results to the output file with a different run name for each column
                                column_counter = 1
                                for hit in hits.scoreDocs:
                                    doc = searcher.doc(hit.doc)
                                    document_id = doc.get("documentI")

                                    # Use zfill to pad document_id with zeros to a width of 2
                                    output_file.write(f"{int(num_info)} 0 {document_id.zfill(2)} 1 {hit.score:.2f} run_{column_counter}\n")
                                    column_counter += 1

                    except Exception as e:
                        print(f"An error occurred processing file '{text_path}': {e}")

except Exception as e:
    print(f"An error occurred: {e}")

