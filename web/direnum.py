import requests
import os
from datetime import datetime

target_url = input("Enter target URL (example: https://example.com/): ").strip()

kali_wordlist = "/usr/share/wordlists/dirb/common.txt"
use_default = input("Use Kali default wordlist? (y/n): ").lower()

if use_default == "y":
    wordlist = kali_wordlist
else:
    wordlist = input("Enter full path to your wordlist: ").strip()

if not os.path.isfile(wordlist):
    print("[-] Wordlist file not found!")
    exit()

output_file = "results.txt"

print(f"\n[+] Starting directory enumeration on {target_url}")
print(f"[+] Using wordlist: {wordlist}")
print(f"[+] Saving results to: {output_file}\n")

with open(output_file, "w") as out:
    out.write("Directory Enumeration Results\n")
    out.write("=" * 40 + "\n")
    out.write(f"Target: {target_url}\n")
    out.write(f"Wordlist: {wordlist}\n")
    out.write(f"Date: {datetime.now()}\n\n")

    with open(wordlist, "r", errors="ignore") as file:
        for line in file:
            directory = line.strip()
            if not directory:
                continue

            url = f"{target_url.rstrip('/')}/{directory}/"

            try:
                response = requests.get(url, timeout=5, allow_redirects=False)
                status = response.status_code

                if status == 200:
                    print(f"[200 OK] {url}")
                    out.write(f"[200 OK] {url}\n")

                elif status == 302:
                    location = response.headers.get("Location", "Unknown")
                    print(f"[302 REDIRECT] {url} -> {location}")
                    out.write(f"[302 REDIRECT] {url} -> {location}\n")

                elif status == 403:
                    print(f"[403 FORBIDDEN] {url}")
                    out.write(f"[403 FORBIDDEN] {url}\n")

            except requests.RequestException:
                pass

print("\n[✓] Scan completed. Results saved to results.txt")
