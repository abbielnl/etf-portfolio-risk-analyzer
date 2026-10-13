# ETF Portfolio Risk & Return Analyzer

A Python-based financial analysis project that evaluates the historical performance, risk and diversification of four exchange-traded funds (ETFs) and compares three hypothetical portfolio strategies.

## Project Overview

This project analyses historical adjusted prices for four US-listed ETFs:

- **VOO:** Vanguard S&P 500 ETF
- **QQQ:** Invesco QQQ Trust
- **IWM:** iShares Russell 2000 ETF
- **AGG:** iShares Core U.S. Aggregate Bond ETF

The analysis covers January 2019 to December 2025 and explores how combining stock and bond ETFs affects portfolio performance and risk.

## Objectives

- Retrieve and validate historical market data.
- Calculate daily returns and annualized performance metrics.
- Compare annualized return, volatility and maximum drawdown.
- Analyse correlations between ETF daily returns.
- Simulate conservative, balanced and growth-oriented portfolios.
- Visualize correlation and hypothetical portfolio growth.

## Technologies

- Python
- pandas and NumPy
- yfinance
- Matplotlib and Seaborn
- Git and GitHub

## Key Findings

Based on the historical results produced by the analysis:

- QQQ recorded the highest annualized return among the four individual ETFs at 22.59%.
- AGG had the lowest annualized volatility among the individual ETFs at 6.15%.
- The growth-oriented portfolio recorded the highest annualized return among the three tested portfolios at 16.61%.
- The conservative portfolio had the lowest annualized volatility among the three portfolios at 9.84%.
- QQQ and VOO had a daily return correlation of 0.94, while AGG and VOO had a correlation of 0.15.

These results illustrate the historical relationship between risk, return and diversification. They do not predict future performance.

## Portfolio Strategies

| Strategy | VOO | QQQ | IWM | AGG |
|---|---:|---:|---:|---:|
| Conservative | 20% | 10% | 10% | 60% |
| Balanced | 35% | 15% | 10% | 40% |
| Growth | 45% | 30% | 15% | 10% |

## Methodology

1. Download adjusted historical prices using yfinance.
2. Validate the downloaded data for missing values, duplicate dates, chronological order and non-positive prices.
3. Calculate daily percentage returns.
4. Estimate annualized return, annualized volatility and maximum drawdown.
5. Calculate correlations between ETF daily returns.
6. Apply the portfolio weights to daily ETF returns and calculate portfolio performance.
7. Generate charts and export performance metrics to CSV.

Annualized volatility is estimated using the standard deviation of daily returns multiplied by the square root of 252 trading days. Annualized returns are estimated by compounding daily returns over the observed period.

## Outputs

The analysis generates:

- `etf_correlation_heatmap.png` — ETF return correlation heatmap.
- `portfolio_growth.png` — hypothetical portfolio growth chart.
- `etf_metrics.csv` — individual ETF performance metrics.
- `portfolio_metrics.csv` — portfolio performance metrics.
- `return_correlation.csv` — ETF return correlation matrix.

## Limitations

- Historical performance does not guarantee future results.
- The analysis excludes taxes, transaction costs and other trading expenses.
- Portfolio simulations apply the specified target weights to daily returns, representing a simplified daily-rebalanced strategy.
- The analysis uses historical market data and may be affected by data-provider revisions.
- The results are educational and are not investment advice.

## Running the Project

Create and activate a Python environment, then install the dependencies:

```bash
python -m pip install pandas numpy yfinance matplotlib seaborn
```

Run the analysis:

```bash
python main.py
```

A working internet connection is required to download market data.

## Author

Developed as a personal project exploring Python, financial markets, portfolio risk and quantitative analysis.