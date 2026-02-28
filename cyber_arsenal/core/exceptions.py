"""Custom exceptions for Cyber Arsenal."""


class CyberArsenalError(Exception):
    """Base exception for Cyber Arsenal."""

    pass


class WordlistNotFoundError(CyberArsenalError):
    """Raised when a wordlist file is not found."""

    pass


class InvalidHashError(CyberArsenalError):
    """Raised when hash format is invalid or unsupported."""

    pass


class TargetError(CyberArsenalError):
    """Raised when target specification is invalid."""

    pass


class ConfigurationError(CyberArsenalError):
    """Raised when configuration is invalid."""

    pass
