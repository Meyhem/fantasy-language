import random
import argparse
from collections import defaultdict

def load_model(filename):
    model = defaultdict(dict)
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            source, target, prob_str = line.split('|')
            prob = float(prob_str)
            model[source][target] = prob
    return model

def generate_text(model, length=100):
    # Start with a random trigram
    start_trigrams = list(model.keys())
    if not start_trigrams:
        return ""
    current = random.choice(start_trigrams)
    result = current

    for _ in range(length - 3):
        if current not in model:
            break
        next_trigrams = list(model[current].keys())
        if not next_trigrams:
            break
        weights = [model[current][t] for t in next_trigrams]
        next_trigram = random.choices(next_trigrams, weights=weights)[0]
        result += next_trigram[-1]  # append last char
        current = next_trigram

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate text using Markov trigram model')
    parser.add_argument('filename', nargs='?', default='model-english.txt', help='Model file path (default: model-english.txt)')
    parser.add_argument('length', nargs='?', type=int, default=100, help='Number of characters to generate (default: 100)')
    args = parser.parse_args()

    model = load_model(args.filename)
    sentence = generate_text(model, args.length)
    print(sentence)
