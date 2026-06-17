"""Per-node CREP (Coherence, Resonance, Emergence, Poetics) evaluation."""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass

from hikari_ledger.constants import SIGMA


@dataclass(frozen=True)
class CREPState:
    """A single node's CREP tensor and the derived UTAC coupling Gamma."""

    coherence: float
    resonance: float
    emergence: float
    poetics: float
    gamma: float

    def as_dict(self) -> dict[str, float]:
        return {
            "C": self.coherence,
            "R": self.resonance,
            "E": self.emergence,
            "P": self.poetics,
            "Gamma": self.gamma,
        }


def compute_gamma(coherence: float, resonance: float, emergence: float, poetics: float) -> float:
    """Combine the four CREP components into a single Gamma coupling value.

    Gamma is the geometric mean of the four (clamped, non-negative) CREP
    components, which keeps it bounded in [0, 1] when each component is.
    """
    components = [max(0.0, min(1.0, c)) for c in (coherence, resonance, emergence, poetics)]
    product = math.prod(components)
    return product ** 0.25 if product > 0 else 0.0


def evaluate_node_crep(
    phase_alignment: float,
    crep_distance_to_mean: float,
    agreement_beyond_chance: float,
    validator_gammas: list[float],
) -> CREPState:
    """Evaluate a node's CREP state for one consensus round.

    Args:
        phase_alignment: cross-node phase coherence in [0, 1] (component C).
        crep_distance_to_mean: |Gamma_i - mean(Gamma)| normalised to [0, 1];
            used to derive resonance (component R) -- smaller distance means
            higher resonance with the network mean.
        agreement_beyond_chance: fraction of agreement above the 1/n random
            baseline, clamped to [0, 1] (component E).
        validator_gammas: Gamma values of all validators in the round, used
            to compute the entropy-based Poetics component (P).
    """
    coherence = max(0.0, min(1.0, phase_alignment))
    resonance = max(0.0, min(1.0, 1.0 - crep_distance_to_mean))
    emergence = max(0.0, min(1.0, agreement_beyond_chance))
    poetics = _normalised_entropy(validator_gammas)
    gamma = compute_gamma(coherence, resonance, emergence, poetics)
    return CREPState(coherence, resonance, emergence, poetics, gamma)


def _normalised_entropy(values: list[float]) -> float:
    """Shannon entropy of a value distribution, normalised to [0, 1]."""
    if not values or len(values) < 2:
        return 0.0
    total = sum(values)
    if total <= 0:
        return 0.0
    probs = [v / total for v in values if v > 0]
    entropy = -sum(p * math.log(p) for p in probs)
    max_entropy = math.log(len(values))
    return entropy / max_entropy if max_entropy > 0 else 0.0


def eta_from_gamma(gamma: float, sigma: float = SIGMA) -> float:
    """Inverse of the UTAC efficiency mapping: eta = tanh(sigma * Gamma)."""
    return math.tanh(sigma * gamma)


def gini_coefficient(values: list[float]) -> float:
    """Gini coefficient of a non-negative distribution (0 = perfectly equal)."""
    n = len(values)
    if n == 0:
        return 0.0
    sorted_vals = sorted(values)
    cumulative = 0.0
    weighted_sum = 0.0
    total = sum(sorted_vals)
    if total == 0:
        return 0.0
    for i, v in enumerate(sorted_vals, start=1):
        cumulative += v
        weighted_sum += i * v
    return (2 * weighted_sum) / (n * total) - (n + 1) / n


def mean_gamma(states: list[CREPState]) -> float:
    if not states:
        return 0.0
    return statistics.fmean(s.gamma for s in states)
