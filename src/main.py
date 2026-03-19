from portfolio.stock import Stock
from portfolio.portfolio import Portfolio


def main():
    positions = {
        "META": Stock("META", shares=10, price=300),
        "AAPL": Stock("AAPL", shares=20, price=150),
    }

    target_allocation = {
        "META": 0.4,
        "AAPL": 0.6,
    }

    portfolio = Portfolio(positions, target_allocation)

    print("Total value:", portfolio.total_value())
    print("Rebalance actions:", portfolio.rebalance())


if __name__ == "__main__":
    main()
