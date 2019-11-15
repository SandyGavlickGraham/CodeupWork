# Time Series Data Aquisition Exercises
import os
import pandas as pd
import numpy as np
from datetime import datetime
import itertools

# JSON API
import requests
import json

# data visualization
import matplotlib
import seaborn as sns
import statsmodels.api as sm

get_ipython().run_line_magic('matplotlib', 'inline')

# ignore warnings
import warnings
warnings.filterwarnings("ignore")


# Data Dictionary:
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

def get_data(category):
    
    if os.path.exists(category + '.csv'):
        print('Reading ', category, ' from local csv')
        return pd.read_csv(category + '.csv')
    
    base_url = 'https://python.zach.lol'
    # this is the http request, the get function from requests
    response = requests.get(base_url + '/api/v1/' + category)
    data = response.json()
    page_df = pd.DataFrame(data['payload'][category])

    print('Downloading data for ', category, '...')
    max = data['payload']['max_page'] - 1
    print('max page = ', max+1)
    count = 1
    print(count, ' ', end='')    
    
    for page in range(max):
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        page_df = pd.concat([page_df, pd.DataFrame(data['payload'][category])]).reset_index()
        page_df.drop(columns='index', inplace=True)
        count += 1
        print(count, ' ', end='')
        
    print()

    return page_df


def acquire_data():
    items = get_data('items')
    stores = get_data('stores')
    sales = get_data('sales')
    print('items: ', items.shape)
    items.to_csv('items.csv', index=False)
    print('stores: ', stores.shape)
    stores.to_csv('stores.csv', index=False)
    print('sales: ', sales.shape)
    sales.to_csv('sales.csv', index=False)
    
    sales.rename(columns={'store': 'store_id', 'item': 'item_id'}, inplace=True)
    df = pd.merge(sales, items, on='item_id')
    df = pd.merge(df, stores, on='store_id')
    
    df.drop(df.index[1:-1])
    return df

if __name__ == '__main__':

    df = acquire_data()
    print(df.drop(df.index[1:-1]))
