"""Tests for the HikariLedger Diamond Interface."""

from hikari_ledger.system import HikariLedger


def test_run_cycle_returns_summary():
    ledger = HikariLedger(seed=1)
    result = ledger.run_cycle(n_nodes=20, n_blocks=10)
    assert result["n_blocks"] == 10
    assert 0.0 <= result["acceptance_rate"] <= 1.0


def test_diamond_interface_methods():
    ledger = HikariLedger(seed=2)
    ledger.run_cycle(n_nodes=20, n_blocks=10)

    crep_state = ledger.get_crep_state()
    assert set(crep_state) >= {"C", "R", "E", "P", "Gamma"}

    utac_state = ledger.get_utac_state()
    assert set(utac_state) >= {"H", "H_star", "K"}
    assert utac_state["H_star"] == 2 / 3

    assert isinstance(ledger.get_phase_events(), list)

    record = ledger.to_zenodo_record()
    assert record["package_id"] == "P29"
    assert record["name"] == "hikari-ledger"


def test_byzantine_network_produces_consensus_failures():
    ledger = HikariLedger(byzantine_fraction=0.6, seed=3)
    ledger.run_cycle(n_nodes=30, n_blocks=10)
    assert len(ledger.get_phase_events()) > 0


def test_mint_hikari_increases_balance():
    ledger = HikariLedger(seed=4)
    ledger.run_cycle(n_nodes=10, n_blocks=5)
    node_id = ledger.nodes[0].node_id
    balance_before = ledger.minter.balance_of(node_id)
    ledger.mint_hikari(node_id)
    assert ledger.minter.balance_of(node_id) >= balance_before
