# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Licensing migrated from MIT in the original v0.1.0 foundation to Apache-2.0 during v0.2 development.

## [0.1.0] - 2026-09-10

### Added
- **Issue Triage**: Heuristic-based classification of labels, priority, area, and maintainer response urgency.
- **PR Review Preparation**: Risk scoring, sensitive file changes alert (auth, CI, crypto), missing test delta detection.
- **Release Assistant**: Automated changelog and release notes generation from merged PR metadata.
- **Repository Health**: Audit scoring engine checking for license, documentation, security policy, and templates.
- **GitHub Action**: Reusable workflow action for automated repository triage and health monitoring.
- **Optional AI Provider**: Clean fallback architecture supporting OpenAI API models for enhanced semantic reasoning.

### Licensing
- The authentic v0.1.0 baseline commit was released under the MIT License.
