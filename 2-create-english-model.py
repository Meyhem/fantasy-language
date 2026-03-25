from collections import Counter, defaultdict
import os
import time

def create_english_model(infile: str, outfile: str) -> None:
    trigram_count = Counter()
    transition_count = defaultdict(Counter)

    total_size = os.path.getsize(infile)
    start_time = time.time()
    last_print = start_time

    with open(infile, 'r', encoding='utf-8') as f:
        text = f.read()
        chars_read = len(text)
        for i in range(len(text) - 3):
            gram1 = text[i:i+3]
            gram2 = text[i+1:i+4]
            trigram_count[gram1] += 1
            transition_count[gram1][gram2] += 1

            # Progress reporting every 5 seconds
            current_time = time.time()
            if current_time - last_print >= 5:
                unique_trigrams = len(trigram_count)
                processed_chars = i + 3
                total_chars = len(text)
                percentage = (processed_chars / total_chars) * 100 if total_chars > 0 else 0
                print(f"Unique trigrams: {unique_trigrams}, Processed chars: {processed_chars:.0e} / {total_chars:.0e}, {percentage:.2f}%")
                last_print = current_time

        elapsed = time.time() - start_time
        print(f"Processed {chars_read} chars in {elapsed:.2f}s")

    # Calculate total occurrences and select top trigrams for 99%
    total_occurrences = sum(trigram_count.values())
    sorted_trigrams = sorted(trigram_count.items(), key=lambda x: x[1], reverse=True)

    # Write all trigrams and their counts to model-counts-english.txt
    with open('model-counts-english.txt', 'w', encoding='utf-8') as f:
        for trigram, count in sorted_trigrams:
            f.write(f"{trigram}|{count}\n")

    cumulative = 0
    selected_trigrams = set()
    for trigram, count in sorted_trigrams:
        cumulative += count
        selected_trigrams.add(trigram)
        if cumulative >= 0.99 * total_occurrences:
            break

    # Clean transition_count: remove transitions <1% prob for selected trigrams
    removed_count = 0
    total_trans_before = 0
    for trigram1 in selected_trigrams:
        total_trans_before += len(transition_count[trigram1])
        total_original = trigram_count[trigram1]
        to_remove = []
        for trigram2 in transition_count[trigram1]:
            count = transition_count[trigram1][trigram2]
            if count / total_original < 0.01:
                to_remove.append(trigram2)
        removed_count += len(to_remove)
        for trigram2 in to_remove:
            del transition_count[trigram1][trigram2]

    lines = []
    for trigram1 in sorted(selected_trigrams):
        new_total = sum(transition_count[trigram1].values())
        if new_total == 0:
            continue
        for trigram2, count in sorted(transition_count[trigram1].items()):
            prob = count / new_total
            lines.append(f"{trigram1}|{trigram2}|{prob:.10f}")

    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    # Print stats
    total_found = len(trigram_count)
    used = len(selected_trigrams)
    print(f"Total trigrams found: {total_found}")
    print(f"Removed {removed_count} low-probability transitions out of {total_trans_before} transitions")
    print(f"Exporting {used} trigrams")

if __name__ == '__main__':
    try:
        create_english_model('dataset-english.txt', 'model-english.txt')
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
