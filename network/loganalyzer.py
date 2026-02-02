import re
from collections import Counter
from datetime import datetime

log_file = input("Enter log file path: ").strip()
output_file = "generic_log_report.txt"

# Regex patterns
ip_pattern = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
error_keywords = ["error", "failed", "denied", "unauthorized", "invalid", "warning"]

total_lines = 0
ip_counter = Counter()
error_counter = Counter()

try:
    with open(log_file, "r", errors="ignore") as file:
        for line in file:
            total_lines += 1
            line_lower = line.lower()

            # Find IPs
            ips = ip_pattern.findall(line)
            for ip in ips:
                ip_counter[ip] += 1

            # Find error keywords
            for keyword in error_keywords:
                if keyword in line_lower:
                    error_counter[keyword] += 1

except FileNotFoundError:
    print("[-] Log file not found!")
    exit()

# Write report
with open(output_file, "w") as out:
    out.write("Generic Log Analysis Report\n")
    out.write("=" * 40 + "\n")
    out.write(f"Date: {datetime.now()}\n\n")

    out.write(f"Total log lines: {total_lines}\n\n")

    out.write("Top 5 IP addresses:\n")
    if ip_counter:
        for ip, count in ip_counter.most_common(5):
            out.write(f"{ip} -> {count} occurrences\n")
    else:
        out.write("No IP addresses found\n")

    out.write("\nSuspicious / Error Keywords:\n")
    if error_counter:
        for key, count in error_counter.items():
            out.write(f"{key.upper()} -> {count}\n")
    else:
        out.write("No error keywords detected\n")

print(f"[✓] Log analysis completed. Results saved to {output_file}")
