# MaintainerKit 🛠️

[![CI](https://github.com/qchaudary/maintainer-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/qchaudary/maintainer-kit/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Open-source maintenance automation for GitHub projects.**
> A GitHub-native toolkit for issue triage, PR review preparation, release management, repository health, and maintainer automation.

---

## Why MaintainerKit?

Open-source maintainers spend hundreds of hours triaging duplicate issues, preparing PR context for reviewers, compiling release notes, and checking baseline repository standards.

Inspired by initiatives like OpenAI's **Symphony** and **Codex for Open Source**, **MaintainerKit** provides deterministic, workflow-native automation for maintainers that works 100% offline out-of-the-box, with an optional AI layer (OpenAI/Codex) for deep semantic reasoning.

---

## Key Features

- 🎯 **Issue Triage**: Automatically classify issue type, priority, code area, and maintainer response urgency.
- 🔍 **PR Review Preparation**: Generate structured PR risk reports highlighting sensitive logic touchpoints (Auth, Crypto, CI/CD) and missing test coverage deltas.
- 🚀 **Release Assistant**: Aggregate merged pull requests into categorized Keep-A-Changelog release notes with contributor attribution.
- 🏥 **Repository Health Audit**: Run `maintainerkit health` to verify license, security policy, CI workflows, and templates with a 0–100 quality score.
- 🤖 **GitHub Action**: Drop-in composite action for zero-configuration repository automation.
- 🧠 **Optional AI Provider**: Use OpenAI / Codex API models when an API key is available, falling back gracefully to deterministic heuristics.

---

## Quickstart

### Installation

```bash
git clone https://github.com/qchaudary/maintainer-kit.git
cd maintainer-kit
pip install -e .
```

### 1. Check Repository Health
```bash
maintainerkit health .
```
Output:
```text
Repository Health Report
────────────────────────────────────────
License                   ✓
Documentation (README)    ✓
Security Policy           ✓
Contributing Guide        ✓
Code of Conduct           ✓
Issue Templates           ✓
Pull Request Template     ✓
CI Workflow               ✓
────────────────────────────────────────
Overall Score: 100/100
```

### 2. Issue Triage
```bash
maintainerkit triage --title "Crash on JWT validation in auth service" --body "Traceback on line 42"
```

### 3. PR Review Risk Preparation
```bash
maintainerkit review --pr 142 --title "Refactor session tokens" --files src/auth/token.py requirements.txt --added 312 --removed 91
```

### 4. Generate Release Notes
```bash
maintainerkit release --version v0.1.0
```

---

## GitHub Action Usage

Add MaintainerKit directly to your repository:

```yaml
name: MaintainerKit Automation

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened, synchronize]

jobs:
  maintainerkit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: qchaudary/maintainer-kit@v1
        with:
          mode: health
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
