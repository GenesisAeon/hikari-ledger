"""Tests for the Proof-of-Resonance consensus engine."""

import random

from hikari_ledger.consensus import ProofOfResonanceValidator, run_consensus_round
from hikari_ledger.network import build_network, run_crep_cycle


def test_weights_sum_to_one():
    nodes = build_network(10, rng=random.Random(1))
    run_crep_cycle(nodes, rng=random.Random(1))
    weights = ProofOfResonanceValidator.weights_for(nodes)
    assert abs(sum(weights.values()) - 1.0) < 1e-9


def test_honest_network_reaches_consensus():
    rng = random.Random(7)
    nodes = build_network(50, byzantine_fraction=0.0, rng=rng)
    run_crep_cycle(nodes, rng=rng)
    result = run_consensus_round(nodes, {"seq": 0}, rng=rng)
    assert result.accepted is True
    assert result.weighted_agreement > 2 / 3


def test_majority_byzantine_network_fails_consensus():
    rng = random.Random(7)
    nodes = build_network(50, byzantine_fraction=0.6, rng=rng)
    run_crep_cycle(nodes, rng=rng)
    result = run_consensus_round(nodes, {"seq": 0}, rng=rng)
    assert result.accepted is False
