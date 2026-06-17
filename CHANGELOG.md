# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026
### Added
- Initial v1.0.0 release of `hikari-ledger` — Proof-of-Resonance (PoR)
  distributed consensus for genesis-os node networks (GenesisAeon
  Package 29). Replaces the previous unfilled `diamond-setup` scaffold
  content with a real implementation: CREP-weighted validator nodes,
  weighted-BFT consensus engine, BFT fallback, block/chain structures,
  the `HikariCurrencyMinter` token model, and the `HikariLedger` Diamond
  Interface (`run_cycle`, `get_crep_state`, `get_utac_state`,
  `get_phase_events`, `to_zenodo_record`).
- CLI (`hikari-ledger run|simulate-attack|energy-comparison|version`).
- Standardized release tooling: `.zenodo.json`, GitHub Actions release
  workflow (`.github/workflows/release.yml`), `RELEASE_GUIDE.md`,
  `CONTRIBUTING.md`, issue/PR templates.

### Changed
- Project metadata (`pyproject.toml`) normalized: name (`hikari-ledger`),
  version, description, license, authors, `requires-python`.
