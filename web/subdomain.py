import requests
import os
from datetime import datetime

# Target domain
domain = input("Enter target domain (example: example.com): ").strip()

# Kali default subdomain wordlist
DEFAULT_WORDLIST = "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"

use_default = input("Use Kali default wordlist? (y/n): ").lower()

if use_default == "y":
    wordlist = DEFAULT_WORDLIST
else:
    wordlist = input("Enter full path to your wordlist: ").strip()

if not os.path.isfile(wordlist):
    print("[-] Wordlist file not found!")
    exit()

# Output file
output_file = "subdomains_results.txt"

print(f"\n[+] Subdomain discovery on {domain}")
print(f"[+] Wordlist: {wordlist}")
print(f"[+] Saving results to: {output_file}\n")

with open(output_file, "w") as out:
    out.write("Subdomain Discovery Results\n")
    out.write("=" * 40 + "\n")
    out.write(f"Target domain: {domain}\n")
    out.write(f"Wordlist: {wordlist}\n")
    out.write(f"Date: {datetime.now()}\n\n")

    with open(wordlist, "r", errors="ignore") as file:
        for line in file:
            sub = line.strip()
            if not sub:
                continue

            url = f"http://{sub}.{domain}"

            try:
                r = requests.get(url, timeout=3, allow_redirects=False)
                status = r.status_code

                # 404 չենք տպում
                if status != 404:
                    print(f"[{status}] {sub}.{domain}")
                    out.write(f"[{status}] {sub}.{domain}\n")

            except requests.RequestException:
                pass

print("\n[✓] Scan completed. Results saved to subdomains_results.txt")
