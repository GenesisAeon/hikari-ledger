"""Proof-of-Resonance validator node."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass, field

from hikari_ledger.crep_validator import CREPState


def _new_signing_key() -> bytes:
    return secrets.token_bytes(32)


@dataclass
class ValidatorNode:
    """A single PoR validator.

    Each node holds a symmetric signing key (HMAC-SHA256 stand-in for a real
    public-key signature scheme -- sufficient for simulating the validation
    protocol without pulling in an external crypto dependency) and the CREP
    state produced by its most recent UTAC cycle.
    """

    node_id: str
    _signing_key: bytes = field(default_factory=_new_signing_key, repr=False)
    crep_state: CREPState | None = None
    byzantine: bool = False

    def sign(self, payload: bytes) -> str:
        return hmac.new(self._signing_key, payload, hashlib.sha256).hexdigest()

    def verify(self, payload: bytes, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)

    def update_crep_state(self, state: CREPState) -> None:
        self.crep_state = state

    @property
    def gamma(self) -> float:
        return self.crep_state.gamma if self.crep_state is not None else 0.0
