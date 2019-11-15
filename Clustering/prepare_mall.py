# Create a file named perpare_mall.py that contains functions that do the following:
# 
# - detects any outliers
# - encodes all the categorical columns, and adds the encoded column (i.e. it doesn't remove the original column)
# - accepts the unprepared mall customers data frame and applies all the transformations above
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from acquire_mall import get_mall_customer_data 
from summarize import df_summary


def get_outliers(s, k):
    '''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.

    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    lower_bound = q3 - k * iqr
    upper = s.apply(lambda x: max([x - upper_bound, 0]))
    lower = s.apply(lambda x: min([x + lower_bound, 0]))
    return (upper,lower)


def add_outlier_columns(df, k):
    '''
    Add a column with the suffix _outliers for all the numeric columns
    in the given dataframe.
    '''
   # make a copy of the df to avoid possible side-affects
    df = df.copy()
    
    for col in df.select_dtypes('number'):
        upper, lower = get_outliers(df[col], k)
        df[col + '_upper_outliers'] = upper
        df[col + '_lower_outliers'] = lower

    return df


# Summarize
# 1. Write or use a previous function you have written that summarizes the data you have just read into a dataframe in the ways we have discussed in previous modules (sample view, datatypes, value counts, summary stats, ...)
# 2. Use this function from a notebook to get an overview of your data.
# 3. Use this function to help when you are working with the zillow data as well.


def prep_mall_data(mall_df):
    mall_df = mall_df.copy()
    mall_df.set_index('customer_id', inplace=True)
    print(mall_df.dtypes)
    print(mall_df.head(3).append(mall_df.tail(3)))
    # Add the columns for the outliers
    mall_df = add_outlier_columns(mall_df, k=1.5)
    mall_df.head(3).append(mall_df.tail(3))
    # create two columns for male and female respectively
    dummy = pd.get_dummies(mall_df['gender'])
    df = pd.concat((mall_df, dummy), axis=1)
    df.head(3)
    df_summary(df)
    return df