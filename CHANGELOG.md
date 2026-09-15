# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.1] - 2026-09-15

### Fixed (documentation/metadata honesty, no numeric value change)
- **Ecosystem-wide Γ-circularity review**: `GAMMA_POR` (≈0.367) rescales
  a genuine mathematical fact (Byzantine fault tolerance requires >2/3
  agreement) through `SIGMA=2.2` — a shared default reused unchanged
  across unrelated GenesisAeon UTAC packages, never independently
  derived for distributed-consensus systems. The numeric value is
  unchanged; removed language presenting it as independently comparable
  across domains, including a specific false-coincidence claim
  ("close to the Manna sandpile criticality value (0.376), suggesting
  PoR consensus naturally operates near dense self-organized
  criticality" — `sandpile-utac`'s `MANNA_GAMMA` shares the identical
  `SIGMA=2.2`, so this "closeness" is an artifact of the shared
  constant, not a physical finding). Updated `constants.py`,
  `README.md`, `.zenodo.json`. See
  `D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md` for the
  full ecosystem-wide finding.

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
