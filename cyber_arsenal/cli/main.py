"""Central CLI entry point for Cyber Arsenal."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from cyber_arsenal import __version__
from cyber_arsenal.core.config import Config
from cyber_arsenal.core.exceptions import (
    CyberArsenalError,
    InvalidHashError,
    TargetError,
    WordlistNotFoundError,
)
from cyber_arsenal.utils.output import Output


def _create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="arsenal",
        description="Cyber Arsenal - Red Team Cybersecurity Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python arsenal.py hash-crack -H abc123... -w wordlist.txt
  python arsenal.py hash-identify -H abc123...
  python arsenal.py dir-enum -u https://example.com/ -w common.txt
  python arsenal.py subdomain-scan -d example.com -w subdomains.txt
  python arsenal.py port-scan -t 192.168.1.1
  python arsenal.py log-analyze -f /var/log/apache2/access.log
        """,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode (minimal output)")
    parser.add_argument("--no-banner", action="store_true", help="Suppress banner")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to run")

    # hash-crack
    crack = subparsers.add_parser("hash-crack", help="Crack hash using wordlist")
    crack.add_argument("-H", "--hash", required=True, help="Hash to crack")
    crack.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    crack.add_argument("-o", "--output", default="crack_results.txt", help="Output file")
    crack.add_argument("--no-progress", action="store_true", help="Disable progress bar")

    # hash-identify
    identify = subparsers.add_parser("hash-identify", help="Identify hash type")
    identify.add_argument("-H", "--hash", required=True, help="Hash to identify")

    # dir-enum
    direnum = subparsers.add_parser("dir-enum", help="Directory enumeration")
    direnum.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com/)")
    direnum.add_argument("-w", "--wordlist", required=True, help="Path to directory wordlist")
    direnum.add_argument("-o", "--output", default="dir_enum_results.txt", help="Output file")
    direnum.add_argument("-t", "--threads", type=int, default=10, help="Threads (default: 10)")
    direnum.add_argument("-s", "--status", type=int, nargs="+", default=[200, 301, 302, 403],
                        help="Status codes to report (default: 200 301 302 403)")

    # subdomain-scan
    subdom = subparsers.add_parser("subdomain-scan", help="Subdomain discovery")
    subdom.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    subdom.add_argument("-w", "--wordlist", required=True, help="Path to subdomain wordlist")
    subdom.add_argument("-o", "--output", default="subdomain_results.txt", help="Output file")
    subdom.add_argument("-t", "--threads", type=int, default=20, help="Threads (default: 20)")
    subdom.add_argument("--https", action="store_true", help="Use HTTPS instead of HTTP")

    # port-scan
    portscan = subparsers.add_parser("port-scan", help="TCP port scanner")
    portscan.add_argument("-t", "--target", required=True, help="Target IP or hostname")
    portscan.add_argument("-p", "--ports", type=str, default="1-1000",
                         help="Port range (e.g., 1-1000 or 80,443,8080)")
    portscan.add_argument("-o", "--output", default="port_scan_results.txt", help="Output file")
    portscan.add_argument("--threads", type=int, default=50, help="Threads (default: 50)")
    portscan.add_argument("--no-grab", dest="grab_banners", action="store_false",
                         help="Disable service banner grabbing")

    # log-analyze
    log = subparsers.add_parser("log-analyze", help="Log file analysis")
    log.add_argument("-f", "--file", required=True, help="Path to log file")
    log.add_argument("-o", "--output", default="log_analysis_report.txt", help="Output file")
    log.add_argument("-n", "--top-n", type=int, default=10, help="Top N IPs to report (default: 10)")

    return parser


def _parse_ports(spec: str) -> list[int]:
    """Parse port specification like '1-1000' or '80,443,8080'."""
    ports: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                start, end = int(a.strip()), int(b.strip())
                ports.extend(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                ports.append(int(part))
            except ValueError:
                continue
    return sorted(set(ports)) if ports else list(range(1, 1001))


def _cmd_hash_crack(args: argparse.Namespace, out: Output) -> int:
    """Execute hash-crack command."""
    from cyber_arsenal.crypto.hashcracker import HashCracker

    try:
        cracker = HashCracker(args.hash)
    except InvalidHashError as e:
        out.error(str(e))
        return 1

    wordlist = Path(args.wordlist)
    if not wordlist.exists():
        out.error(f"Wordlist not found: {wordlist}")
        return 1

    out.info(f"Hash type: {cracker.hash_type}")
    out.info(f"Target: {args.hash[:16]}...")
    out.info(f"Wordlist: {wordlist}")

    def on_progress(count: int, word: str) -> None:
        if args.verbose and count % 10000 == 0 and count > 0:
            out.verbose_msg(f"Checked {count} words...")

    result = cracker.crack_wordlist(wordlist, progress_callback=on_progress)

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write("Hash Cracking Results\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Hash type: {cracker.hash_type}\n")
        f.write(f"Target: {args.hash}\n")
        f.write(f"Wordlist: {wordlist}\n\n")
        if result:
            f.write(f"[+] PASSWORD FOUND: {result}\n")
        else:
            f.write("[-] Password not found in wordlist\n")

    if result:
        out.success(f"PASSWORD FOUND: {result}")
        out.info(f"Results saved to {output_path}")
        return 0
    else:
        out.warning("Password not found in wordlist")
        out.info(f"Results saved to {output_path}")
        return 1


def _cmd_hash_identify(args: argparse.Namespace, out: Output) -> int:
    """Execute hash-identify command."""
    from cyber_arsenal.crypto.hashiden import HashIdentifier

    identifier = HashIdentifier(args.hash)
    details = identifier.get_details()
    result = details["type"] or "Unknown"
    out.success(f"Identified: {result}")
    out.verbose_msg(f"Length: {details['length']}, Entropy: {details['entropy']}")
    return 0


def _cmd_dir_enum(args: argparse.Namespace, out: Output) -> int:
    """Execute dir-enum command."""
    from cyber_arsenal.web.dir_enum import DirEnumerator
    from cyber_arsenal.utils.progress import ProgressBar

    wordlist = Path(args.wordlist)
    if not wordlist.exists():
        out.error(f"Wordlist not found: {wordlist}")
        return 1

    enumerator = DirEnumerator(
        args.url,
        wordlist,
        threads=args.threads,
        status_filter=args.status,
    )

    out.info(f"Target: {args.url}")
    out.info(f"Wordlist: {wordlist}")
    out.info(f"Threads: {args.threads}")

    progress = ProgressBar(total=0, prefix="Enumerating") if not args.quiet else None

    def on_progress(done: int, total: int) -> None:
        if progress and progress.total != total:
            progress.total = total
        if progress:
            progress.current = done
            progress._render()

    results = enumerator.enumerate(progress_callback=on_progress)

    if progress:
        progress.finish()

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write("Directory Enumeration Results\n")
        f.write("=" * 40 + "\n")
        f.write(f"Target: {args.url}\n")
        f.write(f"Date: {datetime.now()}\n\n")
        for r in results:
            line = f"[{r.status_code}] {r.url}"
            if r.redirect_location:
                line += f" -> {r.redirect_location}"
            f.write(line + "\n")
            if not args.quiet:
                out.success(line)

    out.info(f"Found {len(results)} results. Saved to {output_path}")
    return 0


def _cmd_subdomain_scan(args: argparse.Namespace, out: Output) -> int:
    """Execute subdomain-scan command."""
    from cyber_arsenal.web.subdomain_scanner import SubdomainScanner
    from cyber_arsenal.utils.progress import ProgressBar

    wordlist = Path(args.wordlist)
    if not wordlist.exists():
        out.error(f"Wordlist not found: {wordlist}")
        return 1

    scanner = SubdomainScanner(
        args.domain,
        wordlist,
        threads=args.threads,
        protocol="https" if args.https else "http",
    )

    out.info(f"Domain: {args.domain}")
    out.info(f"Wordlist: {wordlist}")
    out.info(f"Protocol: {scanner.protocol}")

    progress = ProgressBar(total=0, prefix="Scanning") if not args.quiet else None

    def on_progress(done: int, total: int) -> None:
        if progress and progress.total != total:
            progress.total = total
        if progress:
            progress.current = done
            progress._render()

    results = scanner.scan(progress_callback=on_progress)

    if progress:
        progress.finish()

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write("Subdomain Discovery Results\n")
        f.write("=" * 40 + "\n")
        f.write(f"Domain: {args.domain}\n")
        f.write(f"Date: {datetime.now()}\n\n")
        for r in results:
            line = f"[{r.status_code}] {r.full_domain}"
            f.write(line + "\n")
            if not args.quiet:
                out.success(line)

    out.info(f"Found {len(results)} subdomains. Saved to {output_path}")
    return 0


def _cmd_port_scan(args: argparse.Namespace, out: Output) -> int:
    """Execute port-scan command."""
    from cyber_arsenal.network.port_scanner import PortScanner
    from cyber_arsenal.utils.progress import ProgressBar

    ports = _parse_ports(args.ports)
    scanner = PortScanner(
        args.target,
        ports=ports,
        threads=args.threads,
        grab_banners=args.grab_banners,
    )

    out.info(f"Target: {args.target}")
    out.info(f"Ports: {len(ports)}")

    progress = ProgressBar(total=len(ports), prefix="Scanning") if not args.quiet else None

    def on_progress(done: int, total: int) -> None:
        if progress:
            progress.current = done
            progress._render()

    results = scanner.scan(progress_callback=on_progress)

    if progress:
        progress.finish()

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write(f"Port Scan Results - {args.target}\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {datetime.now()}\n\n")
        for r in results:
            line = f"Port {r.port} OPEN"
            if r.banner:
                line += f" - {r.banner}"
            f.write(line + "\n")
            if not args.quiet:
                out.success(line)

    out.info(f"Found {len(results)} open ports. Saved to {output_path}")
    return 0


def _cmd_log_analyze(args: argparse.Namespace, out: Output) -> int:
    """Execute log-analyze command."""
    from cyber_arsenal.network.log_analyzer import LogAnalyzer

    log_path = Path(args.file)
    if not log_path.exists():
        out.error(f"Log file not found: {log_path}")
        return 1

    analyzer = LogAnalyzer(log_path, top_n=args.top_n)
    report = analyzer.analyze()

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write("Log Analysis Report\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {report.analyzed_at}\n")
        f.write(f"File: {log_path}\n\n")
        f.write(f"Total lines: {report.total_lines}\n\n")
        f.write("Top IPs:\n")
        for ip, count in report.top_ips:
            f.write(f"  {ip} -> {count}\n")
        f.write("\nError keywords:\n")
        for k, v in report.error_keywords.items():
            f.write(f"  {k.upper()} -> {v}\n")
        if report.status_codes:
            f.write("\nHTTP status codes (4xx/5xx):\n")
            for code, count in sorted(report.status_codes.items()):
                f.write(f"  {code} -> {count}\n")
        if report.anomalies:
            f.write("\nAnomalies:\n")
            for a in report.anomalies:
                f.write(f"  {a}\n")

    out.success("Log analysis completed")
    out.info(f"Top IPs: {len(report.top_ips)}")
    if report.anomalies:
        out.warning(f"Anomalies detected: {len(report.anomalies)}")
    out.info(f"Report saved to {output_path}")
    return 0


def main() -> int:
    """Main entry point."""
    parser = _create_parser()
    args = parser.parse_args()

    out = Output(verbose=args.verbose, quiet=args.quiet)
    if not args.no_banner and not args.quiet:
        out.banner()

    handlers = {
        "hash-crack": _cmd_hash_crack,
        "hash-identify": _cmd_hash_identify,
        "dir-enum": _cmd_dir_enum,
        "subdomain-scan": _cmd_subdomain_scan,
        "port-scan": _cmd_port_scan,
        "log-analyze": _cmd_log_analyze,
    }

    handler = handlers.get(args.command)
    if not handler:
        parser.print_help()
        return 1

    try:
        return handler(args, out)
    except (WordlistNotFoundError, InvalidHashError, TargetError) as e:
        out.error(str(e))
        return 1
    except CyberArsenalError as e:
        out.error(str(e))
        return 1
    except KeyboardInterrupt:
        out.warning("Interrupted by user")
        return 130
    except Exception as e:
        if args.verbose:
            raise
        out.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
