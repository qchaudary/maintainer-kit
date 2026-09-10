# MaintainerKit 🛠️

[![CI](https://github.com/qchaudary/maintainerkit/actions/workflows/ci.yml/badge.svg)](https://github.com/qchaudary/maintainerkit/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Open-source maintenance automation for GitHub projects.**
> A GitHub-native toolkit for issue triage, PR review preparation, release management, repository health, and maintainer automation.

---

## Why MaintainerKit?

Open-source maintainers spend hundreds of hours triaging issues, preparing PR context for reviewers, compiling release notes, and enforcing baseline repository standards.

Inspired by initiatives like OpenAI's **Symphony** and **Codex for Open Source**, **MaintainerKit** provides deterministic, workflow-native automation for maintainers that works 100% offline out-of-the-box, with an optional AI layer (OpenAI/Codex) for deep semantic reasoning.

---

## Strategic Roadmap & Releases

- **v0.1 — Foundation (Current)**
  - Fast CLI & zero-dependency architecture
  - Repository health audits (100/100 standard)
  - Issue classification & deterministic rule heuristics
  - Composite GitHub Action (`action.yml`)
  - Full test suite & CI workflows
- **v0.2 — Maintainer Automation**
  - Advanced label management & stale issue/PR detection
  - PR metadata & risk analysis
  - Semantic release-notes generation
- **v0.3 — AI Assistance**
  - Optional OpenAI / Codex provider
  - Structured issue analysis & prompt configurations
  - Human approval boundaries (no autonomous merges)
- **v0.4 — Security**
  - Dependency verification & packaging manifest audits
  - Secret & sensitive config checks
  - Responsible vulnerability disclosure process
- **v1.0 — Stable Ecosystem**
  - Stable CLI, comprehensive docs, and multi-repo dogfooding

---

## Quickstart

### Installation

```bash
git clone https://github.com/qchaudary/maintainerkit.git
cd maintainerkit
pip install -e .
```

### 1. Check Repository Health
```bash
maintainerkit health .
```
Output:
```text
Repository Health Report
----------------------------------------
License                   [PASS]
Documentation (README)    [PASS]
Security Policy           [PASS]
Contributing Guide        [PASS]
Code of Conduct           [PASS]
Issue Templates           [PASS]
Pull Request Template     [PASS]
CI Workflow               [PASS]
----------------------------------------
Overall Score: 100/100
```

### 2. Issue Triage
```bash
maintainerkit triage --title "Crash on JWT validation in auth header" --body "Traceback shows token expired exception"
```

### 3. PR Review Risk Preparation
```bash
maintainerkit review --pr 142 --title "Refactor session tokens" --files src/auth/token.py pyproject.toml --added 312 --removed 91
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
      - uses: qchaudary/maintainerkit@v1
        with:
          mode: health
```

---

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.
