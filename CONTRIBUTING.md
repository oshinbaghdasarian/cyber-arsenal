# Contributing to Cyber Arsenal

Thank you for your interest in contributing. This document provides guidelines for contributing to the project.

---

## Code of conduct

- Be respectful and professional.
- Focus on constructive feedback.
- This project is for authorized security testing and education only.

---

## Development setup

```bash
git clone https://github.com/your-org/cyber-arsenal.git
cd cyber-arsenal
pip install -e ".[dev]"  # If dev extras exist
# or
pip install -e .
pip install -r requirements.txt
```

---

## Code style

- **Python**: Follow PEP 8. Use type hints and Google-style docstrings.
- **Formatting**: Black (if adopted), or consistent 4-space indentation.
- **Imports**: Standard library first, then third-party, then local. Use absolute imports from `cyber_arsenal`.

---

## Project structure

- `cyber_arsenal/` — Main package. Add new modules here.
- `cyber_arsenal/core/` — Shared config, logging, exceptions.
- `cyber_arsenal/utils/` — Output, progress, helpers.
- `cyber_arsenal/cli/` — CLI and command handlers.

---

## Adding a new command

1. **Create module** (if needed) under `cyber_arsenal/<module>/`.
2. **Add subparser** in `cyber_arsenal/cli/main.py`.
3. **Implement handler** `_cmd_<name>(args, out) -> int`.
4. **Register** in the `handlers` dict.
5. **Document** in README.md, CLI_USAGE.md, and module README.

---

## Testing

- Run existing tools manually: `python arsenal.py <command> --help`
- Test against local targets (e.g., localhost, test VMs).
- Do not run aggressive scans against unauthorized targets.

---

## Pull requests

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make changes with clear commits.
4. Update documentation as needed.
5. Submit a PR with a description of changes and motivation.

---

## Reporting issues

- Use the issue tracker for bugs and feature requests.
- Include: Python version, OS, command used, and error output.
- For security issues, consider responsible disclosure.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
