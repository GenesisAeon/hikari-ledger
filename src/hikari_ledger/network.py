"""P2P validator network simulation."""

from __future__ import annotations

import random

from hikari_ledger.crep_validator import CREPState, evaluate_node_crep
from hikari_ledger.node import ValidatorNode


def build_network(
    n_nodes: int, byzantine_fraction: float = 0.0, rng: random.Random | None = None
) -> list[ValidatorNode]:
    """Build a validator pool, marking ``byzantine_fraction`` of nodes as faulty."""
    rng = rng or random.Random()
    n_byzantine = int(round(n_nodes * byzantine_fraction))
    byzantine_indices = set(rng.sample(range(n_nodes), n_byzantine)) if n_byzantine else set()
    return [
        ValidatorNode(node_id=f"node-{i:04d}", byzantine=(i in byzantine_indices))
        for i in range(n_nodes)
    ]


def run_crep_cycle(nodes: list[ValidatorNode], rng: random.Random | None = None) -> list[CREPState]:
    """Have every node produce a fresh CREP state for one UTAC cycle.

    Honest nodes draw high-coherence, high-resonance parameters; Byzantine
    nodes are simulated as low-coherence (their states are less internally
    consistent), which is exactly the failure mode PoR is designed to
    downweight automatically via w_i = Gamma_i / sum(Gamma).
    """
    rng = rng or random.Random()
    states: list[CREPState] = []

    raw_gammas = [rng.uniform(0.3, 0.7) for _ in nodes]
    mean_gamma_guess = sum(raw_gammas) / len(raw_gammas) if raw_gammas else 0.0
    for node, guess in zip(nodes, raw_gammas, strict=True):
        distance = abs(guess - mean_gamma_guess)
        if node.byzantine:
            phase_alignment = rng.uniform(0.0, 0.4)
            agreement = rng.uniform(0.0, 0.3)
        else:
            phase_alignment = rng.uniform(0.7, 1.0)
            agreement = rng.uniform(0.6, 1.0)
        state = evaluate_node_crep(
            phase_alignment=phase_alignment,
            crep_distance_to_mean=min(distance, 1.0),
            agreement_beyond_chance=agreement,
            validator_gammas=raw_gammas,
        )
        node.update_crep_state(state)
        states.append(state)
    return states
