import pytest

from portfolio.stock import Stock
from portfolio.portfolio import Portfolio
from portfolio.exceptions import AllocationError


def test_rebalance_basic():
    positions = {
        "META": Stock("META", 10, 100),  # 1000
        "AAPL": Stock("AAPL", 10, 100),  # 1000
    }

    allocation = {
        "META": 0.5,
        "AAPL": 0.5,
    }

    portfolio = Portfolio(positions, allocation)

    result = portfolio.rebalance()

    assert result["BUY"] == {}
    assert result["SELL"] == {}


def test_rebalance_missing_symbol_raises_error():
    # Total value = 1000 (only META exists in positions)
    positions = {
        "META": Stock("META", 10, 100),  # 1000
    }
    allocation = {
        "META": 0.2,  # target 200 -> SELL 800
        "AAPL": 0.8,  # target 800 -> BUY 800
    }

    with pytest.raises(AllocationError):
        Portfolio(positions, allocation).rebalance()


def test_rebalance_mixed_buy_and_sell_multiple_assets():
    # Total value = 3000
    positions = {
        "META": Stock("META", 10, 100),  # 1000
        "AAPL": Stock("AAPL", 10, 200),  # 2000
    }
    allocation = {
        "META": 0.4,  # target 1200 -> BUY 200
        "AAPL": 0.6,  # target 1800 -> SELL 200
    }

    portfolio = Portfolio(positions, allocation)
    result = portfolio.rebalance()

    assert result["BUY"] == {"META": 200}
    assert result["SELL"] == {"AAPL": 200}


def test_rebalance_allocation_must_sum_to_one():
    positions = {
        "META": Stock("META", 10, 100),
        "AAPL": Stock("AAPL", 10, 100),
    }

    allocation = {
        "META": 0.6,
        "AAPL": 0.6,  # sums to 1.2
    }

    with pytest.raises(AllocationError):
        Portfolio(positions, allocation)


def test_rebalance_ignores_position_symbols_not_in_target():
    # TSLA exists in positions, but target_allocation doesn't mention it.
    # The current logic still uses TSLA in total_value, so it affects targets.
    positions = {
        "META": Stock("META", 10, 10),  # 100
        "AAPL": Stock("AAPL", 10, 10),  # 100
        "TSLA": Stock("TSLA", 10, 10),  # 100 (no target entry -> no BUY/SELL action expected)
    }
    allocation = {
        "META": 0.5,  # target 150 -> BUY 50
        "AAPL": 0.5,  # target 150 -> BUY 50
    }

    portfolio = Portfolio(positions, allocation)
    result = portfolio.rebalance()

    assert result["BUY"] == {"META": 50, "AAPL": 50}
    assert result["SELL"] == {}


def test_rebalance_supports_fractional_shares():
    # Total value = 1500
    positions = {
        "META": Stock("META", 1.5, 100),  # 150
        "AAPL": Stock("AAPL", 6.0, 225),  # 1350
    }
    allocation = {
        "META": 0.2,  # target 300 -> BUY 150
        "AAPL": 0.8,  # target 1200 -> SELL 150
    }

    portfolio = Portfolio(positions, allocation)
    result = portfolio.rebalance()

    assert result["BUY"] == {"META": 150}
    assert result["SELL"] == {"AAPL": 150}


def test_rebalance_allocation_rounding_allows_sum_to_one():
    positions = {
        "META": Stock("META", 1, 100),
        "AAPL": Stock("AAPL", 1, 200),
        "TSLA": Stock("TSLA", 1, 700),
    }

    # 0.1 + 0.2 + 0.7 puede no ser exacto en binario,
    # pero la validación usa round(..., 5).
    allocation = {
        "META": 0.1,
        "AAPL": 0.2,
        "TSLA": 0.7,
    }

    portfolio = Portfolio(positions, allocation)
    result = portfolio.rebalance()

    # Ya están en el objetivo => no debería haber acciones.
    assert result["BUY"] == {}
    assert result["SELL"] == {}
