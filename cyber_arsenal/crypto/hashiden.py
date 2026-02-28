"""Hash type identification with prefix, length, and entropy-based detection."""

import math
import re
from typing import Optional

# Hash type patterns: (regex, name)
HASH_PATTERNS = [
    (r"^\$2a\$", "bcrypt"),
    (r"^\$2y\$", "bcrypt"),
    (r"^\$2b\$", "bcrypt"),
    (r"^\$1\$", "MD5 Crypt"),
    (r"^\$6\$", "SHA-512 Crypt"),
    (r"^\$5\$", "SHA-256 Crypt"),
    (r"^\{SHA\}", "SHA1 (Base64)"),
    (r"^\{SSHA\}", "Salted SHA1"),
    (r"^NTLM:", "NTLM"),
    (r"^\{md5\}", "MD5 (LDAP)"),
    (r"^\{SHA256\}", "SHA256 (LDAP)"),
    (r"^\$apr1\$", "Apache MD5"),
]

# Hex length mapping (characters)
HEX_LENGTH_MAP = {
    32: "MD5",
    40: "SHA1",
    56: "SHA224",
    64: "SHA256",
    96: "SHA384",
    128: "SHA512",
}

# Base64-like hash lengths (approximate)
BASE64_PATTERNS = [
    (r"^[A-Za-z0-9+/]{27}={0,2}$", "MD5 (Base64)"),
    (r"^[A-Za-z0-9+/]{28}={0,2}$", "SHA1 (Base64)"),
]


def _entropy(data: str) -> float:
    """Calculate Shannon entropy of a string (for hash detection)."""
    if not data:
        return 0.0
    freq: dict[str, int] = {}
    for c in data:
        freq[c] = freq.get(c, 0) + 1
    length = len(data)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())


def identify_hash(hash_value: str) -> Optional[str]:
    """Identify hash type from a hash string.

    Uses prefix matching, hex length, and entropy heuristics.
    Returns None if unknown.

    Args:
        hash_value: The hash string to identify.

    Returns:
        Hash type name or None if unknown.
    """
    h = hash_value.strip()

    # Prefix-based detection
    for pattern, name in HASH_PATTERNS:
        if re.match(pattern, h):
            return name

    # Hex length-based detection
    if re.fullmatch(r"[a-fA-F0-9]+", h):
        length = len(h)
        if length in HEX_LENGTH_MAP:
            return HEX_LENGTH_MAP[length]
        # Fallback for non-standard lengths
        if 28 <= length <= 36:
            return "MD5 (possible)"
        if 38 <= length <= 42:
            return "SHA1 (possible)"
        if 62 <= length <= 66:
            return "SHA256 (possible)"

    # Base64-like patterns
    for pattern, name in BASE64_PATTERNS:
        if re.match(pattern, h):
            return name

    # Entropy-based heuristic: high entropy suggests hash
    ent = _entropy(h)
    if len(h) >= 16 and ent > 3.5:
        return "Unknown (high entropy - likely hash)"

    return None


class HashIdentifier:
    """Hash identification service with detailed analysis."""

    def __init__(self, hash_value: str) -> None:
        """Initialize with hash to identify."""
        self.hash_value = hash_value.strip()
        self.identified_type: Optional[str] = None
        self.entropy: float = 0.0
        self.length: int = 0

    def analyze(self) -> str:
        """Perform full analysis and return identified type."""
        self.length = len(self.hash_value)
        self.entropy = _entropy(self.hash_value)
        self.identified_type = identify_hash(self.hash_value)
        return self.identified_type or "Unknown"

    def get_details(self) -> dict:
        """Return analysis details as dict."""
        self.analyze()
        return {
            "type": self.identified_type,
            "length": self.length,
            "entropy": round(self.entropy, 2),
        }
