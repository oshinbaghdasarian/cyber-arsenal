"""Progress indicator utilities."""

import sys
from typing import Optional

from cyber_arsenal.utils.output import Colors


class ProgressBar:
    """Simple progress bar for long-running operations."""

    def __init__(
        self,
        total: int,
        prefix: str = "Progress",
        width: int = 40,
        use_colors: bool = True,
    ):
        """Initialize progress bar.

        Args:
            total: Total number of items.
            prefix: Prefix text before the bar.
            width: Bar width in characters.
            use_colors: Enable colored output.
        """
        self.total = total
        self.prefix = prefix
        self.width = width
        self.current = 0
        self._colors = use_colors and sys.stdout.isatty()

    def update(self, n: int = 1) -> None:
        """Update progress by n items."""
        self.current = min(self.current + n, self.total)
        self._render()

    def _render(self) -> None:
        """Render the progress bar."""
        if self.total == 0:
            pct = 100.0
        else:
            pct = 100.0 * self.current / self.total

        filled = int(self.width * self.current / self.total) if self.total else self.width
        bar = "█" * filled + "░" * (self.width - filled)

        color = Colors.GREEN if self._colors else ""
        reset = Colors.RESET if self._colors else ""

        sys.stdout.write(f"\r{self.prefix}: [{color}{bar}{reset}] {pct:.1f}% ({self.current}/{self.total})")
        sys.stdout.flush()

    def finish(self) -> None:
        """Mark progress as complete and print newline."""
        sys.stdout.write("\n")
        sys.stdout.flush()
