import hashlib

import requests

url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"
local_file = "problem2/password.txt"


# Attempt to download the password list and save it locally
try:
    response = requests.get(url)
    response.raise_for_status()
    with open(local_file, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Password list downloaded and saved to {local_file}\n")
except requests.exceptions.RequestException as e:
    print(f"Failed to download password list: {e}\n")


# Load all passwords into a list
with open(local_file, "r", encoding="utf-8", errors="ignore") as f:
    passwords = [line.strip() for line in f]


# Function to compute SHA-1 hash of a string
def sha1(text):
    return hashlib.sha1(text.encode()).hexdigest()


# Dictionary of target SHA-1 hashes with optional salt values
targets = {
    "db3ae03df555104cd021c6308d5d11cfa40aac41": {"salt": None},
    "884950a05fe822dddee8030304783e21cdc2b246": {"salt": None},
    "9b467cbabe4b44ce7f34332acc1aa7305d4ac2ba": {"salt": None},
    "9d6b628c1f81b4795c0266c0f12123c1e09a7ad3": {
        "salt": "dfc3e4f0b9b5fb047e9be9fb89016f290d2abb06"
    }
}

# Brute-force password cracking loop
for target_hash, info in targets.items():
    salt = info["salt"]
    found = False

    # If salt is provided, use a two-step hash chaining process
    if salt:
        for i, a in enumerate(passwords, start=1):
            if sha1(a) == salt:
                for j, b in enumerate(passwords, start=1):
                    if sha1(a + b) == target_hash:
                        print(f"Hash: {target_hash}")
                        print(f"Password: {a} + {b}")
                        print(f"Took {j} attempts to crack message.\n")
                        found = True
                        break
                break

    # No salt: directly hash each password and compare
    else:
        for i, pwd in enumerate(passwords, start=1):
            if sha1(pwd) == target_hash:
                print(f"Hash: {target_hash}")
                print(f"Password: {pwd}")
                print(f"Took {i} attempts to crack message.\n")
                found = True
                break

    # If nothing matches
    if not found:
        print(f"Hash: {target_hash} not cracked.\n")


# ----- chatgpt code -----
# for hashval, info in targets.items():
#     attempts = 0
#     salt = info["salt"]
#     found = False
#     for pwd in passwords:
#         attempts += 1
#         if salt:
#             candidate = salt + pwd
#         else:
#             candidate = pwd
#         hashed = hashlib.sha1(candidate.encode()).hexdigest()
#         if hashed == hashval:
#             print(f"Hash: {hashval}")
#             print(f"Password: {pwd}")
#             print(f"Took {attempts} attempts to crack message.\n")
#             found = True
#             break
#     if not found:
#         print(f"Hash: {hashval} not cracked.\n")
