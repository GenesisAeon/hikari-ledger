"""Plain (unweighted) Byzantine Fault Tolerant fallback consensus.

Used when the validator pool has not yet produced verifiable CREP states
(e.g. network bootstrap) -- falls back to classic one-node-one-vote BFT
with the same 2/3 agreement threshold as Proof-of-Resonance.
"""

from __future__ import annotations

from hikari_ledger.constants import CONSENSUS_THRESHOLD
from hikari_ledger.node import ValidatorNode


def bft_consensus(nodes: list[ValidatorNode]) -> bool:
    if not nodes:
        return False
    agreeing = sum(1 for node in nodes if not node.byzantine)
    return (agreeing / len(nodes)) > CONSENSUS_THRESHOLD


def max_tolerable_byzantine_fraction() -> float:
    """f < n/3 -- the classic BFT Byzantine tolerance bound."""
    return 1.0 - CONSENSUS_THRESHOLD
