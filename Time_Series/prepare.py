# # Prepare
# prepare.py

# Time Series Data Aquisition Exercises
import pandas as pd
from acquire import acquire_data


# # Data Dictionary:
# 
# - date - Date of the sale data. There are no holiday effects or store closures.
#  
# - store_address, store_id, store_city, store_state, store_zipcode
#  
# - item_brand, item_id, item_name, item_price, item_upc12, item_upc14
#  
# - sales.item: item id in the transaction
#  
# - sale_amount: Number of items sold at a particular store on a particular date.
#  
# - sale_date: Date of the transaction
#  
# - sale_id: ID of the sale of that item of that transaction.
#  
# - sales.store: store where the sale took place
#  
# - /stores[/{store_id}]
#  
# - /items[/{item_id}]
#  
# - /sales[/{sale_id}]


# - Write a function to convert a date to a datetime data type.
# class datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
def parse_sales_date(df):
    df = df.copy()
    df.sale_date = pd.to_datetime(arg=df.sale_date, 
                          dayfirst=True, 
                          utc=True, 
                          box=True, 
                          exact=True,
                          format='%a, %d %b %Y %H:%M:%S %Z',
                          cache=True,
                          errors='raise') 
    df.sale_date = df.sale_date.dt.date
    return df


# - Write a function to change a datetime to UTC. 
#     - done by setting parameter in my to_datetime function

# - Write a function to parse a date column into 6 additional columns (while keeping the original date): year, quarter, month, day of month, day of week, weekend vs. weekday

def add_date_parts(df):
    df = df.copy()
    df['year'] = df.sale_date.dt.year
    df['quarter'] = df.sale_date.dt.quarter
    df['month'] = df.sale_date.dt.month
    df['day'] = df.sale_date.dt.day
    df['hour'] = df.sale_date.dt.hour
    df['dayofweek'] = df.sale_date.dt.dayofweek
    df['weekday'] = df.sale_date.dt.day_name().str[:3]
    # df['weekday'] = df.sale_date.dt.day_name().str[:3]
    df['is_weekend'] = ((pd.DatetimeIndex(df.sale_date).dayofweek) // 5 == 1)
    return df.set_index('sale_date')


# - Add a column to your dataframe, sales_total, which is a derived from sale_amount (total items) and item_price.
def improve_sales_data(df):
    df = df.copy()
    df.rename(columns={'sale_amount':'quantity'}, inplace=True)
    df['sale_total'] = df['quantity'] * df['item_price']
    return df

# # - Create a new dataframe that aggregates the sales_total and sale_amount(item count) using sum and median by day of week.
# def aggregate_by_weekday(df):
#     df = df.copy()
#     by_dayofweek = pd.DataFrame()
#     by_dayofweek['quantity_sum'] = df.groupby(['weekday']).quantity.sum()
#     by_dayofweek['item_cnt_sum'] = df.groupby(['weekday']).sale_total.sum()
#     by_dayofweek['quantity_median'] = df.groupby(['weekday']).quantity.median()
#     by_dayofweek['item_cnt_median'] = df.groupby(['weekday']).sale_total.median()
#     return by_dayofweek



# - Explore the pandas DataFrame.diff() function. Create a new column that is the result of the current sales - the previous days sales.
def add_sales_difference(df):
    df = df.copy()
    df['diff_from_last_day'] = df.sale_total.diff()
    return df


# - Write a function to set the index to be the datetime variable.
#     - done in the return of parse_date
# def prep_store_data(df):
#     df = df.copy()
#     df = parse_sales_date(df)
#     df = add_date_parts(df)
#     df = improve_sales_data(df)
#     df = add_sales_difference(df)
#     return(df)

def prep_store_data(df):
    df = df.copy()
    df = parse_sales_date(df)
    df = improve_sales_data(df)
    return df

if __name__ == '__main__':
    df = acquire_data()
    df = prep_store_data(df)
    df.head(3)