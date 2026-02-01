import hashlib
import re
import os
from datetime import datetime

# Kali default wordlist
DEFAULT_WORDLIST = "/usr/share/wordlists/rockyou.txt"

OUTPUT_FILE = "crack_results.txt"


def identify_hash(hash_value):
    hash_value = hash_value.lower()

    if re.fullmatch(r"[a-f0-9]{32}", hash_value):
        return "md5"
    elif re.fullmatch(r"[a-f0-9]{40}", hash_value):
        return "sha1"
    elif re.fullmatch(r"[a-f0-9]{64}", hash_value):
        return "sha256"
    else:
        return None


def hash_word(word, hash_type):
    word = word.encode()

    if hash_type == "md5":
        return hashlib.md5(word).hexdigest()
    elif hash_type == "sha1":
        return hashlib.sha1(word).hexdigest()
    elif hash_type == "sha256":
        return hashlib.sha256(word).hexdigest()


def crack_hash():
    HASH_TO_CRACK = input("Enter hash: ").strip().lower()
    HASH_TYPE = identify_hash(HASH_TO_CRACK)

    if HASH_TYPE is None:
        print("[!] Unknown or unsupported hash type")
        return

    use_default = input("Use Kali default wordlist? (y/n): ").lower()

    if use_default == "y":
        wordlist = DEFAULT_WORDLIST
    else:
        wordlist = input("Enter full path to your wordlist: ").strip()

    if not os.path.isfile(wordlist):
        print("[-] Wordlist file not found!")
        return

    print("\n[*] Hash cracking started")
    print(f"[*] Detected hash type: {HASH_TYPE}")
    print(f"[*] Target hash: {HASH_TO_CRACK}")
    print(f"[*] Wordlist: {wordlist}")
    print(f"[*] Saving results to: {OUTPUT_FILE}\n")

    with open(OUTPUT_FILE, "w") as out:
        out.write("Hash Cracking Results\n")
        out.write("=" * 40 + "\n")
        out.write(f"Date: {datetime.now()}\n")
        out.write(f"Hash type: {HASH_TYPE}\n")
        out.write(f"Target hash: {HASH_TO_CRACK}\n")
        out.write(f"Wordlist: {wordlist}\n\n")

        try:
            with open(wordlist, "r", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    if not word:
                        continue

                    hashed = hash_word(word, HASH_TYPE)

                    if hashed == HASH_TO_CRACK:
                        print("[+] PASSWORD FOUND!")
                        print(f"[+] Password: {word}")

                        out.write("[+] PASSWORD FOUND!\n")
                        out.write(f"Password: {word}\n")
                        return

            print("[-] Password not found in wordlist")
            out.write("[-] Password not found in wordlist\n")

        except FileNotFoundError:
            print("[!] Wordlist file not found")


if __name__ == "__main__":
    crack_hash()
