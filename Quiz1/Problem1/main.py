import os
import matplotlib.pyplot as plt
from collections import Counter
import string
import math


def read_file(file_path):
    """Read ciphertext from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def analyze_frequencies(text):
    """Analyze character frequencies in the text using Counter."""
    # Count occurrences of each character
    char_counts = Counter(text)

    # Calculate total characters
    total_chars = sum(char_counts.values())

    # Calculate frequency percentage for each character
    freq_dict = {char: (count / total_chars) * 100 for char, count in char_counts.items()}

    # Sort by frequency (descending)
    sorted_freq = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_freq, char_counts



def visualize_frequencies(freq_data, title="Character Frequencies"):
    """Create a bar chart visualization of character frequencies."""
    chars = [char for char, _ in freq_data]
    freqs = [freq for _, freq in freq_data]

    plt.figure(figsize=(15, 8))
    plt.bar(chars, freqs)
    plt.title(title)
    plt.xlabel('Characters')
    plt.ylabel('Frequency (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("frequency_analysis.png")
    plt.close()

    return "frequency_analysis.png"


def create_mapping_table(ciphertext_freq, english_freq_dict):
    """Create a mapping table from ciphertext characters to plaintext characters."""
    # Map characters based on frequency ranking
    mapping = {}
    for (cipher_char, _), plain_char in zip(ciphertext_freq, english_freq_dict):
        mapping[cipher_char] = plain_char

    return mapping


def apply_mapping(ciphertext, mapping):
    """Apply the mapping to decrypt the ciphertext."""
    plaintext = ""
    for char in ciphertext:
        if char in mapping:
            plaintext += mapping[char]
        else:
            plaintext += char  # Keep unmapped characters as is

    return plaintext

def main():


    ciphertext_path = "ciphertext.txt"

    ciphertext = read_file(ciphertext_path)

    if ciphertext is None :
        raise ValueError("無法讀取")


    # Analyze the frequencies using Counter
    cipher_freq, char_counts = analyze_frequencies(ciphertext)


    # Write all frequencies to a file
    with open("all_frequencies.txt", "w", encoding="utf-8") as freq_file:
        for char, count in char_counts.most_common():
            frequency = (count / sum(char_counts.values())) * 100
            freq_file.write(f"'{char}': {count} occurrences ({frequency:.2f}%)\n")

    print("\nAll character frequencies saved to 'all_frequencies.txt'")

    # Create a visualization
    visualization_path = visualize_frequencies(cipher_freq, "Ciphertext Character Frequencies")
    print(f"Frequency visualization saved to '{visualization_path}'")



    order = " etonsairhdlucfmpg,bwyv.HASCFLTGWkPj;x:RI-BJNqOMzD7E416'KQ&UXZVY\n"


    # Create the mapping table
    mapping = create_mapping_table(cipher_freq, order)

    # -------------------Print the mapping table-------------------------
    # print("\nTable 1: Mapping from Ciphertext to Plaintext")
    # print("=" * 50)
    # print("| Ciphertext | Plaintext |")
    # print("|" + "-" * 11 + "|" + "-" * 10 + "|")

    ## Sort by ASCII value for better readability
    # for cipher_char in sorted(mapping.keys()):
    #     plain_char = mapping[cipher_char]
    #     print(f"| {cipher_char:<10} | {plain_char:<9} |")
    # -------------------------------------------------------------------

    # Apply the mapping to get plaintext
    plaintext = apply_mapping(ciphertext, mapping)

    # Save the plaintext to a file
    with open("decrypted_plaintext.txt", "w", encoding="utf-8") as f:
        f.write(plaintext)
    print("Full plaintext saved to 'decrypted_plaintext.txt'")

    # Save the mapping table to a file
    with open("mapping_table.txt", "w", encoding="utf-8") as f:
        f.write("Ciphertext | Plaintext\n")
        f.write("-" * 22 + "\n")
        for cipher_char in sorted(mapping.keys()):
            f.write(f"{cipher_char} | {mapping[cipher_char]}\n")
            ascii_value = ord(mapping[cipher_char])

            result_ascii = (17 * ascii_value + 45) % 95 + 32

            result_char = chr(result_ascii)

            if result_char != cipher_char: print("wrong")


    print("Mapping table saved to 'mapping_table.txt'")


    # -------------------Print sample of plaintext ----------------------
    print("\nSample of decrypted plaintext:")
    print("-" * 50)
    print(plaintext[:200] + "..." if len(plaintext) > 200 else plaintext)
    print("\n")
    # ---------------------------------------------



if __name__ == "__main__":
    main()
