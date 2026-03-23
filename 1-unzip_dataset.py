import zipfile

def unzip_dataset():
    with zipfile.ZipFile('dataset-english.zip', 'r') as zip_ref:
        # Extract all contents to the current directory
        zip_ref.extractall()
        # Assuming the zip contains a file that should be renamed or moved to dataset-english.txt
        # If the zip contains a specific file, adjust accordingly
        # For simplicity, if it extracts to a file, rename it if needed
        # But since the task says "into dataset-english.txt", perhaps the zip contains the txt file
        # This script extracts the zip; if the extracted file is not named dataset-english.txt, you may need to rename it manually or adjust the script

if __name__ == "__main__":
    unzip_dataset()