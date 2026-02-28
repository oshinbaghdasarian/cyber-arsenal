"""TCP port scanner with threading and banner grabbing."""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, Optional

from cyber_arsenal.core.exceptions import TargetError


@dataclass
class PortResult:
    """Result of a port scan for a single port."""

    port: int
    open: bool
    banner: Optional[str] = None


def _grab_banner(host: str, port: int, timeout: float = 0.5) -> Optional[str]:
    """Attempt to grab service banner via HTTP HEAD."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore")
        sock.close()
        first_line = banner.strip().splitlines()[0] if banner else None
        return first_line[:80] if first_line else None
    except (socket.error, OSError, UnicodeDecodeError):
        return None


def _scan_port(host: str, port: int, timeout: float, grab_banners: bool) -> PortResult:
    """Scan a single port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            banner = _grab_banner(host, port, timeout) if grab_banners else None
            return PortResult(port=port, open=True, banner=banner)
        return PortResult(port=port, open=False)
    except (socket.error, OSError):
        return PortResult(port=port, open=False)


class PortScanner:
    """Threaded TCP port scanner."""

    def __init__(
        self,
        target: str,
        ports: Optional[list[int]] = None,
        timeout: float = 0.3,
        threads: int = 50,
        grab_banners: bool = True,
    ) -> None:
        """Initialize port scanner.

        Args:
            target: Target hostname or IP.
            ports: Port list; defaults to top 1000 common ports.
            timeout: Socket timeout in seconds.
            threads: Number of concurrent threads.
            grab_banners: Attempt HTTP banner grab on open ports.
        """
        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.grab_banners = grab_banners
        self.ports = ports or self._common_ports()

    def _common_ports(self) -> list[int]:
        """Return top 100 common ports."""
        return [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
            1723, 3306, 3389, 5900, 8080, 8443,
            *range(1, 1025),  # 1-1024
        ][:1000]  # Limit to 1000

    def scan(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> list[PortResult]:
        """Run port scan. Returns list of open port results."""
        results: list[PortResult] = []
        total = len(self.ports)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {
                executor.submit(
                    _scan_port,
                    self.target,
                    port,
                    self.timeout,
                    self.grab_banners,
                ): port
                for port in self.ports
            }
            done = 0
            for future in as_completed(futures):
                result = future.result()
                if result.open:
                    results.append(result)
                done += 1
                if progress_callback:
                    progress_callback(done, total)

        return sorted(results, key=lambda r: r.port)
