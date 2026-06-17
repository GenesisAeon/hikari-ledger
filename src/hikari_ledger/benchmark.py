"""Comparison benchmarks: PoR vs. Proof-of-Work energy, PoS randomness, BFT latency."""

from __future__ import annotations

from typing import Any

from hikari_ledger.constants import HIKARI_TARGETS

# Indicative, order-of-magnitude figures used purely for the qualitative
# comparison CLI command -- not hardware measurements.
POW_ENERGY_PER_BLOCK_KWH = 1_200.0  # Bitcoin-class PoW, order of magnitude
POS_ENERGY_PER_BLOCK_KWH = 0.05
POR_ENERGY_PER_BLOCK_KWH = HIKARI_TARGETS["energy_vs_pow_ratio"][0] * POW_ENERGY_PER_BLOCK_KWH

BFT_LATENCY_MS = 250.0
POR_LATENCY_MS = HIKARI_TARGETS["consensus_latency_ms"][0]


def energy_comparison() -> dict[str, Any]:
    return {
        "proof_of_work_kwh_per_block": POW_ENERGY_PER_BLOCK_KWH,
        "proof_of_stake_kwh_per_block": POS_ENERGY_PER_BLOCK_KWH,
        "proof_of_resonance_kwh_per_block": POR_ENERGY_PER_BLOCK_KWH,
        "por_vs_pow_efficiency_factor": POW_ENERGY_PER_BLOCK_KWH / POR_ENERGY_PER_BLOCK_KWH,
    }


def latency_comparison() -> dict[str, Any]:
    return {
        "bft_latency_ms": BFT_LATENCY_MS,
        "proof_of_resonance_latency_ms": POR_LATENCY_MS,
        "por_vs_bft_speedup": BFT_LATENCY_MS / POR_LATENCY_MS,
    }
