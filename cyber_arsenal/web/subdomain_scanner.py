"""Subdomain discovery with threading and HTTP/DNS checks."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import requests

from cyber_arsenal.core.exceptions import TargetError, WordlistNotFoundError


@dataclass
class SubdomainResult:
    """Result of subdomain check."""

    subdomain: str
    full_domain: str
    status_code: Optional[int]
    resolved: bool


class SubdomainScanner:
    """Subdomain discovery via HTTP checks with threading."""

    def __init__(
        self,
        domain: str,
        wordlist_path: Path,
        threads: int = 20,
        timeout: int = 3,
        protocol: str = "http",
        exclude_404: bool = True,
        user_agent: str = "CyberArsenal/1.0",
    ) -> None:
        """Initialize subdomain scanner.

        Args:
            domain: Base domain (e.g., example.com).
            wordlist_path: Path to subdomain wordlist.
            threads: Number of concurrent threads.
            timeout: Request timeout in seconds.
            protocol: http or https.
            exclude_404: Don't report 404 responses.
            user_agent: User-Agent header.
        """
        self.domain = domain.strip().lower()
        self.wordlist_path = Path(wordlist_path)
        self.threads = threads
        self.timeout = timeout
        self.protocol = protocol
        self.exclude_404 = exclude_404
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent

    def _check_subdomain(self, sub: str) -> Optional[SubdomainResult]:
        """Check if subdomain exists via HTTP."""
        full = f"{sub}.{self.domain}"
        url = f"{self.protocol}://{full}"
        try:
            r = self.session.get(url, timeout=self.timeout, allow_redirects=False)
            if self.exclude_404 and r.status_code == 404:
                return None
            return SubdomainResult(
                subdomain=sub,
                full_domain=full,
                status_code=r.status_code,
                resolved=True,
            )
        except requests.RequestException:
            return None

    def scan(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> list[SubdomainResult]:
        """Run subdomain scan. Returns list of discovered subdomains."""
        if not self.wordlist_path.exists():
            raise WordlistNotFoundError(f"Wordlist not found: {self.wordlist_path}")

        subdomains: list[str] = []
        with open(self.wordlist_path, "r", errors="ignore") as f:
            for line in f:
                s = line.strip().lower()
                if s and not s.startswith("#"):
                    subdomains.append(s)

        results: list[SubdomainResult] = []
        total = len(subdomains)
        done = 0

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._check_subdomain, s): s for s in subdomains}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                done += 1
                if progress_callback:
                    progress_callback(done, total)

        return sorted(results, key=lambda r: r.full_domain)
