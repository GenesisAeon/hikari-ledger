"""Tests for CREP evaluation helpers."""

import math

from hikari_ledger.constants import GAMMA_POR
from hikari_ledger.crep_validator import (
    compute_gamma,
    eta_from_gamma,
    evaluate_node_crep,
    gini_coefficient,
)


def test_compute_gamma_bounds():
    assert compute_gamma(1.0, 1.0, 1.0, 1.0) == 1.0
    assert compute_gamma(0.0, 1.0, 1.0, 1.0) == 0.0


def test_gamma_por_matches_two_thirds_threshold():
    eta = eta_from_gamma(GAMMA_POR)
    assert math.isclose(eta, 2 / 3, rel_tol=1e-3)


def test_evaluate_node_crep_returns_bounded_state():
    state = evaluate_node_crep(0.8, 0.1, 0.7, [0.4, 0.5, 0.6])
    assert 0.0 <= state.gamma <= 1.0
    assert 0.0 <= state.coherence <= 1.0


def test_gini_coefficient_equal_distribution_is_zero():
    assert gini_coefficient([0.5, 0.5, 0.5]) == 0.0


def test_gini_coefficient_unequal_distribution_is_positive():
    assert gini_coefficient([0.0, 0.0, 1.0]) > 0.0
