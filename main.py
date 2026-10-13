
from pathlib import Path

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Project settings
TICKERS = ["VOO", "QQQ", "AGG", "IWM"]
START_DATE = "2019-01-01"
END_DATE = "2026-01-01"


RISK_FREE_RATE = 0.0


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def download_prices():
    """Download adjusted historical closing prices for selected ETFs."""
    prices = yf.download(
        TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False
    )["Close"]

    if prices.empty:
        raise ValueError(
            "No price data downloaded. Check your internet connection."
        )

    prices = prices.sort_index()
    prices = prices.dropna()

    return prices

def validate_prices(prices):
        """Check the quality of historical price data."""

        expected_tickers = {"VOO", "QQQ", "AGG", "IWM"}

        # Check expected columns
        if set(prices.columns) != expected_tickers:
            raise ValueError("Unexpected or missing ETF columns.")

        # Check date index
        if prices.index.has_duplicates:
            raise ValueError("Duplicate trading dates found.")

        if not prices.index.is_monotonic_increasing:
            raise ValueError("Dates are not in chronological order.")

        # Check missing and invalid prices
        if prices.isna().any().any():
            raise ValueError("Missing prices detected.")

        if (prices <= 0).any().any():
            raise ValueError("Non-positive prices detected.")

        print("\nData validation passed.")
        print(f"Start date: {prices.index.min().date()}")
        print(f"End date:   {prices.index.max().date()}")
        print(f"Trading observations: {len(prices)}")
        print(f"ETFs validated: {len(prices.columns)}")


def calculate_metrics(returns):
        """Calculate historical return and risk metrics for one ETF."""

        # Reconstruct investment growth from daily returns
        wealth = (1 + returns).cumprod()
        wealth = pd.concat([
            pd.Series([1.0], index=[returns.index[0] - pd.Timedelta(days=1)]),
            wealth
        ])

        # Approximate number of years represented by the data
        years = len(returns) / 252

        # Compound annual growth rate
        total_growth = wealth.iloc[-1]
        annualized_return = total_growth ** (1 / years) - 1

        # Annualized standard deviation of daily returns
        annualized_volatility = returns.std() * np.sqrt(252)
        
        sharpe_ratio = (
            (annualized_return - RISK_FREE_RATE) / annualized_volatility
            if annualized_volatility != 0
            else np.nan
        )

        # Largest decline from a previous wealth peak
        running_peak = wealth.cummax()
        drawdowns = wealth / running_peak - 1
        max_drawdown = drawdowns.min()

        return {
            "Sharpe Ratio": sharpe_ratio,
            "Annualized Return": annualized_return,
            "Annualized Volatility": annualized_volatility,
            "Maximum Drawdown": max_drawdown
        }


def calculate_portfolio_returns(returns):
    """Calculate daily returns for different ETF portfolios."""

    portfolios = {
        "Conservative": {
            "VOO": 0.20,
            "QQQ": 0.10,
            "IWM": 0.10,
            "AGG": 0.60
        },
        "Balanced": {
            "VOO": 0.35,
            "QQQ": 0.15,
            "IWM": 0.10,
            "AGG": 0.40
        },
        "Growth": {
            "VOO": 0.45,
            "QQQ": 0.30,
            "IWM": 0.15,
            "AGG": 0.10
        }
    }

    portfolio_returns = {}

    for name, weights in portfolios.items():
        weight_series = pd.Series(weights)
        portfolio_returns[name] = returns[list(weights)].mul(
            weight_series
        ).sum(axis=1)

    return pd.DataFrame(portfolio_returns)


def plot_portfolio_allocations():
    """Visualize ETF weights across the three portfolio strategies."""

    allocations = pd.DataFrame({
        "Conservative": {
            "VOO": 20,
            "QQQ": 10,
            "IWM": 10,
            "AGG": 60
        },
        "Balanced": {
            "VOO": 35,
            "QQQ": 15,
            "IWM": 10,
            "AGG": 40
        },
        "Growth": {
            "VOO": 45,
            "QQQ": 30,
            "IWM": 15,
            "AGG": 10
        }
    })

    ax = allocations.T.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 6)
    )

    ax.set_title("ETF Allocation by Portfolio Strategy")
    ax.set_xlabel("Portfolio Strategy")
    ax.set_ylabel("Allocation (%)")
    ax.set_ylim(0, 100)
    ax.legend(title="ETF")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "portfolio_allocations.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    plt.close()

    print("Saved portfolio allocation chart to outputs/portfolio_allocations.png")

def main():
    prices = download_prices()
    validate_prices(prices)

    # Calculate daily percentage returns
    returns = prices.pct_change(fill_method=None).dropna()

    
    # Calculate daily returns for each portfolio
    portfolio_returns = calculate_portfolio_returns(returns)

    print("\nPORTFOLIO DAILY RETURNS (%):")
    print((portfolio_returns.head() * 100).round(3))

    
    
    # Track the growth of a hypothetical investment
    initial_investment = float(
        input("Enter your initial investment amount ($): ")
    )

    if initial_investment <= 0:
        raise ValueError("Investment amount must be greater than zero.")

    
    portfolio_values = (
        (1 + portfolio_returns).cumprod() * initial_investment
    )

    # Add the initial investment before the first daily return.
    start_date = portfolio_returns.index[0] - pd.Timedelta(days=1)

    
    initial_values = pd.DataFrame(
        [[initial_investment] * len(portfolio_returns.columns)],
        columns=portfolio_returns.columns,
        index=[start_date]
    )


    portfolio_values = pd.concat([initial_values, portfolio_values])

    
    print("\nPORTFOLIO ENDING VALUES ($):")
    print(portfolio_values.iloc[-1].round(2).to_string())

    plt.figure(figsize=(12, 6))

    for portfolio in portfolio_values.columns:
        plt.plot(
            portfolio_values.index,
            portfolio_values[portfolio],
            label=portfolio
        )

    
    plt.title(
        f"Growth of a Hypothetical ${initial_investment:,.0f} Investment"
    )

    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "portfolio_growth.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

    print("Saved portfolio growth chart to outputs/portfolio_growth.png")

    plot_portfolio_allocations()

    # Calculate risk and return metrics for each portfolio
    portfolio_metrics = pd.DataFrame({
        name: calculate_metrics(portfolio_returns[name])
        for name in portfolio_returns.columns
    }).T

    
    print("\nPORTFOLIO RISK AND RETURN COMPARISON:")

    portfolio_display = portfolio_metrics.copy()

    percentage_columns = [
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown"
    ]

    portfolio_display[percentage_columns] *= 100

    print(portfolio_display.round(2).to_string())


    
    # Save portfolio performance metrics
    portfolio_metrics.to_csv(
        DATA_DIR / "portfolio_metrics.csv"
    )

    print("Saved portfolio metrics to data/portfolio_metrics.csv")


    # Calculate risk and return metrics for every ETF
    metrics = pd.DataFrame({
        ticker: calculate_metrics(returns[ticker])
        for ticker in returns.columns
    }).T

    print("\nETF RISK AND RETURN COMPARISON")
    
    metrics_display = metrics.copy()

    percentage_columns = [
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown"
    ]

    metrics_display[percentage_columns] *= 100

    print(metrics_display.round(2))


    # Save individual ETF performance metrics
    metrics.to_csv(
        DATA_DIR / "etf_metrics.csv"
    )

    print("Saved ETF metrics to data/etf_metrics.csv")

    # Analyze relationships between ETF daily returns
    correlation = returns.corr()

    print("\nETF RETURN CORRELATION MATRIX:")
    print(correlation.round(2).to_string())

    # Save the results for later analysis
    correlation.to_csv(DATA_DIR / "return_correlation.csv")
    print("\nSaved correlation matrix to data/return_correlation.csv")

    
    # Visualize ETF return correlations
    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        fmt=".2f"
    )

    plt.title("ETF Daily Return Correlations (2019–2025)")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "etf_correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

    print("Saved correlation heatmap to outputs/etf_correlation_heatmap.png")



    print("\nFirst five daily returns (%):")
    print((returns.head() * 100).round(3))

    print("\nAverage daily return (%):")
    print((returns.mean() * 100).round(4))

    print("\nFirst five rows:")
    print(prices.head())

    print("\nDataset shape:")
    print(prices.shape)

    print("\nMissing values:")
    print(prices.isna().sum())

    prices.to_csv(DATA_DIR / "adjusted_prices.csv")
    print("\nSaved historical prices to data/adjusted_prices.csv")


if __name__ == "__main__":
    main()
