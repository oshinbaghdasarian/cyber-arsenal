# Cyber Arsenal

**A modular Red Team cybersecurity toolkit for penetration testing and security research.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Cyber Arsenal provides a unified CLI and modular architecture for common Red Team operations: hash cracking, hash identification, directory enumeration, subdomain discovery, port scanning, and log analysis. Built for professional use, portfolio projects, and authorized security testing.

---

## Features

| Module | Tools | Description |
|--------|-------|-------------|
| **Crypto** | `hash-crack`, `hash-identify` | Multi-algorithm hash cracking (MD5, SHA1, SHA256, etc.) and identification with entropy-based detection |
| **Network** | `port-scan`, `log-analyze` | Threaded TCP port scanner with banner grabbing; log analysis with anomaly detection |
| **Web** | `dir-enum`, `subdomain-scan` | Directory enumeration and subdomain discovery with configurable threading and status filtering |

### Highlights

- **Unified CLI** — Single entry point: `python arsenal.py <command>`
- **Threading** — Port scanner, dir enum, and subdomain scanner use concurrent execution
- **Professional UX** — Banner, colored output, progress indicators, verbose/quiet modes
- **Clean Architecture** — Modular design, type hints, shared utilities, consistent error handling
- **Production Ready** — `pyproject.toml`, proper packaging, full documentation

---

## Architecture

```
cyber-arsenal/
├── arsenal.py              # CLI entry point
├── cyber_arsenal/
│   ├── core/               # Config, logging, exceptions
│   ├── crypto/             # Hash identification & cracking
│   ├── network/            # Port scanner, log analyzer
│   ├── web/                # Dir enum, subdomain scanner
│   ├── utils/              # Output, progress, helpers
│   └── cli/                # Argument parsing, command handlers
├── crypto/                 # Redirects to cyber_arsenal/crypto
├── network/
├── web/
├── wordlists/
├── ARCHITECTURE.md
├── CONTRIBUTING.md
└── CLI_USAGE.md
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

---

## Installation

### From source

```bash
git clone https://github.com/oshinbaghdasarian/cyber-arsenal.git
cd cyber-arsenal
pip install -e .
```

### Requirements

- Python 3.10+
- `requests` (for web modules)

```bash
pip install -r requirements.txt
```

### Recommended (Kali Linux)

- SecLists: `sudo apt install seclists`
- rockyou.txt: `/usr/share/wordlists/rockyou.txt`

---

## Usage

### Quick examples

```bash
# Hash identification
python arsenal.py hash-identify -H 5f4dcc3b5aa765d61d8327deb882cf99

# Hash cracking (wordlist)
python arsenal.py hash-crack -H 5f4dcc3b5aa765d61d8327deb882cf99 -w /usr/share/wordlists/rockyou.txt

# Directory enumeration
python arsenal.py dir-enum -u https://example.com/ -w /usr/share/wordlists/dirb/common.txt

# Subdomain discovery
python arsenal.py subdomain-scan -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Port scan
python arsenal.py port-scan -t 192.168.1.1 -p 1-1000

# Log analysis
python arsenal.py log-analyze -f /var/log/apache2/access.log
```

### Global options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Verbose output |
| `-q, --quiet` | Minimal output |
| `--no-banner` | Suppress startup banner |
| `--version` | Show version |

See [CLI_USAGE.md](CLI_USAGE.md) for full command reference.

---

## Module breakdown

| Module | README | Purpose |
|--------|--------|---------|
| [crypto](cyber_arsenal/crypto/README.md) | Hash identification, hash cracking | Identify unknown hashes; crack weak hashes via wordlist |
| [network](cyber_arsenal/network/README.md) | Port scanner, log analyzer | Reconnaissance, service discovery, log forensics |
| [web](cyber_arsenal/web/README.md) | Dir enum, subdomain scanner | Web application reconnaissance |

---

## Future roadmap

- [ ] DNS-based subdomain enumeration (without HTTP)
- [ ] Recursive directory enumeration
- [ ] Additional hash types (bcrypt, NTLM via passlib)
- [ ] JSON/structured output mode
- [ ] Configuration file support
- [ ] Plugin architecture for custom modules

---

## Disclaimer

**For authorized testing and educational purposes only.**

Unauthorized access to computer systems is illegal. Use these tools only on systems you own or have explicit written permission to test. The authors assume no liability for misuse.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
