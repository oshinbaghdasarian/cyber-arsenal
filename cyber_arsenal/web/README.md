# Web Module

Directory enumeration and subdomain discovery for web reconnaissance.

---

## What it does

- **Directory enumeration**: Checks paths from a wordlist against a target URL; reports configurable status codes (200, 301, 302, 403, etc.).
- **Subdomain scanner**: Resolves subdomains via HTTP; excludes 404 by default; supports HTTP/HTTPS.

---

## How it works

### Directory enumeration

1. Reads directory paths from wordlist.
2. Uses `ThreadPoolExecutor` for concurrent HTTP requests.
3. For each path: `GET` request, checks status code against filter.
4. Reports URL, status, redirect location, content length.

### Subdomain scanner

1. Reads subdomain prefixes from wordlist.
2. Builds `subdomain.domain` and performs HTTP request.
3. Excludes 404 responses by default (configurable).
4. Returns discovered subdomains with status codes.

---

## Example usage

### CLI

```bash
python arsenal.py dir-enum -u https://example.com/ -w /usr/share/wordlists/dirb/common.txt
python arsenal.py subdomain-scan -d example.com -w subdomains.txt --https
```

### Python API

```python
from cyber_arsenal.web.dir_enum import DirEnumerator
from cyber_arsenal.web.subdomain_scanner import SubdomainScanner

# Dir enum
enum = DirEnumerator("https://example.com/", Path("common.txt"), threads=20)
results = enum.enumerate()

# Subdomain scan
scanner = SubdomainScanner("example.com", Path("subdomains.txt"), protocol="https")
results = scanner.scan()
```

---

## Security relevance

- **Reconnaissance**: Discover hidden directories and subdomains.
- **Attack surface mapping**: Identify potential entry points.
- **Bug bounty**: Common first steps in web assessment.

**Warning**: Use only on targets you are authorized to test.
