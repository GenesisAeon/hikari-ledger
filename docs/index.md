# hikari-ledger

**Proof-of-Resonance distributed consensus** for genesis-os node networks.

CREP-weighted block validation: nodes whose CREP state harmonizes more
strongly with the network earn proportionally more validation weight, with
blocks accepted once weighted agreement crosses the 2/3 Byzantine fault
tolerance threshold.

## Quickstart

```bash
pip install hikari-ledger
```

```bash
hikari-ledger run --nodes 50 --blocks 100
```

## Commands

| Command | Description |
|---------|-------------|
| `hikari-ledger run` | Run a Proof-of-Resonance consensus simulation |
| `hikari-ledger simulate-attack` | Simulate consensus under a Byzantine fraction |
| `hikari-ledger energy-comparison` | Compare PoR energy/latency vs. PoW/PoS/BFT |
| `hikari-ledger version` | Show version |
