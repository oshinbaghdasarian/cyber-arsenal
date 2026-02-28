"""Configuration management for Cyber Arsenal."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Global configuration for the toolkit."""

    verbose: bool = False
    quiet: bool = False
    output_dir: Path = field(default_factory=lambda: Path("."))
    timeout: int = 5
    threads: int = 10

    # Default wordlist paths (Kali Linux)
    wordlist_rockyou: Path = Path("/usr/share/wordlists/rockyou.txt")
    wordlist_dirb: Path = Path("/usr/share/wordlists/dirb/common.txt")
    wordlist_subdomains: Path = Path(
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
    )

    def ensure_output_dir(self) -> Path:
        """Ensure output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir
