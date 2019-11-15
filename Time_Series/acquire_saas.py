import pandas as pd
from datetime import datetime


def get_saas_data():
    df = pd.read_csv('./saas.csv')
    return df


if __name__ == '__main__':
    df = get_saas_data()
    print(df.head())
    print(df.dtypes)