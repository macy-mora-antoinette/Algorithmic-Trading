# Algorithmic-Trading

# 1. Introduction
This report implements two trading strategies and compares their performance. One strategy manually determine trades while the other technique uses machine learning in the form of a Random Forest classifier to determine trades. Both use the same market indicators: bollinger bands, golden crossings, and moving average convergence-divergence (MACD). The goal is to determine how a machine learning strategy may outperform the manual strategy with the ability to adapt to changes in the market. For the purposes of this report, we select an in-sample time period (1/1/2008-12/31/2009) to train on and an out-of-sample time period (1/1/2010-12/31/2011) to test on. The starting portfolio value is $100,000. The number of total long or short sells allowed at any given time must be within 1000 to -1000. Commission is $9.95 and impact is 0.05% unless otherwise stated. I hypothesize that the Random Forest classifier will improve the performance of the indicators’ predictions to optimize the portfolio return. I also hypothesize that as transaction fees increase, whether it be in the form of commission or impact, there will be a disruption in the overall performance of both trading strategies.

# 2 INDICATOR OVERVIEW
## 2.1 Bollinger Bands
Bollinger Bands are used to indicate a buy and sell signal when using the simple moving average (SMA). The equations are shown below.
〖SMA〗_t=(〖Price〗_t+〖Price〗_(t-1)+...+〖Price〗_(t-n))/n                                          (1)
〖Bollinger Band〗_(+,-)= 〖(SMA〗_t- Current Price)/ 2σ_t                                               (2)
The bollinger bands values indicates that two standard deviations above and below the SMA would be a long or short signal. When the stock price is two standard deviations or more away from the SMA, this can indicate either a buy (if above the SMA) or a sell (if below the SMA). In this report, the number of lookback days was optimized for the Manual and Strategy Learner by using n = 20 days.

## 2.2 Golden Crossings
Crossings between short term and long term SMAs are also used to indicate buy and sell signals for stocks. A golden crossing is a when a short term SMA is above a long term SMA. Golden crossings indicate a buy signal. The opposite can also hold true, where the short term SMA is below the long term SMA. This is called a death crossing and indicates short selling. The crossings indicate either a recent underperformance or overperformance compared to the long term price history. In this report, the lookback for the short term SMA was optimized to 25 days for the lookback for the long term SMA was optimized to 100 days.

## 2.3 Moving Average Convergence-Divergence (MACD)
The final indicator is the Moving Average Convergence Divergence (MACD). The MACD indicates buy and sell signals by comparing a long term and short term EMA. The exponential moving average (EMA) is another statistic commonly used in a similar manner as SMA. EMA is a type of weighted moving average that gives more weighting or importance to recent price data. When the short term EMA is above the long term EMA, this indicates a buy signal. The opposite can also hold true: when the short term EMA is below the long term EMA, this indicates a sell. This is shown in Equations 3 and 4 below: 
〖EMA〗_t=〖Price〗_t  2/(1 + n)     +    〖EMA〗_(t-1) ( 1 -  2/(1+n)  )         (3)

〖MACD〗_entry=EMA(n1) - EMA(n2)                      (4)
Since the short term and long term EMA values have different time periods, the difference between them essentially indicates a recent under or over performance in the recent stock trends. For this report, we optimized the short term lookback as 12 days and the long term lookback as 26 days.

## Example with Apple Stock (AAPL)

![figure1](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/9e2a3355-9373-4bc7-873a-6538fa7955a3)

Figure 1

![figure2](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/88d28aff-a090-4ba1-9ee0-64665476f1e9)

Figure 2

![table1](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/d919cd6f-2dee-4597-b14a-100c9ec13023)

Table 1

![figure3](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/e817a646-019a-4733-82fa-c8e16414bc24)

Figure 3

![figure4](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/972dc8d3-27bd-4d06-ad9b-453cc5d2a599)

Figure 4

![figure5](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/560cb513-4e96-4cd6-a4c9-71c9e840bf8d)

Figure 5

![figure6](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/3397cf71-2dab-4fba-a733-8ccc88afcd40)

Figure 6

![table2](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/bb23d427-c79c-4bc5-a6db-45378589ecee)

Table 2



