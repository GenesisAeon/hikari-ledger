# hikari-ledger

**Proof-of-Resonance distributed consensus** for genesis-os node networks — a
CREP-weighted alternative to Proof-of-Work and Proof-of-Stake.

[![CI](https://github.com/GenesisAeon/hikari-ledger/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/hikari-ledger/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Instead of energy-intensive hash computation (PoW) or capital-based staking
(PoS), Proof-of-Resonance (PoR) validates blocks based on each node's CREP
harmonic state — the same Coherence/Resonance/Emergence/Poetics tensor used
throughout the GenesisAeon ecosystem. Nodes whose CREP state is in higher
harmony with the network (higher Γ) earn proportionally more validation
weight; a block is accepted once weighted agreement crosses the classic
Byzantine fault tolerance threshold of 2/3.

## Installation

```bash
pip install hikari-ledger
```

## Usage

```python
from hikari_ledger import HikariLedger

ledger = HikariLedger(seed=42)
result = ledger.run_cycle(n_nodes=50, n_blocks=100)
print(result["acceptance_rate"])

print(ledger.get_crep_state())   # {"C": ..., "R": ..., "E": ..., "P": ..., "Gamma": ...}
print(ledger.get_utac_state())   # {"H": ..., "H_star": 0.667, "K": 1.0, ...}
print(ledger.get_phase_events())  # consensus failures / forks
print(ledger.to_zenodo_record())
```

Or via the CLI:

```bash
hikari-ledger run --nodes 50 --blocks 100
hikari-ledger simulate-attack --byzantine-fraction 0.30
hikari-ledger energy-comparison --vs-pow --vs-pos
```

## Physical mapping (UTAC)

| UTAC symbol | Meaning in PoR |
|---|---|
| `H(t)` | network consensus strength (fraction of weighted agreement) |
| `K` | 1.0 (perfect consensus) |
| `H*` | 2/3 (Byzantine fault tolerance threshold) |
| `Γ` | per-node CREP coupling, derived from coherence/resonance/emergence/poetics |

`Γ_PoR = arctanh(2/3) / σ ≈ 0.367` — close to the Manna sandpile criticality
value (0.376), suggesting PoR consensus naturally operates near dense
self-organized criticality.

## Role in the GenesisAeon Ecosystem

`hikari-ledger` is **P29** in the GenesisAeon CREP Criticality Spectrum,
representing the **distributed-systems** domain. It implements the
Proof-of-Resonance consensus layer used to coordinate `genesis-os` node
networks, weighting validation rights by each node's measured CREP state
rather than computational work or staked capital.

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20788575.svg)](https://doi.org/10.5281/zenodo.20788575)

---

Built with [uv](https://docs.astral.sh/uv/) · [Typer](https://typer.tiangolo.com/)
