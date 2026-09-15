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
#
# HONESTY NOTE (2026-09-15, ecosystem-wide Gamma-circularity review):
# CONSENSUS_THRESHOLD=2/3 is a genuine, rigorously derived mathematical
# fact (Byzantine fault tolerance requires n > 3f, i.e. > 2/3 agreement)
# -- unlike the empirical thresholds used elsewhere in the GenesisAeon
# ecosystem, this one is not an estimate. However SIGMA=2.2 is the same
# shared default reused unchanged across unrelated UTAC packages (Amazon,
# AMOC, Cygnus X-1 jets, solar flares, neural avalanches, sandpile SOC),
# never independently derived for distributed-consensus systems. GAMMA_POR
# is therefore a well-defined rescaling of a real threshold, but -- like
# the other packages sharing SIGMA=2.2 -- it is NOT independently
# comparable to other domains' Gamma values; any apparent "closeness" to
# another package's Gamma (e.g. sandpile-utac's MANNA_GAMMA=0.376) is an
# artifact of both domains' threshold fractions being similar in magnitude
# and passing through the same shared constant, not evidence of shared
# underlying physics. See
# D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md for the full
# ecosystem-wide finding.
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
