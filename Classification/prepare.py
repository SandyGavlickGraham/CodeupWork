import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

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
    
#     # the scaling should be done after the train/test split
#     scaler = MinMaxScaler()
#     df[["age", "fare"]] = scaler.fit_transform(df[["age", "fare"]])
    
#     train, test = train_test_split(df, train_size=0.7, random_state=123, stratify=df[["survived"]])
    
    return df




# import acquire 
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder

# def drop_species_meas(iris_df):
#     iris_df = iris_df.drop(columns=['measurement_id', 'species_id'])
#     return iris_df

# def rename_col(iris_df):
#     iris_df = iris_df.rename(columns={"species_name": "species"})
#     return iris_df

# def encode_species(iris_df):
#     encoder = LabelEncoder()
#     encoder.fit(iris_df.species)
#     iris_df['species_encode'] = encoder.transform(iris_df.species)
#     return (iris_df)

# def prep_iris(iris_df):
#     return iris_df.pipe(drop_species_meas)\
#     .pipe(rename_col)\
#     .pipe(encode_species)





# def fix_embark(titanic_df):
#     titanic_df.embark_town.fillna('Other', inplace=True)
#     titanic_df.embarked.fillna('O', inplace=True)
#     return(titanic_df)

# def drop_deck(titanic_df):
#     titanic_df.drop(columns='deck')
#     return(titanic_df)

# def prep_embarked (titanic_df):
#     encoder = LabelEncoder()
#     encoder.fit(titanic_df.embarked)
#     titanic_df['embarked_encode'] = encoder.transform(titanic_df.embarked)
#     return (titanic_df)


# def prep_titanic (titanic_df):
#     fix_embark(titanic_df)
#     drop_deck(titanic_df)
#     prep_embarked(titanic_df)
#     return(titanic_df)