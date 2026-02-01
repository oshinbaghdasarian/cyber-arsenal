import re

def identify_hash(h):
    h = h.strip()

    # --- Symbol / prefix based ---
    if h.startswith("$2a$") or h.startswith("$2y$") or h.startswith("$2b$"):
        return "bcrypt"

    if h.startswith("$1$"):
        return "MD5 Crypt"

    if h.startswith("$6$"):
        return "SHA-512 Crypt"

    if h.startswith("$5$"):
        return "SHA-256 Crypt"

    if h.startswith("{SHA}"):
        return "SHA1 (Base64)"

    if h.startswith("{SSHA}"):
        return "Salted SHA1"

    if h.startswith("NTLM:"):
        return "NTLM"

    # --- Hex length based ---
    if re.fullmatch(r"[a-fA-F0-9]{32}", h):
        return "MD5"

    if re.fullmatch(r"[a-fA-F0-9]{40}", h):
        return "SHA1"

    if re.fullmatch(r"[a-fA-F0-9]{64}", h):
        return "SHA256"

    if re.fullmatch(r"[a-fA-F0-9]{96}", h):
        return "SHA384"

    if re.fullmatch(r"[a-fA-F0-9]{128}", h):
        return "SHA512"

    return "Unknown hash type"


hash_input = input("Enter hash: ")
print(f"[+] Possible hash type: {identify_hash(hash_input)}")
