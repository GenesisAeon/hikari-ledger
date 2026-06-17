"""Hikari token minting from CREP resonance contribution."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HikariCurrencyMinter:
    """Mints Hikari tokens proportional to a validator's CREP resonance.

    Token emission rate: delta_H_i = k * Gamma_i * (1 - S_H)
    where S_H is the current Hikari supply entropy (saturating term that
    prevents unbounded oversaturation as total supply grows).
    """

    emission_rate_k: float = 1.0
    supply_cap: float = 1_000_000.0
    balances: dict[str, float] = field(default_factory=dict)

    @property
    def total_supply(self) -> float:
        return sum(self.balances.values())

    def supply_entropy(self) -> float:
        """S_H -- normalised fraction of the supply cap already minted."""
        return min(1.0, self.total_supply / self.supply_cap) if self.supply_cap > 0 else 0.0

    def mint(self, validator_id: str, gamma: float) -> float:
        delta = self.emission_rate_k * max(gamma, 0.0) * (1.0 - self.supply_entropy())
        self.balances[validator_id] = self.balances.get(validator_id, 0.0) + delta
        return delta

    def balance_of(self, validator_id: str) -> float:
        return self.balances.get(validator_id, 0.0)
