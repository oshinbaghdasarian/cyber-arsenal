"""Output utilities - colors, banners, and progress indicators."""

import sys
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @staticmethod
    def disable() -> None:
        """Disable colors (e.g., when not a TTY)."""
        Colors.RED = ""
        Colors.GREEN = ""
        Colors.YELLOW = ""
        Colors.BLUE = ""
        Colors.MAGENTA = ""
        Colors.CYAN = ""
        Colors.WHITE = ""
        Colors.BOLD = ""
        Colors.DIM = ""
        Colors.RESET = ""


class Output:
    """Unified output handler with color support and quiet/verbose modes."""

    def __init__(self, verbose: bool = False, quiet: bool = False, use_colors: bool = True):
        """Initialize output handler.

        Args:
            verbose: Enable verbose output.
            quiet: Suppress non-essential output.
            use_colors: Enable colored output (disabled if not TTY).
        """
        self.verbose = verbose
        self.quiet = quiet
        self._colors = use_colors and sys.stdout.isatty()
        if not self._colors:
            Colors.disable()

    def _write(self, msg: str, color: str = "") -> None:
        """Write message with optional color."""
        if self.quiet:
            return
        if color and self._colors:
            sys.stdout.write(f"{color}{msg}{Colors.RESET}")
        else:
            sys.stdout.write(msg)
        sys.stdout.flush()

    def info(self, msg: str) -> None:
        """Print info message (blue)."""
        self._write(f"[*] {msg}\n", Colors.BLUE)

    def success(self, msg: str) -> None:
        """Print success message (green)."""
        self._write(f"[+] {msg}\n", Colors.GREEN)

    def warning(self, msg: str) -> None:
        """Print warning message (yellow)."""
        self._write(f"[!] {msg}\n", Colors.YELLOW)

    def error(self, msg: str) -> None:
        """Print error message (red)."""
        self._write(f"[-] {msg}\n", Colors.RED)

    def verbose_msg(self, msg: str) -> None:
        """Print verbose message (dim) - only if verbose mode."""
        if self.verbose:
            self._write(f"[~] {msg}\n", Colors.DIM)

    def banner(self) -> None:
        """Print the Cyber Arsenal banner."""
        if self.quiet:
            return
        banner_text = f"""
{Colors.CYAN}{Colors.BOLD}
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
{Colors.RESET}  {Colors.DIM}Red Team Toolkit • v1.0.0 • Authorized Testing Only{Colors.RESET}
"""
        sys.stdout.write(banner_text)
        sys.stdout.flush()
