"""Hash cracking with wordlist and brute-force modes."""

import hashlib
from pathlib import Path
from typing import Callable, Iterator, Optional

from cyber_arsenal.core.exceptions import InvalidHashError, WordlistNotFoundError
from cyber_arsenal.crypto.hashiden import identify_hash


# Supported hash types for cracking (standard library only for portability)
CRACKABLE_TYPES = {"md5", "sha1", "sha256", "sha224", "sha384", "sha512"}


def _hash_func(hash_type: str) -> Callable[[bytes], str]:
    """Get hashlib function for hash type."""
    mapping = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha224": hashlib.sha224,
        "sha256": hashlib.sha256,
        "sha384": hashlib.sha384,
        "sha512": hashlib.sha512,
    }
    if hash_type.lower() not in mapping:
        raise InvalidHashError(f"Unsupported hash type for cracking: {hash_type}")
    return lambda b: mapping[hash_type.lower()](b).hexdigest()


def _normalize_hash_type(identified: Optional[str]) -> Optional[str]:
    """Normalize identified hash type to crackable format."""
    if not identified:
        return None
    lower = identified.lower()
    if "md5" in lower and "crypt" not in lower and "base64" not in lower:
        return "md5"
    if "sha1" in lower and "base64" not in lower and "salted" not in lower:
        return "sha1"
    if "sha256" in lower and "crypt" not in lower:
        return "sha256"
    if "sha224" in lower:
        return "sha224"
    if "sha384" in lower:
        return "sha384"
    if "sha512" in lower and "crypt" not in lower:
        return "sha512"
    return None


class HashCracker:
    """Hash cracker supporting wordlist and brute-force modes."""

    def __init__(
        self,
        target_hash: str,
        hash_type: Optional[str] = None,
    ) -> None:
        """Initialize cracker with target hash.

        Args:
            target_hash: The hash to crack.
            hash_type: Optional explicit type; auto-detected if None.
        """
        self.target_hash = target_hash.strip().lower()
        self.hash_type = hash_type or _normalize_hash_type(identify_hash(self.target_hash))
        if not self.hash_type or self.hash_type not in CRACKABLE_TYPES:
            raise InvalidHashError(
                f"Cannot crack: unsupported or unknown hash type. "
                f"Supported: {', '.join(CRACKABLE_TYPES)}"
            )
        self._hash_func = _hash_func(self.hash_type)

    def _hash_word(self, word: str) -> str:
        """Hash a word using the configured algorithm."""
        return self._hash_func(word.encode("utf-8", errors="replace"))

    def crack_wordlist(
        self,
        wordlist_path: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Optional[str]:
        """Crack using wordlist. Returns password if found, else None.

        Args:
            wordlist_path: Path to wordlist file.
            progress_callback: Optional callback(count, word) for progress.

        Returns:
            Cracked password or None.
        """
        if not wordlist_path.exists():
            raise WordlistNotFoundError(f"Wordlist not found: {wordlist_path}")

        count = 0
        with open(wordlist_path, "r", errors="ignore") as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                count += 1
                if progress_callback:
                    progress_callback(count, word)
                if self._hash_word(word) == self.target_hash:
                    return word
        return None

    def crack_bruteforce(
        self,
        charset: str = "abcdefghijklmnopqrstuvwxyz0123456789",
        min_len: int = 1,
        max_len: int = 4,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Optional[str]:
        """Simple brute-force crack (short passwords only).

        WARNING: Only use for very short passwords (max_len <= 4 recommended).

        Args:
            charset: Character set to use.
            min_len: Minimum password length.
            max_len: Maximum password length.
            progress_callback: Optional callback for progress.

        Returns:
            Cracked password or None.
        """
        from itertools import product

        count = 0
        for length in range(min_len, max_len + 1):
            for combo in product(charset, repeat=length):
                word = "".join(combo)
                count += 1
                if progress_callback:
                    progress_callback(count, word)
                if self._hash_func(word.encode("utf-8")) == self.target_hash:
                    return word
        return None
