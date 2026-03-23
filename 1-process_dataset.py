import json
import re

def process_dataset():
    with open('dataset-raw.json', 'r', encoding='utf-8') as infile, \
         open('dataset-english.txt', 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                text = obj.get('text', '')
                # Remove punctuation and special chars, keep only lowercase alpha
                cleaned = re.sub(r'[^a-z ]', ' ', text.lower())
                cleaned = re.sub(r'\s+', ' ', cleaned)
                # Write without newlines
                outfile.write(cleaned + ' ')
            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue

if __name__ == '__main__':
    process_dataset()