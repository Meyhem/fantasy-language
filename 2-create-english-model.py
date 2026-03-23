from collections import Counter, defaultdict
import os
import time

def create_english_model(infile: str, outfile: str) -> None:
    trigram_count = Counter()
    transition_count = defaultdict(Counter)

    total_size = os.path.getsize(infile)
    start_time = time.time()

    with open(infile, 'r', encoding='utf-8') as f:
        text = f.read()
        chars_read = len(text)
        for i in range(len(text) - 3):
            gram1 = text[i:i+3]
            gram2 = text[i+1:i+4]
            trigram_count[gram1] += 1
            transition_count[gram1][gram2] += 1

        elapsed = time.time() - start_time
        print(f"Processed {chars_read} chars in {elapsed:.2f}s")

    lines = []
    for trigram1 in sorted(trigram_count):
        total = trigram_count[trigram1]
        for trigram2, count in sorted(transition_count[trigram1].items()):
            prob = count / total
            lines.append(f"{trigram1}|{trigram2}|{prob:.10f}")

    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    try:
        create_english_model('dataset-english.txt', 'model-english.txt')
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
