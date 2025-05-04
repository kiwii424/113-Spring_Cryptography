from collections import Counter
from wordsegment import load, segment
import random

# common words in English
COMMON_WORDS = {"THE", "THERE", "AND", "TO", "OF", "IS", "IN", "THAT", "IT", "ARE", "FOR", "AS", "WITH"}

def index_of_coincidence(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    N = len(text)
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

def detect_language_by_ic(ic):
    language_ranges = [
        ("English", 0.065, 0.070),
        ("French", 0.075, 0.078),
        ("German", 0.074, 0.077),
        ("Spanish", 0.072, 0.075),
        ("Latin", 0.068, 0.071),
        ("Chinese", 0.050, 0.060),
        ("Random or Strongly Encrypted", 0.038, 0.045),
    ]
    for lang, lower, upper in language_ranges:
        if lower <= ic <= upper:
            return f"Most likely to be {lang} (IC ≈ {lower:.3f} ~ {upper:.3f})\n"
    return f"Undefined language or strongly encrypted text (IC = {ic:.5f})\n"

def caesar_decrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base - shift) % 26 + base)
        else:
            result += ch
    return result

def score_english_words(text):
    words = text.split()
    count = sum(1 for w in words if w in COMMON_WORDS)
    return count

def auto_segment(text):
    load()
    filtered = ''.join(ch for ch in text.upper() if ch.isalpha())
    segmented = segment(filtered.lower())
    return ' '.join(segmented)


if __name__ == "__main__":

    with open("ciphertext.txt", mode='r') as file:
        original_text = file.read()
        ciphertext = original_text.replace(" ", "").replace("\n", "").upper()

    ic_value = index_of_coincidence(ciphertext)
    print("\n--- Analyzing the ciphertext ---")
    print(f"Index of Coincidence (IC): {ic_value:.5f}")
    print(detect_language_by_ic(ic_value))

    best_shift = None
    best_score = -1
    best_plaintext = ""
    for shift in range(1, 26):
        decrypted = caesar_decrypt(original_text.upper(), shift)
        score = score_english_words(decrypted.upper())
        if score > best_score:
            best_score = score
            best_shift = shift
            best_plaintext = decrypted

    best_plaintext = auto_segment(best_plaintext)


    print("--- Decrypting the ciphertext ---")
    print(f"Most likely Caesar shift: {best_shift}")

    with open("plaintext.txt", mode = 'w') as file:
        file.write(best_plaintext)

    print("Formatted plaintext saved to plaintext.txt")



