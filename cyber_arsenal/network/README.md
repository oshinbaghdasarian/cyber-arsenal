# Network Module

Port scanning and log analysis for reconnaissance and forensics.

---

## What it does

- **Port scanner**: Threaded TCP connect scan with optional HTTP banner grabbing.
- **Log analyzer**: Extracts IPs, error keywords, HTTP status codes; performs anomaly detection (z-score on request counts).

---

## How it works

### Port scanner

1. Uses `ThreadPoolExecutor` for concurrent port checks.
2. For each port: `socket.connect_ex()` to detect open state.
3. On open ports: optional HTTP HEAD request to grab service banner.
4. Default port set: top 1000 common ports (customizable).

### Log analyzer

1. **IP extraction**: Regex for IPv4 addresses.
2. **Error keywords**: Counts occurrences of `error`, `failed`, `denied`, etc.
3. **HTTP status**: Detects 4xx/5xx codes in log lines.
4. **Anomaly detection**: Z-score on IP request counts; flags IPs with unusually high activity.

---

## Example usage

### CLI

```bash
python arsenal.py port-scan -t 192.168.1.1 -p 1-1000
python arsenal.py log-analyze -f /var/log/apache2/access.log -n 20
```

### Python API

```python
from cyber_arsenal.network.port_scanner import PortScanner
from cyber_arsenal.network.log_analyzer import LogAnalyzer

# Port scan
scanner = PortScanner("192.168.1.1", ports=[80, 443, 8080])
results = scanner.scan()

# Log analysis
analyzer = LogAnalyzer(Path("/var/log/access.log"), top_n=10)
report = analyzer.analyze()
```

---

## Security relevance

- **Reconnaissance**: Identify open ports and services.
- **Incident response**: Analyze logs for suspicious IPs and errors.
- **Compliance**: Audit access patterns and anomalies.

**Warning**: Port scanning should only be performed on authorized targets.
