# import env
# from pydataset import data

# def get_titanic_data(titanic_df):
# # returns the titanic data from the codeup data science 
# # database as a pandas data frame.
#     path = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/titanic_db'
#     titanic_df = pd.read_sql('SELECT * FROM passengers', path)
#     return (titanic_df)


# def get_iris_data(iris_df):
# # returns the data from the iris_db on the codeup data 
# # science database as a pandas data frame. 
# # The returned data frame should include the actual name of 
# # the species in addition to the species_ids.
#     path = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/iris_db'
#     iris_df = pd.read_sql('SELECT * FROM passengers', path)
#     return(iris_df)

import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers', get_connection('titanic_db'))

def get_iris_data():
    return pd.read_sql('SELECT 	s.species_name, m.* FROM species AS s JOIN measurements AS m ON  s.species_id = m.species_id', get_connection('iris_db'))

titanic_df = get_titanic_data()
iris_df = get_iris_data()

# print(titanic_df.head())
# print(iris_df.head())