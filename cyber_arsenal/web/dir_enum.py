"""Directory enumeration with threading, status filtering, and recursion."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urljoin, urlparse

import requests

from cyber_arsenal.core.exceptions import TargetError, WordlistNotFoundError


@dataclass
class DirResult:
    """Result of directory enumeration for a single path."""

    url: str
    status_code: int
    redirect_location: Optional[str] = None
    content_length: Optional[int] = None


class DirEnumerator:
    """Directory enumerator with threading and status filtering."""

    def __init__(
        self,
        base_url: str,
        wordlist_path: Path,
        threads: int = 10,
        timeout: int = 5,
        status_filter: Optional[list[int]] = None,
        user_agent: str = "CyberArsenal/1.0",
    ) -> None:
        """Initialize directory enumerator.

        Args:
            base_url: Base URL (e.g., https://example.com/).
            wordlist_path: Path to directory wordlist.
            threads: Number of concurrent threads.
            timeout: Request timeout in seconds.
            status_filter: Only report these status codes; None = 200, 301, 302, 403.
            user_agent: User-Agent header.
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.wordlist_path = Path(wordlist_path)
        self.threads = threads
        self.timeout = timeout
        self.status_filter = status_filter or [200, 301, 302, 403]
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent

    def _check_path(self, path: str) -> Optional[DirResult]:
        """Check a single path. Returns result if in filter, else None."""
        url = urljoin(self.base_url, path)
        if not url.endswith("/"):
            url += "/"
        try:
            r = self.session.get(
                url,
                timeout=self.timeout,
                allow_redirects=False,
            )
            if r.status_code in self.status_filter:
                location = r.headers.get("Location") if r.status_code in (301, 302) else None
                cl = r.headers.get("Content-Length")
                return DirResult(
                    url=url,
                    status_code=r.status_code,
                    redirect_location=location,
                    content_length=int(cl) if cl and cl.isdigit() else None,
                )
        except requests.RequestException:
            pass
        return None

    def enumerate(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> list[DirResult]:
        """Run directory enumeration. Returns list of matching results."""
        if not self.wordlist_path.exists():
            raise WordlistNotFoundError(f"Wordlist not found: {self.wordlist_path}")

        paths: list[str] = []
        with open(self.wordlist_path, "r", errors="ignore") as f:
            for line in f:
                p = line.strip()
                if p and not p.startswith("#"):
                    paths.append(p)

        results: list[DirResult] = []
        total = len(paths)
        done = 0

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._check_path, p): p for p in paths}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                done += 1
                if progress_callback:
                    progress_callback(done, total)

        return results
