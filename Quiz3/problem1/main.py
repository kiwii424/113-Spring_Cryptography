from hashlib import shake_128

def derive_keystream(key, length):
    return shake_128(key.encode()).digest(length)

def encrypt(plaintext, key):
    keystream = derive_keystream(key, len(plaintext))
    return bytes([p ^ k for p, k in zip(plaintext.encode(), keystream)])

def decrypt(ciphertext, key):
    keystream = derive_keystream(key, len(ciphertext))
    return bytes([c ^ k for c, k in zip(ciphertext, keystream)]).decode()


if __name__ == "__main__":
    key = "mypassword"
    plaintext = "HELLO WORLD"

    # Encrypt the plaintext
    ciphertext = encrypt(plaintext, key)
    print("Ciphertext:", ciphertext)

    # Decrypt the ciphertext
    decrypted_text = decrypt(ciphertext, key)
    print("Decrypted text:", decrypted_text)

    # Check if the decrypted text matches the original plaintext
    assert decrypted_text == plaintext, "Decryption failed!"
    print("Decryption successful!")

