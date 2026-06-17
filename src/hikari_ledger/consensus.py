"""Proof-of-Resonance consensus engine.

Node i validates with weight w_i = Gamma_i / sum_j Gamma_j.
A block is accepted when the weighted agreement exceeds the Byzantine
fault tolerance threshold (2/3, see ``hikari_ledger.constants``).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from hikari_ledger.constants import CONSENSUS_THRESHOLD
from hikari_ledger.node import ValidatorNode


@dataclass
class ConsensusResult:
    accepted: bool
    weighted_agreement: float
    weights: dict[str, float]
    agreeing_nodes: list[str]


class ProofOfResonanceValidator:
    """Evaluates a node's CREP state and assigns it a validation weight."""

    @staticmethod
    def weights_for(nodes: list[ValidatorNode]) -> dict[str, float]:
        total_gamma = sum(max(node.gamma, 0.0) for node in nodes)
        if total_gamma <= 0:
            # Degenerate case: no node has produced a CREP state yet.
            # Fall back to one-node-one-vote (plain BFT) weighting.
            n = len(nodes) or 1
            return {node.node_id: 1.0 / n for node in nodes}
        return {node.node_id: max(node.gamma, 0.0) / total_gamma for node in nodes}

    @staticmethod
    def minimum_gamma_threshold() -> float:
        """Minimum Gamma a node must report to be eligible to validate."""
        return 1e-6


def run_consensus_round(
    nodes: list[ValidatorNode],
    block_payload: dict[str, Any],
    rng: random.Random | None = None,
) -> ConsensusResult:
    """Run one Proof-of-Resonance consensus round over ``nodes``.

    Byzantine nodes (``node.byzantine``) disagree with the honest majority;
    every other node agrees, simulating a quorum proposing a valid block.
    """
    rng = rng or random.Random()
    weights = ProofOfResonanceValidator.weights_for(nodes)

    agreeing_nodes: list[str] = []
    weighted_agreement = 0.0
    for node in nodes:
        agrees = not node.byzantine
        if agrees:
            agreeing_nodes.append(node.node_id)
            weighted_agreement += weights[node.node_id]

    accepted = weighted_agreement > CONSENSUS_THRESHOLD
    return ConsensusResult(
        accepted=accepted,
        weighted_agreement=weighted_agreement,
        weights=weights,
        agreeing_nodes=agreeing_nodes,
    )
