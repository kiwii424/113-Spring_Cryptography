import string
from collections import Counter
from wordsegment import load, segment

freqMap = {
    'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.13,
    'F': 0.022, 'G': 0.02, 'H': 0.061, 'I': 0.07, 'J': 0.0015,
    'K': 0.0077, 'L': 0.04, 'M': 0.024, 'N': 0.067, 'O': 0.075,
    'P': 0.019, 'Q': 0.00095, 'R': 0.06, 'S': 0.063, 'T': 0.091,
    'U': 0.028, 'V': 0.0098, 'W': 0.024, 'X': 0.0015, 'Y': 0.02,
    'Z': 0.00074
}

def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def split_into_groups(text, key_len):
    return [text[i::key_len] for i in range(key_len)]

def chi_squared_stat(text):
    N = len(text)
    counter = Counter(text)
    chi_sq = 0
    for letter in string.ascii_uppercase:
        observed = counter.get(letter, 0)
        expected = freqMap[letter] * N
        chi_sq += (observed - expected) ** 2 / expected if expected > 0 else 0
    return chi_sq

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - 65 - shift) % 26 + 65) for c in text)

def best_caesar_shift(text):
    scores = [(shift, chi_squared_stat(caesar_decrypt(text, shift))) for shift in range(26)]
    best_shift = min(scores, key=lambda x: x[1])[0]
    return best_shift

def index_of_coincidence(text):
    N = len(text)
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1)) if N > 1 else 0
    return ic

def find_key_length(ciphertext, max_key_len=8):
    ic_values = []
    for key_len in range(1, max_key_len):
        groups = split_into_groups(ciphertext, key_len)
        avg_ic = sum(index_of_coincidence(group) for group in groups) / len(groups)
        ic_values.append((key_len, avg_ic))
    best = max(ic_values, key=lambda x: x[1])
    print(f"The most probable key length: {best[0]}, IC: {best[1]:.5f}")
    return best[0]

def decrypt_vigenere(ciphertext):
    clean = clean_text(ciphertext)
    key_len = find_key_length(clean)
    groups = split_into_groups(clean, key_len)
    key_shifts = [best_caesar_shift(group) for group in groups]
    key = ''.join(chr(65 + s) for s in key_shifts)

    plaintext = ""
    for i, c in enumerate(clean):
        shift = key_shifts[i % key_len]
        plain_char = chr((ord(c) - 65 - shift) % 26 + 65)
        plaintext += plain_char

    return key, plaintext

def auto_segment(text):
    load()
    filtered = ''.join(ch for ch in text.upper() if ch.isalpha())
    segmented = segment(filtered.lower())
    return ' '.join(segmented)

if __name__ == "__main__":
    with open("Ciphertext.txt", 'r') as f:
        ciphertext = f.read()

    key, plaintext = decrypt_vigenere(ciphertext)
    formatted_text = auto_segment(plaintext)

    with open("plaintext.txt", "w") as out:
        out.write(formatted_text)

    print("Key:", key)
    print("Formatted plaintext saved to plaintext.txt")
