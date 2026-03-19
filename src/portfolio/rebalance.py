from typing import Dict
from .stock import Stock
from .exceptions import AllocationError


def calculate_rebalance(
    positions: Dict[str, Stock],
    target_allocation: Dict[str, float],
) -> Dict[str, Dict[str, float]]:
    """
    Core rebalance logic extracted for better testability.

    Returns:
        {
            "BUY": {symbol: amount_in_dollars},
            "SELL": {symbol: amount_in_dollars}
        }
    """

    total_value = sum(stock.get_value() for stock in positions.values())

    actions = {"BUY": {}, "SELL": {}}

    for symbol, target_pct in target_allocation.items():
        target_value = total_value * target_pct

        if symbol not in positions:
            raise AllocationError(f"Missing position for symbol '{symbol}'")

        # At this point we know `symbol` exists in `positions`.
        current_value = positions[symbol].get_value()

        difference = target_value - current_value

        if difference > 0:
            actions["BUY"][symbol] = difference
        elif difference < 0:
            actions["SELL"][symbol] = abs(difference)

    return actions
