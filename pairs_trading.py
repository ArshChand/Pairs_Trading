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

# %%
# Examine p values

from statsmodels.tsa.stattools import coint, adfuller

coint_result_g1 = coint(g1stock1_close, g1stock2_close)
print(coint_result_g1[1])

coint_result_g2 = coint(g2stock1_close, g2stock2_close)
print(coint_result_g2[1])

coint_result_g3 = coint(g3stock1_close, g3stock2_close)
print(coint_result_g3[1])

# Based on the above results we reject group 1 and 3 and proceed only with group 2

# %% 
# Perform Linear Regression

# Log-transform the close prices
log_stock1 = np.log(g2stock1_close)
log_stock2 = np.log(g2stock2_close)

# Linear regression: log(stock2) ~ log(stock1)
X = sm.add_constant(log_stock1)
Y = log_stock2

model = sm.OLS(Y, X)
results = model.fit()

# Extract regression parameters
intercept, beta = results.params
print(f"Intercept: {intercept:.4f}, Beta (Hedge Ratio): {beta:.4f}")

# Calculate spread (residuals)
predicted_Y = results.predict(X)
residuals = Y - predicted_Y

plt.figure(figsize=(14, 5))
plt.plot(residuals, color='navy', label='Residuals')
plt.axhline(residuals.mean(), color='black', linestyle='--', label='Mean')
plt.title(f'Spread (Residuals) from log-price regression\nSpread = log({grp2_stock2}) - {beta:.2f} × log({grp2_stock1})')
plt.xlabel("Date")
plt.ylabel("Spread (Residuals)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# %%
# Z-score of spread residuals

zscore = (residuals - residuals.mean()) / residuals.std()

plt.figure(figsize=(14, 5))
plt.plot(zscore, color='purple', label='Z-score of Spread')
plt.axhline(1, color='red', linestyle='--', label='+1 Threshold')
plt.axhline(-1, color='green', linestyle='--', label='-1 Threshold')
plt.axhline(0, color='black', linestyle='--')
plt.title("Z-score of Residuals")
plt.xlabel("Date")
plt.ylabel("Z-score")
plt.grid(True)
plt.legend()
plt.tight_layout() 
plt.show()