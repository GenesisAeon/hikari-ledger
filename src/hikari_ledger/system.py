"""HikariLedger -- the GenesisAeon Diamond Interface implementation for
Package 29 (Proof-of-Resonance distributed consensus)."""

from __future__ import annotations

import random
import statistics
from typing import Any

from hikari_ledger.bft_fallback import max_tolerable_byzantine_fraction
from hikari_ledger.block import GENESIS_HASH, Block
from hikari_ledger.consensus import run_consensus_round
from hikari_ledger.constants import CONSENSUS_THRESHOLD, GAMMA_POR, SIGMA
from hikari_ledger.crep_validator import eta_from_gamma, gini_coefficient
from hikari_ledger.hikari_currency import HikariCurrencyMinter
from hikari_ledger.network import build_network, run_crep_cycle
from hikari_ledger.node import ValidatorNode


class HikariLedger:
    """Diamond Interface system class for the Proof-of-Resonance ledger.

    Simulates a validator network running PoR consensus over a series of
    blocks and exposes the resulting CREP/UTAC state, phase events (forks
    and consensus failures), and a Zenodo-ready summary record.
    """

    def __init__(self, byzantine_fraction: float = 0.0, seed: int | None = 42) -> None:
        self.byzantine_fraction = byzantine_fraction
        self._rng = random.Random(seed)
        self.nodes: list[ValidatorNode] = []
        self.minter = HikariCurrencyMinter()
        self.chain: list[Block] = []
        self._phase_events: list[dict[str, Any]] = []
        self._last_network_gamma = 0.0

    # -- core simulation -------------------------------------------------

    def run_cycle(self, n_nodes: int = 50, n_blocks: int = 100) -> dict[str, Any]:
        """Run a full PoR simulation: build the network, then propose and
        validate ``n_blocks`` blocks against it."""
        self.nodes = build_network(n_nodes, self.byzantine_fraction, self._rng)
        self.chain = []
        self._phase_events = []

        previous_hash = GENESIS_HASH
        accepted_count = 0
        for i in range(n_blocks):
            states = run_crep_cycle(self.nodes, self._rng)
            network_gamma = statistics.fmean(s.gamma for s in states) if states else 0.0
            self._last_network_gamma = network_gamma

            result = run_consensus_round(self.nodes, {"seq": i}, self._rng)
            block = Block(
                index=i,
                payload={"seq": i},
                previous_hash=previous_hash,
                network_gamma=network_gamma,
                accepted=result.accepted,
                weighted_agreement=result.weighted_agreement,
            )
            self.chain.append(block)

            if result.accepted:
                accepted_count += 1
                previous_hash = block.hash
                for node_id in result.agreeing_nodes:
                    self.mint_hikari(node_id)
            else:
                self._phase_events.append(
                    {
                        "type": "consensus_failure",
                        "block_index": i,
                        "weighted_agreement": result.weighted_agreement,
                        "threshold": CONSENSUS_THRESHOLD,
                    }
                )

        return {
            "n_nodes": n_nodes,
            "n_blocks": n_blocks,
            "accepted_blocks": accepted_count,
            "rejected_blocks": n_blocks - accepted_count,
            "acceptance_rate": accepted_count / n_blocks if n_blocks else 0.0,
            "network_gamma_mean": self._last_network_gamma,
        }

    # -- Diamond Interface -------------------------------------------------

    def get_crep_state(self) -> dict[str, Any]:
        gammas = [node.gamma for node in self.nodes]
        states = [node.crep_state for node in self._states() if node.crep_state is not None]
        if not states:
            return {"C": 0.0, "R": 0.0, "E": 0.0, "P": 0.0, "Gamma": 0.0,
                     "Gamma_target": GAMMA_POR, "crep_gini_coefficient": 0.0}
        return {
            "C": statistics.fmean(s.coherence for s in states),
            "R": statistics.fmean(s.resonance for s in states),
            "E": statistics.fmean(s.emergence for s in states),
            "P": statistics.fmean(s.poetics for s in states),
            "Gamma": statistics.fmean(gammas) if gammas else 0.0,
            "Gamma_target": GAMMA_POR,
            "crep_gini_coefficient": gini_coefficient(gammas),
        }

    def get_utac_state(self) -> dict[str, Any]:
        accepted = [b for b in self.chain if b.accepted]
        h = len(accepted) / len(self.chain) if self.chain else 0.0
        return {
            "H": h,
            "H_star": CONSENSUS_THRESHOLD,
            "K": 1.0,
            "K_eff": eta_from_gamma(self._last_network_gamma, SIGMA),
            "dH_dt": self._consensus_strength_drift(),
        }

    def get_phase_events(self) -> list[dict[str, Any]]:
        return list(self._phase_events)

    def to_zenodo_record(self) -> dict[str, Any]:
        utac = self.get_utac_state()
        crep = self.get_crep_state()
        return {
            "package_id": "P29",
            "name": "hikari-ledger",
            "domain": "distributed-systems",
            "scale": "network",
            "version": "1.0.0",
            "crep_state": crep,
            "utac_state": utac,
            "phase_events": self.get_phase_events(),
            "n_blocks": len(self.chain),
            "n_nodes": len(self.nodes),
            "byzantine_fraction": self.byzantine_fraction,
            "reference": "Gemini-2026-GenesisAeon-Assessment",
        }

    # -- domain-specific API -------------------------------------------------

    def validate_block(
        self, block_data: dict[str, Any], node_crep_states: list[dict[str, Any]]
    ) -> bool:
        """Validate ``block_data`` against externally supplied node CREP
        states (rather than the internally simulated network)."""
        total_gamma = sum(max(s.get("Gamma", 0.0), 0.0) for s in node_crep_states)
        if total_gamma <= 0:
            return False
        weighted_agreement = sum(
            max(s.get("Gamma", 0.0), 0.0) / total_gamma
            for s in node_crep_states
            if s.get("agrees", True)
        )
        return bool(weighted_agreement > CONSENSUS_THRESHOLD)

    def mint_hikari(self, validator_id: str) -> float:
        node = next((n for n in self.nodes if n.node_id == validator_id), None)
        gamma = node.gamma if node is not None else 0.0
        return self.minter.mint(validator_id, gamma)

    def network_crep_mean(self) -> float:
        return self._last_network_gamma

    def byzantine_tolerance_pct(self) -> float:
        return max_tolerable_byzantine_fraction() * 100.0

    # -- internals -------------------------------------------------

    def _states(self) -> list[ValidatorNode]:
        return [n for n in self.nodes if n.crep_state is not None]

    def _consensus_strength_drift(self) -> float:
        if len(self.chain) < 2:
            return 0.0
        first, last = self.chain[0], self.chain[-1]
        return (last.weighted_agreement - first.weighted_agreement) / len(self.chain)
