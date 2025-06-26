# %% [markdown]
# # Pairs Trading Strategy
# Project using yfinance, statsmodels, and matplotlib to implement a mean-reversion-based pairs trading strategy.
# We will try a set of 3 pairs to understand and study the stocks well.

# %%
# 📦 Import libraries
import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# %%
# Download stock data
start = '2017-06-01'
end = '2020-06-01'

grp1_stock1 = "HDFCBANK.NS"
grp1_stock2 = "ICICIBANK.NS"

grp2_stock1 = "INFY.NS"
grp2_stock2 = "TCS.NS"

grp3_stock1 = "BRITANNIA.NS"
grp3_stock2 = "NESTLEIND.NS"

g1stock1 = yf.Ticker(grp1_stock1)
g1stock2 = yf.Ticker(grp2_stock2)
g2stock1 = yf.Ticker(grp2_stock1)
g2stock2 = yf.Ticker(grp2_stock2)
g3stock1 = yf.Ticker(grp3_stock1)
g3stock2 = yf.Ticker(grp3_stock2)

g1stock1_data = g1stock1.history(interval='1d', start=start, end=end)
g1stock2_data = g1stock2.history(interval='1d', start=start, end=end)
g2stock1_data = g2stock1.history(interval='1d', start=start, end=end)
g2stock2_data = g2stock2.history(interval='1d', start=start, end=end)
g3stock1_data = g3stock1.history(interval='1d', start=start, end=end)
g3stock2_data = g3stock2.history(interval='1d', start=start, end=end)

# %%
# Extract and combine closing prices

g1stock1_close = g1stock1_data['Close']
g1stock2_close = g1stock2_data['Close']
g2stock1_close = g2stock1_data['Close']
g2stock2_close = g2stock2_data['Close']
g3stock1_close = g3stock1_data['Close']
g3stock2_close = g3stock2_data['Close']

# %%
# Plot the closing prices of the stocks
plt.figure(figsize=(14, 6))
stock1_close_relative = g1stock1_close / g1stock1_close[0]
stock2_close_relative = g1stock2_close / g1stock2_close[0]
plt.plot(stock1_close_relative , label = grp1_stock1 )
plt.plot(stock2_close_relative , label = grp1_stock2 )
plt.xlabel("Time")
plt.ylabel("Rel Close Price")
plt.legend()
plt.show()

plt.figure(figsize=(14, 6))
stock1_close_relative = g2stock1_close / g2stock1_close[0]
stock2_close_relative = g2stock2_close / g2stock2_close[0]
plt.plot(stock1_close_relative , label = grp2_stock1 )
plt.plot(stock2_close_relative , label = grp2_stock2 )
plt.xlabel("Time")
plt.ylabel("Rel Close Price")
plt.legend()
plt.show()

plt.figure(figsize=(14, 6))
stock1_close_relative = g3stock1_close / g3stock1_close[0]
stock2_close_relative = g3stock2_close / g3stock2_close[0]
plt.plot(stock1_close_relative , label = grp3_stock1 )
plt.plot(stock2_close_relative , label = grp3_stock2 )
plt.xlabel("Time")
plt.ylabel("Rel Close Price")
plt.legend()
plt.show()
