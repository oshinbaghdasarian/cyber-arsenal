"""Logging system for Cyber Arsenal."""

import logging
import sys
from typing import Optional


def setup_logging(
    verbose: bool = False,
    quiet: bool = False,
    log_file: Optional[str] = None,
) -> None:
    """Configure logging for the application.

    Args:
        verbose: Enable debug-level logging.
        quiet: Suppress non-essential output.
        log_file: Optional file path for log output.
    """
    level = logging.DEBUG if verbose else logging.INFO
    if quiet:
        level = logging.WARNING

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]

    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given module name."""
    return logging.getLogger(name)
