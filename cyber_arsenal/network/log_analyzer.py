"""Log file analyzer with IP extraction, error detection, and anomaly detection."""

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from cyber_arsenal.core.exceptions import TargetError


IP_PATTERN = re.compile(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
                        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")

ERROR_KEYWORDS = [
    "error", "failed", "denied", "unauthorized", "invalid", "warning",
    "critical", "exception", "fatal", "timeout", "refused",
]

STATUS_PATTERN = re.compile(r"\b(?:4\d{2}|5\d{2})\b")  # 4xx, 5xx HTTP


@dataclass
class LogReport:
    """Log analysis report."""

    total_lines: int = 0
    top_ips: list[tuple[str, int]] = field(default_factory=list)
    error_keywords: dict[str, int] = field(default_factory=dict)
    status_codes: dict[str, int] = field(default_factory=dict)
    anomalies: list[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.now)


class LogAnalyzer:
    """Analyze log files for security-relevant patterns."""

    def __init__(
        self,
        log_path: Path,
        top_n: int = 10,
        anomaly_threshold: float = 3.0,
    ) -> None:
        """Initialize log analyzer.

        Args:
            log_path: Path to log file.
            top_n: Number of top IPs to report.
            anomaly_threshold: Z-score threshold for anomaly detection.
        """
        self.log_path = Path(log_path)
        self.top_n = top_n
        self.anomaly_threshold = anomaly_threshold

    def analyze(self) -> LogReport:
        """Perform full log analysis."""
        if not self.log_path.exists():
            raise TargetError(f"Log file not found: {self.log_path}")

        ip_counter: Counter[str] = Counter()
        error_counter: Counter[str] = Counter()
        status_counter: Counter[str] = Counter()
        total_lines = 0

        with open(self.log_path, "r", errors="ignore") as f:
            for line in f:
                total_lines += 1
                line_lower = line.lower()

                for ip in IP_PATTERN.findall(line):
                    ip_counter[ip] += 1

                for keyword in ERROR_KEYWORDS:
                    if keyword in line_lower:
                        error_counter[keyword] += 1

                for match in STATUS_PATTERN.finditer(line):
                    status_counter[match.group()] += 1

        report = LogReport(total_lines=total_lines)
        report.top_ips = ip_counter.most_common(self.top_n)
        report.error_keywords = dict(error_counter)
        report.status_codes = dict(status_counter)

        # Anomaly detection: IPs with unusually high request counts
        if ip_counter:
            counts = list(ip_counter.values())
            mean = sum(counts) / len(counts)
            variance = sum((c - mean) ** 2 for c in counts) / len(counts)
            std = variance ** 0.5 if variance > 0 else 0
            if std > 0:
                for ip, count in ip_counter.most_common(20):
                    z = (count - mean) / std
                    if z > self.anomaly_threshold:
                        report.anomalies.append(
                            f"Anomaly: {ip} has {count} requests (z-score: {z:.1f})"
                        )

        return report
