"""Command-line interface for hikari-ledger."""

from __future__ import annotations

import json

import typer

from hikari_ledger import __version__
from hikari_ledger.benchmark import energy_comparison, latency_comparison
from hikari_ledger.system import HikariLedger

app = typer.Typer(help="Proof-of-Resonance distributed consensus simulator.")


@app.command()
def run(
    nodes: int = typer.Option(50, "--nodes", help="Number of validator nodes."),
    blocks: int = typer.Option(100, "--blocks", help="Number of blocks to simulate."),
    seed: int = typer.Option(42, "--seed", help="Random seed for reproducibility."),
) -> None:
    """Run a Proof-of-Resonance consensus simulation."""
    ledger = HikariLedger(seed=seed)
    result = ledger.run_cycle(n_nodes=nodes, n_blocks=blocks)
    typer.echo(json.dumps(result, indent=2))


@app.command(name="simulate-attack")
def simulate_attack(
    nodes: int = typer.Option(50, "--nodes"),
    blocks: int = typer.Option(100, "--blocks"),
    byzantine_fraction: float = typer.Option(0.30, "--byzantine-fraction"),
    seed: int = typer.Option(42, "--seed"),
) -> None:
    """Simulate consensus under a given fraction of Byzantine validators."""
    ledger = HikariLedger(byzantine_fraction=byzantine_fraction, seed=seed)
    result = ledger.run_cycle(n_nodes=nodes, n_blocks=blocks)
    result["byzantine_fraction"] = byzantine_fraction
    result["byzantine_tolerance_pct"] = ledger.byzantine_tolerance_pct()
    typer.echo(json.dumps(result, indent=2))


@app.command(name="energy-comparison")
def energy_comparison_cmd(
    vs_pow: bool = typer.Option(True, "--vs-pow/--no-vs-pow"),
    vs_pos: bool = typer.Option(True, "--vs-pos/--no-vs-pos"),
) -> None:
    """Compare PoR energy use against PoW / PoS / BFT latency."""
    result = energy_comparison() | latency_comparison()
    if not vs_pow:
        result.pop("proof_of_work_kwh_per_block", None)
        result.pop("por_vs_pow_efficiency_factor", None)
    if not vs_pos:
        result.pop("proof_of_stake_kwh_per_block", None)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def version() -> None:
    """Show the installed hikari-ledger version."""
    typer.echo(__version__)


if __name__ == "__main__":
    app()
