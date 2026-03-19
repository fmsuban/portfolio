class Stock:
    """
    Represents a stock position in the portfolio.
    """

    def __init__(self, symbol: str, shares: float, price: float):
        self.symbol = symbol
        self.shares = shares
        self.price = price

    def get_value(self) -> float:
        return self.shares * self.price

    def __repr__(self):
        return f"{self.symbol}: {self.shares} shares @ {self.price}"
