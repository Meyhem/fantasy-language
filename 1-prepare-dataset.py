import json
import re

def process_dataset(infile_path, outfile_path):
    with open(infile_path, 'r', encoding='utf-8') as infile, \
         open(outfile_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                text = obj.get('text', '')
                # Remove punctuation and special chars, keep only lowercase alpha
                cleaned = re.sub(r'[^a-z]', '', text.lower())
                # Write without newlines
                outfile.write(cleaned)
            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue

if __name__ == '__main__':
    try:
        process_dataset('dataset-raw.json', 'dataset-english.txt')
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
