# Cyber Arsenal — Architecture

This document describes the architecture, design decisions, and module structure of Cyber Arsenal.

---

## Design principles

1. **Modularity** — Each capability (crypto, network, web) lives in its own package with clear boundaries.
2. **Reusability** — Core logic is library-style; CLI is a thin layer on top.
3. **Consistency** — Shared config, logging, output, and error handling across all modules.
4. **Testability** — Pure functions and dependency injection where practical.

---

## Package structure

```
cyber_arsenal/
├── __init__.py          # Version
├── core/                # Shared infrastructure
│   ├── config.py        # Configuration dataclass
│   ├── logger.py        # Logging setup
│   └── exceptions.py    # Custom exceptions
├── crypto/              # Hash tools
│   ├── hashiden.py      # Hash identification
│   └── hashcracker.py   # Hash cracking
├── network/             # Network tools
│   ├── port_scanner.py # TCP port scanner
│   └── log_analyzer.py # Log analysis
├── web/                 # Web recon tools
│   ├── dir_enum.py     # Directory enumeration
│   └── subdomain_scanner.py
├── utils/               # Shared utilities
│   ├── output.py       # Colored output, banner
│   └── progress.py     # Progress bar
└── cli/                 # CLI layer
    └── main.py         # Argument parsing, command dispatch
```

---

## Data flow

```
User → arsenal.py → cli/main.py → Command handler → Module (crypto/network/web)
                                        ↓
                              Output / Progress / Logging
```

- **arsenal.py**: Entry point; delegates to `cyber_arsenal.cli.main.main()`.
- **cli/main.py**: Parses args, creates `Output` instance, dispatches to command handlers.
- **Command handlers**: Instantiate module classes, call methods, write results to files.

---

## Key abstractions

### Output

`cyber_arsenal.utils.output.Output` provides:

- `info()`, `success()`, `warning()`, `error()` — Colored messages
- `verbose_msg()` — Only when `--verbose`
- `banner()` — Startup banner
- Respects `--quiet` to suppress non-essential output

### Exceptions

- `CyberArsenalError` — Base
- `WordlistNotFoundError` — Missing wordlist file
- `InvalidHashError` — Unsupported or malformed hash
- `TargetError` — Invalid target (IP, URL, file)
- `ConfigurationError` — Invalid config

### Progress

`ProgressBar` in `utils/progress.py` supports long-running operations. Callbacks like `(done, total)` allow modules to report progress without depending on the progress bar implementation.

---

## Module responsibilities

### core

- **config.py**: Global settings (timeouts, threads, wordlist paths).
- **logger.py**: Centralized logging setup.
- **exceptions.py**: Domain-specific exceptions.

### crypto

- **hashiden.py**: Identify hash type from string (prefix, length, entropy).
- **hashcracker.py**: Crack hashes via wordlist or brute-force (short passwords).

### network

- **port_scanner.py**: Threaded TCP connect scan, optional banner grab.
- **log_analyzer.py**: IP extraction, error keywords, HTTP status codes, anomaly detection (z-score).

### web

- **dir_enum.py**: Threaded HTTP requests for directory paths; status filtering.
- **subdomain_scanner.py**: Threaded HTTP checks for subdomains; exclude 404 by default.

### utils

- **output.py**: Terminal output with colors and quiet/verbose modes.
- **progress.py**: Progress bar for scans and enumeration.

### cli

- **main.py**: `argparse` setup, subcommands, command handlers, error handling.

---

## Concurrency

- **Port scanner**: `ThreadPoolExecutor` for parallel port checks.
- **Dir enum**: `ThreadPoolExecutor` for parallel HTTP requests.
- **Subdomain scanner**: Same pattern.
- **Hash cracker**: Single-threaded (CPU-bound; GIL limits benefit; can be parallelized later with `multiprocessing`).

---

## Extensibility

To add a new command:

1. Add subparser in `cli/main.py`.
2. Implement handler function `_cmd_<name>(args, out) -> int`.
3. Register in `handlers` dict.
4. Optionally add a new module under `cyber_arsenal/` if the feature is substantial.

---

## Dependencies

- **Standard library**: `hashlib`, `socket`, `re`, `argparse`, `concurrent.futures`, etc.
- **External**: `requests` (for web modules only).

No heavy dependencies; suitable for minimal environments.
