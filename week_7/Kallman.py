# Import a Kalman filter and other libraries
pip install pykalman
pip install qq-training-wheels auquan_toolbox --upgrade
from pykalman import KalmanFilter
import numpy as np
import pandas as pd
from scipy import poly1d
from datetime import datetime

import matplotlib.pyplot as plt
matplotlib inline
plt.style.use('seaborn-darkgrid')
plt.rcParams['figure.figsize'] = (10,7)

# Define path where data file is saved in your system
#path = '../data/'
data = pd.read_csv(path +'data.csv', index_col ='Date')
data['ratio'] = data['BAJAJ']/ data['HERO']
stock_1 = data['BAJAJ']
stock_2 = data['HERO']

# Calculate the hedge ratio for pairs trading
ratio =stock_1/stock_2
data.head()

kf = KalmanFilter(transition_matrices = [1],
              observation_matrices = [1],
              initial_state_mean = 0,
              initial_state_covariance = 1,
              observation_covariance=1,
              transition_covariance=.0001)

mean, cov = kf.filter(ratio.values)
mean, std = mean.squeeze(), np.std(cov.squeeze())

plt.figure(figsize=(15,7))
plt.plot(ratio.values - mean, 'm', lw=1)
plt.plot(np.sqrt(cov.squeeze()), 'y', lw=1)
plt.plot(-np.sqrt(cov.squeeze()), 'c', lw=1)
plt.title('Kalman filter estimate')
plt.legend(['Error: real_value - mean', 'std', '-std'])
plt.xlabel('Day')
plt.ylabel('Value')

# Use the observed values of the price to get a rolling mean and z_score
mean, cov =  kf.filter(ratio.values)
data['mean'] = mean.squeeze()
data['cov'] = cov.squeeze()
data['std'] = np.sqrt(data['cov'])
data = data.dropna()

data['ma'] = data['ratio'].rolling(5).mean()
data['z_score'] = (data['ma'] - data['mean'])/data['std']

# Initialise positions as zero
data['position_1'] = np.nan
data['position_2'] = np.nan

# Generate buy, sell and square off signals as: z<-1 buy, z>1 sell and -1<z<1 liquidate the position
for i in range (data.shape[0]):
  if data['z_score'].iloc[i] < -1:
    data['position_1'].iloc[i] = 1
    data['position_2'].iloc[i] = -round(data['ratio'].iloc[i],0)
  if data['z_score'].iloc[i] > 1:
    data['position_1'].iloc[i] = -1
    data['position_2'].iloc[i] = round(data['ratio'].iloc[i],0)
  if (abs(data['z_score'].iloc[i]) < 1) & (abs(data['z_score'].iloc[i]) > 0):
    data['position_1'].iloc[i] = 0
    data['position_2'].iloc[i] = 0
    
# Calculate returns
data['returns'] = ((data['BAJAJ']-data['BAJAJ'].shift(1))/data['BAJAJ'].shift(1))*data['position_1'].shift(1)+ ((data['HERO']-data['HERO'].shift(1))/data['HERO'].shift(1))*data['position_2'].shift(1)
data['returns'].sum()