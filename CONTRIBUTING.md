# Contributing to MaintainerKit

Thank you for your interest in improving MaintainerKit!

## Development Setup

1. Fork and clone the repository:
   `ash
   git clone https://github.com/qchaudary/maintainer-kit.git
   cd maintainer-kit
   `
2. Create and activate a virtual environment:
   `ash
   python -m venv .venv
   source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate
   `
3. Install dependencies in editable mode:
   `ash
   pip install -e .[dev]
   `
4. Run tests:
   `ash
   pytest tests/ -v
   `

## Pull Request Guidelines

- All PRs should include tests confirming new features or bugfixes.
- Follow PEP8 naming conventions.
- MaintainerKit dogfoods its own review analyzer on every PR.
