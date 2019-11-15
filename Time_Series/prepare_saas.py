import pandas as pd
from acquire_saas import get_saas_data


def parse_sales_date(df):
    
    df = df.copy()
    df['Month_Invoiced'] =  pd.to_datetime(df['Month_Invoiced'])
    df = df.set_index('Month_Invoiced')
    return df


def prep_saas_data(df):
    df = df.copy()
    df = parse_sales_date(df)
    return(df)


if __name__ == '__main__':
    df = get_saas_data()
    df = prep_store_data(df)
    df.head(3)


# In[ ]:




