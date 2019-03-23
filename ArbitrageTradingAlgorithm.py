import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import fix_yahoo_finance as yf
from sklearn.model_selection import train_test_split


# In[1]:


# check cointegration status


def get_z_score(currencyPair):
    x = sm.add_constant(currencyPair[0])
    y = currencyPair[1]
    model = sm.OLS(y, x).fit()
    resid = model.resid
    isStationarity = check_for_stationarity(resid)
    if not isStationarity:
        return

    fitted = currencyPair[0]

    signals['fitted'] = np.mat(sm.add_constant(signals['asset2'])) * \
                        np.mat(model.params).reshape(2, 1)

    signals['residual'] = signals['asset1'] - signals['fitted']

    signals['z'] = (signals['residual'] - np.mean(signals['residual'])) / \
                   np.std(signals['residual'])

    # use z*0 to get panda series instead of an integer result
    signals['z upper limit'] = signals['z'] * 0 + np.mean(signals['z']) + np.std(signals['z'])
    signals['z lower limit'] = signals['z'] * 0 + np.mean(signals['z']) - np.std(signals['z'])

    return signals

def cointegration2(data1, data2):
    # train test split
    df1, test1, df2, test2 = train_test_split(data1, data2, test_size=0.7
                                              , shuffle=False)

    train = pd.DataFrame()
    train['asset1'] = df1['Close']
    train['asset2'] = df2['Close']

    # this is the part where we test the cointegration
    # in this case, i use Engle-Granger two-step method
    # which is invented by the mentor of my mentor!!!
    # generally people use Johanssen test to check the cointegration status
    # the first step for EG is to run a linear regression on both variables
    # next, we do OLS and obtain the residual
    # after that we run unit root test to check the existence of cointegration
    # if it is stationary, we can determine its a drunk man with a dog
    # the first step would be adding a constant vector to asset1

    x = sm.add_constant(train['asset1'])
    y = train['asset2']
    model = sm.OLS(y, x).fit()
    resid = model.resid

    print(model.summary())
    print('\n', sm.tsa.stattools.adfuller(resid))

    # this phrase is how we set the trigger conditions
    # first we normalize the residual
    # we would get a vector that follows standard normal distribution
    # generally speaking, most tests use one sigma level as the threshold
    # two sigma level reaches 95% which is relatively difficult to trigger
    # after normalization, we should obtain a white noise follows N(0,1)
    # we set +-1 as the threshold
    # eventually we visualize the result

    signals = pd.DataFrame()
    signals['asset1'] = test1['Close']
    signals['asset2'] = test2['Close']

    signals['fitted'] = np.mat(sm.add_constant(signals['asset2'])) * \
                        np.mat(model.params).reshape(2, 1)

    signals['residual'] = signals['asset1'] - signals['fitted']

    signals['z'] = (signals['residual'] - np.mean(signals['residual'])) / \
                   np.std(signals['residual'])

    # use z*0 to get panda series instead of an integer result
    signals['z upper limit'] = signals['z'] * 0 + np.mean(signals['z']) + np.std(signals['z'])
    signals['z lower limit'] = signals['z'] * 0 + np.mean(signals['z']) - np.std(signals['z'])

    return signals

def cointegration(data1, data2):
    # train test split
    df1, test1, df2, test2 = train_test_split(data1, data2, test_size=0.7
                                              , shuffle=False)

    train = pd.DataFrame()
    train['asset1'] = df1['Close']
    train['asset2'] = df2['Close']

    # this is the part where we test the cointegration
    # in this case, i use Engle-Granger two-step method
    # which is invented by the mentor of my mentor!!!
    # generally people use Johanssen test to check the cointegration status
    # the first step for EG is to run a linear regression on both variables
    # next, we do OLS and obtain the residual
    # after that we run unit root test to check the existence of cointegration
    # if it is stationary, we can determine its a drunk man with a dog
    # the first step would be adding a constant vector to asset1

    x = sm.add_constant(train['asset1'])
    y = train['asset2']
    model = sm.OLS(y, x).fit()
    resid = model.resid

    print(model.summary())
    print('\n', sm.tsa.stattools.adfuller(resid))

    # this phrase is how we set the trigger conditions
    # first we normalize the residual
    # we would get a vector that follows standard normal distribution
    # generally speaking, most tests use one sigma level as the threshold
    # two sigma level reaches 95% which is relatively difficult to trigger
    # after normalization, we should obtain a white noise follows N(0,1)
    # we set +-1 as the threshold
    # eventually we visualize the result

    signals = pd.DataFrame()
    signals['asset1'] = test1['Close']
    signals['asset2'] = test2['Close']

    signals['fitted'] = np.mat(sm.add_constant(signals['asset2'])) * \
                        np.mat(model.params).reshape(2, 1)

    signals['residual'] = signals['asset1'] - signals['fitted']

    signals['z'] = (signals['residual'] - np.mean(signals['residual'])) / \
                   np.std(signals['residual'])

    # use z*0 to get panda series instead of an integer result
    signals['z upper limit'] = signals['z'] * 0 + np.mean(signals['z']) + np.std(signals['z'])
    signals['z lower limit'] = signals['z'] * 0 + np.mean(signals['z']) - np.std(signals['z'])

    return signals



# In[2]:


# the signal generation process is very straight forward
# if the normalized residual gets above or below threshold
# we long the bearish one and short the bullish one, vice versa
# i only need to generate trading signal of one asset
# the other one should be the opposite direction
def signal_generation(df1, df2, method):
    signals = method(df1, df2)

    signals['signals1'] = 0

    # as z statistics cannot exceed both upper and lower bounds at the same time
    # this line holds
    signals['signals1'] = np.select([signals['z'] > signals['z upper limit'], \
                                     signals['z'] < signals['z lower limit']], \
                                    [1, -1], default=0)

    # signals only imply holding
    # we take the first order difference to obtain the execution signal
    signals['positions1'] = signals['signals1'].diff()
    signals['signals2'] = -signals['signals1']
    signals['positions2'] = signals['signals2'].diff()

    return signals


# In[3]:


# visualization
def plot(new, ticker1, ticker2):
    # z stats figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(211)

    new['z'].plot(label='z statistics', c='#e8175d')
    ax.fill_between(new.index, new['z upper limit'], \
                    new['z lower limit'], label='+- 1 sigma', \
                    alpha=0.5, color='#f7db4f')

    plt.legend(loc='best')
    plt.title('Cointegration Normalized Residual')
    plt.xlabel('Date')
    plt.ylabel('value')
    plt.grid(True)
    plt.show()

    # positions

    fig = plt.figure(figsize=(10, 10))
    bx = fig.add_subplot(212, sharex=ax)

    new['asset1'].plot(label='{}'.format(ticker1))
    new['asset2'].plot(label='{}'.format(ticker2))

    bx.plot(new.loc[new['positions1'] == 1].index, \
            new['asset1'][new['positions1'] == 1], \
            lw=0, marker='^', markersize=8, \
            label='LONG {}'.format(ticker1), c='g', alpha=0.7)
    bx.plot(new.loc[new['positions1'] == -1].index, \
            new['asset1'][new['positions1'] == -1], \
            lw=0, marker='v', markersize=8, \
            label='SHORT {}'.format(ticker1), c='r', alpha=0.7)
    bx.plot(new.loc[new['positions2'] == 1].index, \
            new['asset2'][new['positions2'] == 1], \
            lw=0, marker=2, markersize=12, \
            label='LONG {}'.format(ticker2), c='g', alpha=0.9)
    bx.plot(new.loc[new['positions2'] == -1].index, \
            new['asset2'][new['positions2'] == -1], \
            lw=0, marker=3, markersize=12, \
            label='SHORT {}'.format(ticker2), c='r', alpha=0.9)

    bx.legend(loc='best')
    plt.title('Pair Trading')
    plt.xlabel('Date')
    plt.ylabel('price')
    plt.grid(True)
    plt.show()


# In[4]:


def main():
    # the sample i am using are NVDA and AMD from 2012 to 2015
    stdate = '2013-01-01'
    eddate = '2014-12-31'
    ticker1 = 'NVDA'
    ticker2 = 'AMD'

    #проверить тип данных, получаемых с внешних ресурсов
    df1 = yf.download(ticker1, start=stdate, end=eddate)

    print(df1)

    df2 = yf.download(ticker2, start=stdate, end=eddate)

    signals = signal_generation(df1, df2, cointegration)

    plot(signals, ticker1, ticker2)

main()



def root(currencyPair):
    resultStationari1 = check_for_stationarity(currencyPair[0])
    resultStationari2 = check_for_stationarity(currencyPair[1])
    if resultStationari1 or resultStationari2:
        return False

    cointegration(currencyPair[0], currencyPair[1])
