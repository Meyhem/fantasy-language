from collections import Counter, defaultdict, deque
import os
import time

def create_english_model(infile: str, outfile: str) -> None:
    trigram_count = Counter()
    transition_count = defaultdict(Counter)

    total_size = os.path.getsize(infile)
    chars_read = 0
    start_time = time.time()
    last_log = start_time

    buffer = deque(maxlen=4)
    with open(infile, 'r', encoding='utf-8') as f:
        while True:
            char = f.read(1)
            if not char:
                break
            chars_read += 1
            buffer.append(char)
            if len(buffer) == 4:
                trigram1 = ''.join(buffer)[:3]
                trigram2 = ''.join(buffer)[1:4]
                trigram_count[trigram1] += 1
                transition_count[trigram1][trigram2] += 1

            current_time = time.time()
            if current_time - last_log >= 10:
                progress = (chars_read / total_size) * 100 if total_size > 0 else 100
                print(f"Progress: {progress:.2f}% ({chars_read}/{total_size} chars, {len(trigram_count)} trigrams)")
                last_log = current_time

    with open(outfile, 'w', encoding='utf-8') as f:
        for trigram1 in sorted(trigram_count):
            total = trigram_count[trigram1]
            for trigram2, count in sorted(transition_count[trigram1].items()):
                prob = count / total
                f.write(f"{trigram1}|{trigram2}|{prob:.10f}\n")

if __name__ == '__main__':
    try:
        create_english_model('dataset-english.txt', 'model-english.model')
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
