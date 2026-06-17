"""Calibration constants for the Proof-of-Resonance (PoR) consensus model.

See README.md / RELEASE_GUIDE.md for the physical mapping from the UTAC
(Universal Threshold Activation Curve) framework to distributed consensus:

    H(t)  <- network consensus strength (fraction of validation weight agreeing)
    K     <- 1.0 (perfect consensus)
    H*    <- 2/3 (Byzantine fault tolerance threshold)
    sigma <- CREP coupling constant
"""

import math

# CREP coupling constant (shared across the GenesisAeon CREP Criticality Spectrum).
SIGMA = 2.2

# Byzantine fault tolerance threshold: at least 2/3 of weighted validation
# power must agree for a block to be accepted.
CONSENSUS_THRESHOLD = 2.0 / 3.0

# Maximum fraction of (weighted) Byzantine/incoherent nodes the network can
# tolerate before consensus becomes structurally impossible (f < n/3).
BYZANTINE_TOLERANCE = 1.0 / 3.0

# eta_PoR = H*/K = 2/3 -> Gamma_PoR = arctanh(eta_PoR) / sigma
GAMMA_POR = math.atanh(CONSENSUS_THRESHOLD) / SIGMA  # ~= 0.367

# Benchmark targets (value, tolerance) used by benchmark.py / tests.
HIKARI_TARGETS = {
    "consensus_threshold": (CONSENSUS_THRESHOLD, 0.01),
    "gamma_por": (GAMMA_POR, 0.02),
    "energy_vs_pow_ratio": (0.001, 0.002),
    "consensus_latency_ms": (100.0, 50.0),
    "byzantine_tolerance_pct": (33.0, 2.0),
    "crep_gini_coefficient": (0.30, 0.10),
}
