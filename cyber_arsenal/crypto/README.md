# Crypto Module

Hash identification and hash cracking for Red Team operations.

---

## What it does

- **Hash identification**: Detects hash type from prefix (bcrypt, MD5 crypt, etc.), hex length (MD5, SHA1, SHA256, etc.), and entropy heuristics.
- **Hash cracking**: Cracks hashes using wordlist or brute-force (short passwords only) for MD5, SHA1, SHA224, SHA256, SHA384, SHA512.

---

## How it works

### Hash identification

1. **Prefix matching**: Checks for known prefixes (`$2a$`, `$1$`, `{SHA}`, etc.).
2. **Hex length**: Pure hex strings are mapped by length (32→MD5, 40→SHA1, 64→SHA256, etc.).
3. **Entropy**: High Shannon entropy suggests a hash; used as fallback.

### Hash cracking

1. **Auto-detection**: Uses `identify_hash()` to determine algorithm.
2. **Wordlist mode**: Reads wordlist line-by-line, hashes each word, compares to target.
3. **Brute-force mode**: Iterates over character combinations (use only for very short passwords).

---

## Example usage

### CLI

```bash
python arsenal.py hash-identify -H 5f4dcc3b5aa765d61d8327deb882cf99
python arsenal.py hash-crack -H 5f4dcc3b5aa765d61d8327deb882cf99 -w rockyou.txt
```

### Python API

```python
from cyber_arsenal.crypto.hashiden import identify_hash, HashIdentifier
from cyber_arsenal.crypto.hashcracker import HashCracker

# Identify
print(identify_hash("5f4dcc3b5aa765d61d8327deb882cf99"))  # MD5

# Crack
cracker = HashCracker("5f4dcc3b5aa765d61d8327deb882cf99")
password = cracker.crack_wordlist(Path("wordlist.txt"))
```

---

## Security relevance

- **Post-exploitation**: Cracking dumped password hashes.
- **CTF / training**: Hash identification and cracking challenges.
- **Auditing**: Testing password policy strength.

**Warning**: Use only on hashes you own or have authorization to crack.
