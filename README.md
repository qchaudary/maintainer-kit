# MaintainerKit 🛠️

[![CI](https://github.com/qchaudary/maintainer-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/qchaudary/maintainer-kit/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/github/v/release/qchaudary/maintainer-kit?label=release)](https://github.com/qchaudary/maintainer-kit/releases)

> **Open-source maintenance automation for GitHub projects.**
> A GitHub-native toolkit for issue triage, PR review preparation, release management, repository health, and maintainer automation.

---

## Why MaintainerKit?

Open-source maintainers spend hundreds of hours triaging duplicate issues, preparing context for reviewers, compiling release notes, and checking baseline repository standards.

Inspired by initiatives like OpenAI's **Symphony** and **Codex for Open Source**, **MaintainerKit** provides deterministic, workflow-native automation for maintainers that works 100% offline out-of-the-box, with an optional AI layer (OpenAI/Codex) for deep semantic reasoning.

*MaintainerKit is self-dogfooded: we use MaintainerKit to maintain MaintainerKit.*

---

## Strategic Roadmap & Releases

- **v0.1 — Foundation**
  - Fast CLI & zero-dependency architecture
  - Repository health audits (100/100 standard)
  - Issue classification heuristics
  - Composite GitHub Action (`action.yml`)
  - Full CI test suite
- **v0.2 — Maintainer Automation (Current)**
  - Live GitHub API issue triage and PR review bot comments
  - Automated changelog & release-notes generator from merged PRs and commit history
  - Non-invasive human reviewer boundary (no unauthorized automerges)
- **v0.3 — AI Assistance**
  - Optional OpenAI / Codex provider with structured JSON outputs
  - Semantic issue summarization and PR review checklists
- **v0.4 — Security**
  - Packaging manifest audits & dependency CVE verification
  - Secret & sensitive configuration checks
- **v1.0 — Stable Ecosystem**
  - Stable CLI, comprehensive docs, and multi-repo adoption

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
# Triage local text
maintainerkit triage --title "Crash on JWT validation in auth header" --body "Traceback shows token expired exception"

# Or triage a live GitHub issue and post a maintainer report comment
maintainerkit triage --issue 1 --repo qchaudary/maintainer-kit --comment
```

### 3. PR Review Risk Preparation
```bash
# Inspect changed files
maintainerkit review --pr 142 --title "Refactor session tokens" --files src/auth/token.py pyproject.toml --added 312 --removed 91

# Or inspect a live PR directly from GitHub
maintainerkit review --pr 1 --repo qchaudary/maintainer-kit --comment
```

### 4. Generate Release Notes
```bash
# Generate release notes from merged PRs (or git commit history)
maintainerkit release --version v0.2.0 --repo qchaudary/maintainer-kit
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
  workflow_dispatch:

jobs:
  maintainerkit:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: qchaudary/maintainer-kit@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.
