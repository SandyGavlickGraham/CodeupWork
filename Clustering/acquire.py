import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers', get_connection('titanic_db'))

def get_iris_data():
    return pd.read_sql('SELECT s.species_name, m.* FROM species AS s JOIN measurements AS m ON  s.species_id = m.species_id', get_connection('iris_db'))

def get_mall_customer_data():
    return pd.read_sql('SELECT * FROM customers', get_connection('mall_customers'))

titanic_df = get_titanic_data()
iris_df = get_iris_data()
mall_df = get_mall_customer_data()