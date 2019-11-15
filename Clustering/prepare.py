import pandas as pd
from sklearn.preprocessing import LabelEncoder

def prep_iris_data(df_iris):
    df = df_iris.copy()
    
    df = df.drop(columns=["species_id", "measurement_id"])
    
    df = df.rename(index=str, columns={"species_name": "species"})
    
    encoder = LabelEncoder()
    encoder.fit(df.species)
    df = df.assign(species_encode=encoder.transform(df.species))
    
    return df


def prep_titanic_data(df_titanic):
    df = df_titanic.copy()
    
    df.embarked = df.embarked.fillna("U")
    df.embark_town = df.embark_town.fillna("Unknown")
    
    df = df.drop(columns="deck")
    
    encoder = LabelEncoder()
    encoder.fit(df.embarked)
    df = df.assign(embarked_encode=encoder.transform(df.embarked))
    
    df = df.dropna()
    
    return df

def prep_iris_data(df_iris):
    df = df_iris.copy()
    
    df = df.drop(columns=["species_id", "measurement_id"])
    
    df = df.rename(index=str, columns={"species_name": "species"})
    
    encoder = LabelEncoder()
    encoder.fit(df.species)
    df = df.assign(species_encode=encoder.transform(df.species))
    
    return df

def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def data_prep(df, cols_to_remove=[], prop_required_column=.5, prop_required_row=.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df