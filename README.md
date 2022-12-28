# Optimal EMA

An exponential moving average (EMA) is a type of moving average (MA) that places a greater weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted moving average. An exponentially weighted moving average reacts significantly to recent price changes.

Like all moving averages, this technical indicator is used to produce buy and sell signals based on crossovers and divergences from the historical average.

Traders often use several different EMA lengths, such as 10-day, 50-day, and 200-day moving averages.

### What Does the EMA Tell You?

The 12- and 26-day exponential moving averages (EMAs) are often the most quoted and analyzed short-term averages. The 12- and 26-day are used to create indicators like the moving average convergence divergence (MACD) and the percentage price oscillato (PPO). In general, the 50- and 200-day EMAs are used as indicators for long-term trends. When a stock price crosses its 200-day moving average, it is a technical signal that a reversal has occurred.

Traders who employ technical analysis find moving averages very useful and insightful when applied correctly. However, they also realize that these signals can create havoc when used improperly or misinterpreted. All the moving averages commonly used in technical analysis are lagging indicators.

Consequently, the conclusions drawn from applying a moving average to a particular market chart should be to confirm a market move or to indicate its strength. The optimal time to enter the market often passes before a moving average shows that the trend has changed.

An EMA does serve to alleviate the negative impact of lags to some extent. Because the EMA calculation places more weight on the latest data, it "hugs" the price action a bit more tightly and reacts more quickly. This is desirable when an EMA is used to derive a trading entry signal.

Like all moving average indicators, EMAs are much better suited for trending markets. When the market is in a strong and sustained uptrend, the EMA indicator line will also show an uptrend and vice-versa for a downtrend. A vigilant trader will pay attention to both the direction of the EMA line and the relation of the rate of change from one bar to the next.

---

Key Takeaways:

- Get stock price data

- Split dataset to train and test for the ttest model 

- Find the Optimal EMA

- Plot the Optimal EMA

---

Libraries used:

- streamlit

- pandas

- datetime 

- plotly

- yfinance

- numpy

- matplotlib

- scipy

---

## Step 1: Get the data

Using the yahoo finance API get the data of the users choice

set the number of periods forward to be used when shifting

create features for the dataset using a 2 period shift on the close price

create a forward return feature by subtracting the forward close from the current close divided by the current close

---

## Step 2: Split the dataset

Train 80% of the dataset and test the remaining 20%

## Step 3: Find the Optimal EMA

Create a for loop that iterates through a range of 3-500 to find the optimal EMA for the desired pair chosen by the user


## Step 4: Plot the Optimal EMA

Create a candlestick chart using the Optimal EMA to visualize how it fits with the dataset


!['Optimal EMA']()