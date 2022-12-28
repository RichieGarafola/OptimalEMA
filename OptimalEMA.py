# Import libraries

# streamlit library is used to create the web app interface
import streamlit as st
# pandas library is used for data manipulation and analysis
import pandas as pd
# datetime library is used for working with dates and times
import datetime as dt
# plotly library is used for creating interactive plots
import plotly.graph_objs as go
# make_subplots function from plotly is used to create subplots
from plotly.subplots import make_subplots
# yfinance library is used to retrieve stock data from Yahoo Finance
import yfinance as yf
# numpy library is used for numerical calculations
import numpy as np
 # matplotlib library is used for creating static plots
import matplotlib.pyplot as plt
 # ttest_ind function from scipy is used to perform a t-test for independent samples
from scipy.stats import ttest_ind
from PIL import Image



# initiate 'name' variable to hold the ticker of the users choice
# Ask the user to enter the ticker of their choice and store it in the 'name' variable
# Convert the user's input to uppercase
name = (st.text_input("Enter ticker of your choice", "AAPL")).upper()

# check if the ticker is valid by trying to retrieve data using the Yfinance API
# Try to retrieve data using the Yfinance API
try:
    data = yf.download(name)
# If an invalid ticker is entered, show an error message and exit the program    
except ValueError:
    st.write("Invalid ticker entered. Please try again.")
    exit()
# If any other error occurs, show the error message and exit the program
except Exception as e:
    st.write(f"Error occurred: {e}")
    exit()

# allow the user to specify the number of periods forward to look
# Ask the user to enter the number of periods forward to look and store it in the 'n_forward' variable
# Set the minimum value to 1, the maximum value to 30, and the default value to 2
n_forward = st.number_input("Enter the number of periods forward to look", min_value=1, max_value=30, value=2)

# create a 'forward close' column
# Shift the 'Close' column by the number of periods specified by the user and store the result in the 'Forward Close' column
data['Forward Close'] = data['Close'].shift(-n_forward)

# create a forward return column subtracting the forward close from the current close divided by the current close
# Calculate the forward return by subtracting the 'Forward Close' column from the 'Close' column and dividing by the 'Close' column
# Store the result in the 'Forward Return' column
data['Forward Return'] = (data['Forward Close'] - data['Close'])/data['Close']

# create a 'buy and hold return' column using the same forward return calculation as above
# Copy the values from the 'Forward Return' column and store them in the 'Buy and Hold Return' column
data['Buy and Hold Return'] = data['Forward Return']

# Initiate an open bucket to hold the results to be used later
result = []

# allow the user to specify the training sample size
# Ask the user to specify the training sample size as a percentage and store it in the 'train_size' variable
# Set the minimum value to 0.1, the maximum value to 0.9, and the default value to 0.8
train_size = st.slider("Enter the training sample size (as a percentage)", min_value=0.1, max_value=0.9, value=0.8)

# create a for loop that iterates through a range of 3-500 to find the optimal EMA for the desired pair
for ema_length in range(3,500):
    # Set the EMA column to use the optimal ema length
    data['EMA'] = data['Close'].ewm(span=ema_length).mean()
    # create the input column and append if the current close is greater than the EMA
    data['input'] = [int(x) for x in data['Close'] > data['EMA']]
    # Drop null values
    df = data.dropna()
    # train the data using the specified percentage of the data set
    training = df.head(int(train_size * df.shape[0]))
    # test the remaining dataset
    test = df.tail(int((1 - train_size) * df.shape[0]))
    # Filter the training returns if the input is equal to 1
    training_returns = training[training['input'] == 1]['Forward Return']
    # Filter the test returns if the input is equal to 1
    test_returns = test[test['input'] == 1]['Forward Return']
    # find the average forward training returns
    mean_forward_return_training = training_returns.mean()
    # find the average forward test returns
    mean_forward_return_test = test_returns.mean()
    # use the ttest_ind function from the scipy model to calulate
    pvalue = ttest_ind(training_returns,test_returns,equal_var=False)[1]
    # append the results to a dictionary
    result.append({
      'ema_length':ema_length,
      'training_forward_return': mean_forward_return_training,
      'test_forward_return': mean_forward_return_test,
      'p-value':pvalue
    })
    
# find the optimal ema value    
result.sort(key = lambda x : -x['training_forward_return'])
# result[0]

best_ema = result[0]['ema_length']
data['EMA'] = data['Close'].ewm(span=best_ema).mean()

# calculate the overall return for the EMA strategy
overall_return_ema = (data['Forward Return'] * data['input']).sum()

# calculate the overall return for the buy and hold strategy
overall_return_buy_and_hold = data['Buy and Hold Return'].sum()

# create a dataframe to hold the results
results_df = pd.DataFrame(result)

# plot the training and test forward returns for each EMA length
(results_df[['ema_length', 'training_forward_return', 'test_forward_return']]).plot()

# allow the user to specify a start and end date for the analysis
start_date = st.date_input("Enter the start date for the analysis")
end_date = st.date_input("Enter the end date for the analysis")

# filter the data to only include the specified date range
filtered_data = data[(data.index.date >= start_date) & (data.index.date <= end_date)]

#########
# add the overall returns to the result dataframe
result[0]['overall_return_ema'] = overall_return_ema
result[0]['overall_return_buy_and_hold'] = overall_return_buy_and_hold

# display the overall returns for the EMA and buy and hold strategies
st.write(f"Overall return for EMA strategy: {overall_return_ema:.2f}")
st.write(f"Overall return for buy and hold strategy: {overall_return_buy_and_hold:.2f}")

# plot the returns for both strategies
plot_returns = data[['Forward Return', 'Buy and Hold Return']]
# st.line_chart(data[['Forward Return', 'Buy and Hold Return']])
st.line_chart(plot_returns)

### Add optimal EMA to OHLC 

optimal_EMA = data.reset_index()

# create a candlestick chart visualizing the optimal EMA
optimal_EMA_plot = go.Figure(data=[go.Candlestick(
    x=optimal_EMA.index,
    open = optimal_EMA['Open'],
    high = optimal_EMA['High'],
    low = optimal_EMA['Low'],
    close = optimal_EMA['Close']
)])

st.write(f"{best_ema} periods EMA")
st.write(result[0])
# st.line_chart(data['Close'])
# st.line_chart(plot)
st.plotly_chart(optimal_EMA_plot)
