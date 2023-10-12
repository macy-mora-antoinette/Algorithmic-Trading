# Algorithmic-Trading

## Introduction
This report implements two trading strategies and compares their performance. One strategy manually determine trades while the other technique uses machine learning in the form of a Random Forest classifier to determine trades. Both use the same market indicators: bollinger bands, golden crossings, and moving average convergence-divergence (MACD). The goal is to determine how a machine learning strategy may outperform the manual strategy with the ability to adapt to changes in the market. For the purposes of this report, we select an in-sample time period (1/1/2008-12/31/2009) to train on and an out-of-sample time period (1/1/2010-12/31/2011) to test on. The starting portfolio value is $100,000. The number of total long or short sells allowed at any given time must be within 1000 to -1000. Commission is $9.95 and impact is 0.05% unless otherwise stated. I hypothesize that the Random Forest classifier will improve the performance of the indicators’ predictions to optimize the portfolio return. I also hypothesize that as transaction fees increase, whether it be in the form of commission or impact, there will be a disruption in the overall performance of both trading strategies.

## 2 INDICATOR OVERVIEW
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



Figure 1

![figure1](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/e3194f6b-112d-4d9d-8e9d-1b97f8e93bdb)


Figure 2

![figure2](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/31fdaa30-4ac0-4f4b-82c5-e8581bbae5c0)


Table 1

![table1](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/c2668d66-2b99-46bb-91e7-557a7b8be960)


Figure 3

![figure3](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/a37a63fa-6f62-4f0e-8348-63276cd0e2c6)


Figure 4

![figure4](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/eed0b9dd-c939-49ef-aeb8-7763d95bee3d)

Figure 5

![figure5](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/e3f7b576-fc56-422f-b6e5-7e0d6ad1c794)


Figure 6

![figure6](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/e9c71d2d-ec19-4acc-9d37-f28d7e130002)


Table 2

![table2](https://github.com/macy-mora-antoinette/Algorithmic-Trading/assets/112992304/3cb6577b-629a-4aff-b631-4b516b98f8ac)
