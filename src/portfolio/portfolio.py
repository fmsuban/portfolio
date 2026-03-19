from typing import Dict
from .stock import Stock
from .rebalance import calculate_rebalance
from .exceptions import AllocationError


class Portfolio:
    """
    Represents a portfolio with positions and target allocation.
    """

    def __init__(
        self,
        positions: Dict[str, Stock],
        target_allocation: Dict[str, float],
    ):
        self.positions = positions
        self.target_allocation = target_allocation

        self._validate_allocation()

    def _validate_allocation(self):
        total = sum(self.target_allocation.values())

        if round(total, 5) != 1.0:
            raise AllocationError(
                f"Allocation must sum to 1.0, got {total}"
            )

    def total_value(self) -> float:
        return sum(stock.get_value() for stock in self.positions.values())

    def rebalance(self):
        """
        Delegates rebalance logic to dedicated module.
        """
        return calculate_rebalance(self.positions, self.target_allocation)
