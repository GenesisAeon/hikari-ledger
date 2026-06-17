"""Block structure with CREP metadata."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Block:
    """A ledger block, annotated with the network's CREP state at the time
    of proposal so the consensus history doubles as a CREP time series."""

    index: int
    payload: dict[str, Any]
    previous_hash: str
    network_gamma: float
    timestamp: float = field(default_factory=time.time)
    accepted: bool = False
    weighted_agreement: float = 0.0

    @property
    def hash(self) -> str:
        digest_input = json.dumps(
            {
                "index": self.index,
                "payload": self.payload,
                "previous_hash": self.previous_hash,
                "network_gamma": round(self.network_gamma, 8),
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(digest_input).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "network_gamma": self.network_gamma,
            "timestamp": self.timestamp,
            "accepted": self.accepted,
            "weighted_agreement": self.weighted_agreement,
        }


GENESIS_HASH = "0" * 64
