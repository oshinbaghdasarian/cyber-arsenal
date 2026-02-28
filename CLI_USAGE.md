# Cyber Arsenal — CLI Usage

Complete reference for the `arsenal.py` command-line interface.

---

## Entry point

```bash
python arsenal.py <command> [options]
```

Or, after `pip install -e .`:

```bash
arsenal <command> [options]
```

---

## Global options

Available for all commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Enable verbose/debug output |
| `--quiet` | `-q` | Minimal output (errors only) |
| `--no-banner` | | Suppress startup banner |
| `--version` | | Show version and exit |

---

## Commands

### hash-crack

Crack a hash using a wordlist.

```bash
python arsenal.py hash-crack -H <hash> -w <wordlist> [-o output.txt]
```

| Option | Required | Description |
|--------|----------|-------------|
| `-H, --hash` | Yes | Hash to crack |
| `-w, --wordlist` | Yes | Path to wordlist file |
| `-o, --output` | No | Output file (default: `crack_results.txt`) |
| `--no-progress` | No | Disable progress messages |

**Supported hash types**: MD5, SHA1, SHA224, SHA256, SHA384, SHA512 (auto-detected)

**Example**:
```bash
python arsenal.py hash-crack -H 5f4dcc3b5aa765d61d8327deb882cf99 -w /usr/share/wordlists/rockyou.txt
```

---

### hash-identify

Identify the type of a hash.

```bash
python arsenal.py hash-identify -H <hash>
```

| Option | Required | Description |
|--------|----------|-------------|
| `-H, --hash` | Yes | Hash to identify |

**Example**:
```bash
python arsenal.py hash-identify -H $2a$10$N9qo8uLOickgx2ZMRZoMye
```

---

### dir-enum

Enumerate directories on a web server.

```bash
python arsenal.py dir-enum -u <url> -w <wordlist> [-o output.txt] [-t threads] [-s status_codes]
```

| Option | Required | Description |
|--------|----------|-------------|
| `-u, --url` | Yes | Target URL (e.g., `https://example.com/`) |
| `-w, --wordlist` | Yes | Path to directory wordlist |
| `-o, --output` | No | Output file (default: `dir_enum_results.txt`) |
| `-t, --threads` | No | Concurrent threads (default: 10) |
| `-s, --status` | No | Status codes to report (default: 200 301 302 403) |

**Example**:
```bash
python arsenal.py dir-enum -u https://example.com/ -w /usr/share/wordlists/dirb/common.txt -t 20
```

---

### subdomain-scan

Discover subdomains via HTTP checks.

```bash
python arsenal.py subdomain-scan -d <domain> -w <wordlist> [-o output.txt] [-t threads] [--https]
```

| Option | Required | Description |
|--------|----------|-------------|
| `-d, --domain` | Yes | Target domain (e.g., `example.com`) |
| `-w, --wordlist` | Yes | Path to subdomain wordlist |
| `-o, --output` | No | Output file (default: `subdomain_results.txt`) |
| `-t, --threads` | No | Concurrent threads (default: 20) |
| `--https` | No | Use HTTPS instead of HTTP |

**Example**:
```bash
python arsenal.py subdomain-scan -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --https
```

---

### port-scan

TCP port scanner with optional banner grabbing.

```bash
python arsenal.py port-scan -t <target> [-p ports] [-o output.txt] [--threads N] [--no-banner]
```

| Option | Required | Description |
|--------|----------|-------------|
| `-t, --target` | Yes | Target IP or hostname |
| `-p, --ports` | No | Port range or list (default: 1-1000) |
| `-o, --output` | No | Output file (default: `port_scan_results.txt`) |
| `--threads` | No | Concurrent threads (default: 50) |
| `--no-grab` | No | Disable HTTP service banner grabbing |

**Port format**:
- Range: `1-1000`, `80-443`
- List: `80,443,8080,8443`
- Combined: `80,443,8000-9000`

**Example**:
```bash
python arsenal.py port-scan -t 192.168.1.1 -p 1-1000 --threads 100
```

---

### log-analyze

Analyze log files for IPs, errors, and anomalies.

```bash
python arsenal.py log-analyze -f <logfile> [-o output.txt] [-n top_n]
```

| Option | Required | Description |
|--------|----------|-------------|
| `-f, --file` | Yes | Path to log file |
| `-o, --output` | No | Output file (default: `log_analysis_report.txt`) |
| `-n, --top-n` | No | Number of top IPs to report (default: 10) |

**Example**:
```bash
python arsenal.py log-analyze -f /var/log/apache2/access.log -n 20
```

---

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, file not found, etc.) |
| 130 | Interrupted by user (Ctrl+C) |

---

## Tips

- Use `-v` when debugging or understanding tool behavior.
- Use `-q` in scripts or when piping output.
- For large wordlists, `hash-crack` may take a long time; use `-v` to see progress.
- Increase `-t` (threads) for faster dir-enum and subdomain-scan on capable targets.
