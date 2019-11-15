# data manipulation 
import numpy as np
import pandas as pd

from datetime import datetime
import itertools as it

from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AR

from sklearn.model_selection import TimeSeriesSplit
from sklearn import metrics

import math
import statsmodels.api as sm

# data visualization 
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

from acquire_saas import get_saas_data
from prepare_saas import prep_saas_data


def plot_data_and_predictions(predictions, label):
    plt.figure(figsize=(10, 8))

    plt.plot(train,label='Train')
    plt.plot(test, label='Test')
    plt.plot(predictions, label=label, linewidth=5)

    plt.legend(loc='best')
    plt.show()


def evaluate(actual, predictions, output=True):
    mse = metrics.mean_squared_error(actual, predictions)
    rmse = math.sqrt(mse)

    if output:
        print('MSE:  {}'.format(mse))
        print('RMSE: {}'.format(rmse))
    else:
        return mse, rmse    


def plot_and_eval(predictions, actual, train, metric_fmt='{:.2f}', linewidth=4):
    test = actual
    if type(predictions) is not list:
        predictions = [predictions]

    plt.figure(figsize=(16, 8))
    plt.plot(train,label='Train')
    plt.plot(test, label='Test')

    for yhat in predictions:
        mse, rmse = evaluate(actual, yhat, output=False)        
        label = f'{yhat.name}'
        if len(predictions) > 1:
            label = f'{label} -- MSE: {metric_fmt} RMSE: {metric_fmt}'\
                    .format(mse, rmse)
        plt.plot(yhat, label=label, linewidth=linewidth)

    if len(predictions) == 1:
        label = f'{label} -- MSE: {metric_fmt} RMSE: {metric_fmt}'.format(mse, rmse)
        plt.title(label)

    plt.legend(loc='best')
    plt.show()  
    
    
def model_saas_data(df):
    
    df=df.copy()
    
    # Using saas.csv or log data from api usage of last week
    # 1. Split data (train/test) and resample by any period except daily, and aggregate using the sum.
    # 2. Forecast, plot and evaluate using each of the 4 parametric based methods we discussed:
    #     - simple average
    #     - moving average
    #     - Holt's linear trend model
    #     - Based on previous year/month/etc (your choice)


    aggregation = 'sum'


    # # Sampling

    train = df[:'2016'].Amount.resample('M').agg(aggregation)
    test = df['2017':].Amount.resample('M').agg(aggregation)


    print('Observations: %d' % (len(train.values) + len(test.values)))
    print('Training Observations: %d' % (len(train)))
    print('Testing Observations: %d' % (len(test)))

    # #### 1. Simple Average
    print('Simple Average')
    yhat = pd.DataFrame(dict(actual=test))

    yhat['avg_forecast'] = train.sum()

    print(yhat.head())

    plot_and_eval(yhat.avg_forecast, test, train)


    # #### 2. Moving Average
    print('Moving Average')

    periods = 30
    yhat['moving_avg_forecast_30'] = train.rolling(30).sum().iloc[-1]

    plot_and_eval(yhat.moving_avg_forecast_30, test, train)

    periods = 30
    yhat['moving_avg_forecast_30'] = train.rolling(30).mean().iloc[-1]

    plot_and_eval(yhat.moving_avg_forecast_30, test, train)

    # period_vals = [1, 4, 12, 26]

    # for periods in period_vals:
    #     yhat[f'moving_avg_forecast_{periods}'] = train.rolling(periods).sum().iloc[-1]

    # forecasts = [yhat[f'moving_avg_forecast_{p}'] for p in period_vals]

    # plot_and_eval(forecasts, linewidth=2,test, train)


    # #### 3. Holts Linear Trend Model
    print('Holts Linear Trend Model')
    
    sm.tsa.seasonal_decompose(train).plot()
    result = sm.tsa.stattools.adfuller(train)
    plt.show()

    train = df[:'2016'].Amount.resample('M').agg(aggregation)
    test = df['2017':].Amount.resample('M').agg(aggregation)

    sm.tsa.seasonal_decompose(train).plot()
    result = sm.tsa.stattools.adfuller(train)
    plt.show()


    from statsmodels.tsa.api import Holt

    holt = Holt(train).fit(smoothing_level=.9, smoothing_slope=.6497)

    yhat['holt_linear'] = holt.forecast(test.shape[0])

    plot_and_eval(yhat.holt_linear, test, train)


    # #### 4. Predicting Based on the Last Year's Data
    print('Predicting Based on the Last Year''s Data')
    # note that 2016 was a leap year
    using_last_year = train['2016'].reset_index()\
                    .drop(columns='Month_Invoiced')\
                    .set_index(train['2016'].index + 12)

    yhat['last_year'] = using_last_year

    print(yhat)

    plot_and_eval(yhat.last_year, test, train, linewidth=1)

    predictions = train['2016'] + train.diff(12).mean()
    predictions.index = pd.date_range('20170101', periods=12, freq='M')
    predictions.name = 'Last Year + Mean'

    plot_and_eval(predictions, test, train, linewidth=1)

    
  
    
    

def aquire_prep_model_saas_data():
    print('aquire data')
    df = get_saas_data()
    print('prep data')
    df = prep_saas_data(df)
    print(df.head())
    print('model data')
    model_saas_data(df)