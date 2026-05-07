# FIN 405 — Portfolio Allocation and Asset Pricing: Personal Task List

## Case Study 1 — MPT (Due September 25, 2026)

- Set up Python environment: install yfinance, pandas, scipy, matplotlib — due September 9, 2026
- Download 5 years of daily adjusted close prices for 10 S&P 500 stocks using yfinance
- Choose stocks across at least 3 different sectors for diversification
- Compute daily log returns, annualized mean returns, and covariance matrix
- Code efficient frontier: minimize portfolio variance for each target return level
- Find minimum-variance portfolio (analytical and numerical solution — compare both)
- Find tangency portfolio using Sharpe ratio maximization
- Plot efficient frontier with individual assets, MVP, and tangency portfolio labeled
- Write 2-page analysis: interpret results, discuss diversification benefits — due September 23, 2026
- Submit Jupyter notebook + PDF write-up on Gradescope by 11:59 PM September 25, 2026

## Problem Set 1 — CAPM (Due October 9, 2026)

- Read Bodie et al. Chapters 7–9 on CAPM — due October 2, 2026
- Theoretical problems: derive Security Market Line, Jensen's alpha definition
- Empirical: download Fama-French market factor from WRDS or Kenneth French's website
- Run OLS regression of each stock's excess return on market excess return: estimate beta
- Cross-sectional Fama-MacBeth regression: test whether beta predicts expected returns
- Interpret results: does CAPM hold in your sample? Discuss anomalies found
- Submit PDF on Gradescope by 11:59 PM October 9, 2026

## Midterm Exam Prep (Exam: October 27, 2026)

- Review Case Study 1 feedback and re-derive efficient frontier formulas — due October 20, 2026
- Memorize formulas for formula sheet: Sharpe ratio, Jensen's alpha, Treynor ratio, Information ratio
- Practice SML problems: given beta and risk-free rate, compute expected return
- Review Fama-French factor definitions: HML, SMB, momentum (WML)
- Concept check: what is the equity risk premium? What drives it?
- Practice problems from Bodie Chapters 1–10 review questions
- Attend Prof. Morrison's pre-midterm review session (check portal for date/time)
- One formula sheet allowed (one-sided, 8.5x11) — make it by October 24, 2026

## Portfolio Project — Proposal (Due November 6, 2026)

- Decide on portfolio strategy and asset universe — due October 28, 2026
- Asset universe: minimum 15 securities across 3 sectors (equities + bonds or REITs okay)
- Define investment horizon and rebalancing frequency (monthly or quarterly)
- Identify pricing model to use: CAPM, FF3, FF5, or custom
- Write 1-page proposal: strategy, universe, data sources, risk targets — due November 4, 2026
- Get feedback from TA before submitting if possible (TA office hours Mon 4–5 PM)
- Submit on course portal by 11:59 PM November 6, 2026 — NOT ACCEPTED LATE

## Case Study 2 — Options Pricing (Due November 20, 2026)

- Read Hull Chapters 12–17 on options and Black-Scholes — due November 10, 2026
- Download SPY options chain data (use yfinance or CBOE data)
- Implement Black-Scholes formula for European puts and calls in Python
- Back out implied volatilities using scipy.optimize for each option in the chain
- Plot volatility surface: implied vol vs strike and maturity
- Discuss: smile, skew, and term structure of volatility — what do they imply?
- Compare BSM prices to market prices — where does the model fail?
- Write 3-page report and submit with Jupyter notebook on Gradescope — due November 20, 2026

## Portfolio Project — Final Report (Due December 7, 2026)

- Download and clean data for entire asset universe — due November 13, 2026
- Run factor model regressions (at least FF3) on each asset — due November 20, 2026
- Implement portfolio optimization (mean-variance and Black-Litterman if possible)
- Back-test with rolling 6-month window: rebalance portfolio each period — due November 27, 2026
- Compute: annualized return, Sharpe ratio, maximum drawdown, Calmar ratio, beta
- Risk decomposition: systematic vs idiosyncratic variance for portfolio
- Write 8–10 page report + appendices (charts, regression tables) — draft due December 3, 2026
- Submit final report + Jupyter notebook on course portal by 11:59 PM December 7, 2026

## Final Exam Prep (Exam: December 16, 2026)

- Make two-sided formula sheet — start December 9, 2026
- Review options Greeks: delta, gamma, theta, vega — practice computing from BSM
- Review VaR and CVaR: both parametric and historical simulation methods
- Practice duration and convexity bond problems (Chapters 14–16 Bodie)
- Work through 2 past finals from course portal under timed conditions
- Review all case study feedback and correct mistakes
