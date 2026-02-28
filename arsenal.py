#!/usr/bin/env python3
"""
Cyber Arsenal - Red Team Cybersecurity Toolkit

Central CLI entry point. Run:
  python arsenal.py <command> [options]

Examples:
  python arsenal.py hash-crack -H <hash> -w wordlist.txt
  python arsenal.py hash-identify -H <hash>
  python arsenal.py dir-enum -u https://example.com/ -w common.txt
  python arsenal.py subdomain-scan -d example.com -w subdomains.txt
  python arsenal.py port-scan -t 192.168.1.1
  python arsenal.py log-analyze -f /var/log/access.log
"""

import sys

# Ensure package is importable when run from project root
if __name__ == "__main__":
    from cyber_arsenal.cli.main import main
    sys.exit(main())
