# unzip Data from "collectiondedocuments" and copy in "Data" folder
# -----------------
import os
import gzip
import shutil

# Define paths
folder_path = r'TRECAP88-90' 
collection_folder_name = 'collection-de-documents' 
data_folder_name = 'data'

# Path to the collection folder
collection_folder_path = os.path.join(folder_path, collection_folder_name)

# Path to the data folder
data_folder_path = os.path.join(folder_path, data_folder_name)

# Ensure the data folder exists, create it if not
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

# List files in the collection folder
collection_files = os.listdir(collection_folder_path)

# Iterate over each file in the collection folder
for file_name in collection_files:
    # Check if the file is a gzip file
    if file_name.endswith('.gz'):
        # Construct the full path to the gzip file
        gzip_file_path = os.path.join(collection_folder_path, file_name)

        # Create a folder in the data directory with the same name as the gzip file (without extension)
        unzip_folder_path = os.path.join(data_folder_path, os.path.splitext(file_name)[0])

        # Ensure the unzip folder exists, create it if not
        if not os.path.exists(unzip_folder_path):
            os.makedirs(unzip_folder_path)

        # Extract the contents of the gzip file to the new folder
        with gzip.open(gzip_file_path, 'rb') as gz_file:
            # Construct the path to the output file
            output_file_path = os.path.join(unzip_folder_path, os.path.splitext(file_name)[0])

            # Write the decompressed content to the new file
            with open(output_file_path, 'wb') as output_file:
                shutil.copyfileobj(gz_file, output_file)

# Now, the contents of the gzip files are extracted to the "data" folder

# -------

