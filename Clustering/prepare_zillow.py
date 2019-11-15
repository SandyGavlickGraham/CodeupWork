### Zillow
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from summarize import df_summary
from scipy import stats
from sklearn.linear_model import LinearRegression

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# This function was created by Michael P. Moran.
# However, I am still only getting one county...
def keep_only_single_unit_properties(df: pd.DataFrame) -> pd.DataFrame:
    # unit cnt is 1 or nan and has at least one bathroom and bedroom and
    # square footage above 500

    df = df[(df.unitcnt == 1) | (df.unitcnt.isnull())]
    df = df[
        (df.bathroomcnt > 0)
        & (df.bedroomcnt > 0)
        & (df.calculatedfinishedsquarefeet > 500)
    ]
    df = df[
        (~df.propertylandusedesc.str.contains("Duplex"))
        & (~df.propertylandusedesc.str.contains("Triplex"))
    ]

    return df


# I was still getting only one county, so I'm going to try using exactly the 
# function that Michale wrote.
# The code to handle unitcnt below inspired by Michael P. Moran.
# I had to change mine to reflect Michael's because all but one county had nulls in the
# unitcnt field.
# def keep_only_single_unit_properties(df):
#     '''
#     Include only single unit properties (e.g. no duplexes, no land/lot, ...)
#     For some properties, you will need to use multiple fields to estimate 
#     whether it is a single unit property.

#     KEEP:
#     'Single Family Residential', 'Condominium', 
#     'Mobile Home', 'Manufactured, Modular, Prefabricated Homes',
#     'Residential General', 'Townhouse'

#     DROP
#     'Commercial/Office/Residential Mixed Used','Cluster Home',
#     'Planned Unit Development', 'Quadruplex (4 Units, Any Combination)',
#     'Triplex (3 Units, Any Combination)', 'Cooperative', 
#     'Duplex (2 Units, Any Combination)', 'Store/Office (Mixed Use)'

#     and then drop all but unitcnt == 1
#     '''
    
#     # make a copy of the df to avoid possible side-affects
#     df = df.copy()
    
#     # cannot use this next line because two counties appear to have all nulls in this field.
# #     df = df[df['unitcnt'].isin(['1'])] 
#     df = df[(df.unitcnt == 1) | (df.unitcnt.isnull())]
#     df = df[
#         (df.bathroomcnt > 0)
#         & (df.bedroomcnt > 0)
#         & (df.calculatedfinishedsquarefeet > 500)
#     ]
  
#     # cannot use keep because many fields are null
# #     keep = ('Single Family Residential', 'Condominium', 'Mobile Home', 
# #         'Manufactured, Modular, Prefabricated Homes', 
# #         'Residential General', 'Townhouse')
#     multi = ('Commercial/Office/Residential Mixed Used','Cluster Home',
#              'Planned Unit Development', 'Quadruplex (4 Units, Any Combination)',
#              'Triplex (3 Units, Any Combination)', 'Cooperative', 
#              'Duplex (2 Units, Any Combination)', 'Store/Office (Mixed Use)')

#     # only keep the rows that are not in the multi descriptions list
#     df = df[~df['propertylandusedesc'].isin(multi)]

    
#     return df


# The code below inspired by Codeup curriculum.
def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

# The code below inspired by Codeup curriculum.
def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

# The code below inspired by Codeup curriculum.
def data_prep(df, cols_to_remove=[], prop_required_column=.5, prop_required_row=.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df


# The code below inspired by Michael P. Moran's missing_vals_df().
def missing_values_col(df):
    """
    Write or use a previously written function to return the
    total missing values and the percent missing values by column.
    """
    null_count = df.isnull().sum()
    null_percentage = (null_count / df.shape[0]) * 100
    empty_count = pd.Series(((df == ' ') | (df == '')).sum())
    empty_percentage = (empty_count / df.shape[0]) * 100
    nan_count = pd.Series(((df == 'nan') | (df == 'NaN')).sum())
    nan_percentage = (nan_count / df.shape[0]) * 100
    return pd.DataFrame({'num_missing': null_count, 'missing_percentage': null_percentage,
                         'num_empty': empty_count, 'empty_percentage': empty_percentage,
                         'nan_count': nan_count, 'nan_percentage': nan_percentage})

# The code below by Ednalyn de Dios.
def missing_values_row(df):
    """
    Write or use a previously written function to return the
    total missing values and the percent missing values by row.
    """
    null_count = df.isnull().sum(axis=1)
    null_percentage = (null_count / df.shape[1]) * 100
    return pd.DataFrame({'num_missing': null_count, 'percentage': null_percentage})


# The code below by Ednalyn de Dios.
def amount_of_missing_values_in_columns(df):
    '''
    Write or use a previously written function to return the
    total missing values and the percent missing values by column.
    
    Puts all that info into a dataframe with each original feature
    being a row.
    
    Returns a dataframe that only contains rows that have missing values.
    '''
    df = df.copy()
    null_count = df.isnull().sum()
    null_percentage = (null_count / df.shape[0]) * 100
    empty_count = pd.Series(((df == ' ') | (df == '')).sum())
    empty_percentage = (empty_count / df.shape[0]) * 100
    nan_count = pd.Series(((df == 'nan') | (df == 'NaN')).sum())
    nan_percentage = (nan_count / df.shape[0]) * 100
    total_count = null_count + empty_count + nan_count
    total_percentage = null_percentage + empty_percentage + nan_percentage

    missing_df = pd.DataFrame({'total_missing': total_count, 'total_percentage': total_percentage,
                        'num_missing': null_count, 'missing_percentage': null_percentage,
                        'num_empty': empty_count, 'empty_percentage': empty_percentage,
                        'nan_count': nan_count, 'nan_percentage': nan_percentage})
    
    return missing_df[(missing_df != 0).any(1)]


def fix_bathroom_cnts(df):
    '''
    fix calculatedbathnbr, fullbathcnt
    'bathroomcnt'	 Number of bathrooms in home including fractional bathrooms
    'calculatedbathnbr' (55 missing)	 Number of bathrooms in home including fractional bathroom
    'fullbathcnt'(55 missing)	 Number of full bathrooms (sink, shower + bathtub, and toilet) present in home

    fill both latter fields with the bathroomcnt
    '''
    df = df.copy()
    df['calculatedbathnbr'].fillna(df['bathroomcnt'], inplace=True)
    df['fullbathcnt'].fillna(df['bathroomcnt'], inplace=True)
    return df


# The code below by Ednalyn de Dios.
def fill_with_median(df, *cols):
    """
    Fill the NaN values with respective median values.
    """
    df = df.copy()
    for col in cols:
        df[col] = df[col].fillna(df[col].median())
    return df


# The code below by Ednalyn de Dios.
def fill_with_none(df, *cols):
    """
    Fill the NaN values with 'None' string value.
    """
    df = df.copy()
    for col in cols:
        df[col] = df[col].fillna('None')
    return df


# The code below by Ednalyn de Dios.
def fill_with_zeroes(df, *cols):
    """
    Write a function that will take a dataframe and list of
    column names as input and return the dataframe with the
    null values in those columns replace by 0.
    """
    df = df.copy()
    for col in cols:
        df[col] = df[col].fillna(0)
    return df


# The code below by Ednalyn de Dios.
def impute_missing(df):
    """
    Impute the values in land square feet using linear regression
    with landtaxvaluedollarcnt as x and estimated land square feet as y.
    """
    df = df.copy()
    # imputing landtaxvaluedollarcnt
    df_clean = df.dropna(subset = ['landtaxvaluedollarcnt', 'lotsizesquarefeet'])
    df_dirty = df.loc[pd.isnull(df.lotsizesquarefeet)]

    # Create linear regression objects
    lm1 = LinearRegression(fit_intercept=True)

    lm1.fit(df_clean[['landtaxvaluedollarcnt']], df_clean[['lotsizesquarefeet']])
    print(lm1)

    lm1_y_intercept = lm1.intercept_
    print(lm1_y_intercept)

    lm1_coefficients = lm1.coef_
    print(lm1_coefficients)

    print('Univariate - final_exam = b + m * exam1')
    print('    y-intercept (b): %.2f' % lm1_y_intercept)
    print('    coefficient (m): %.2f' % lm1_coefficients[0])
    print()

    y_pred_lm1 = lm1.predict(df_dirty[['landtaxvaluedollarcnt']])

    df.loc[df.lotsizesquarefeet.isna(), 'lotsizesquarefeet'] = y_pred_lm1
    return df


def convert_number_columns_to_appropriate_datatype(df):
    '''
    Accepts an unprepared zillow dataframe, creates a list of
    columns names for numeric columns, transforms those columns
    into category type or integer type or leaves it as float type, 
    and then returns the dataframe with those changes applied.
    '''
    # make a copy of the df to avoid possible side-affects
    df = df.copy()
    
    # convert categorical DataFrame columns to the category dtype
    cat_cols = ['buildingqualitytypeid', 'fips', 'regionidcity', 
                'regionidcounty','regionidzip',]

    for col in cat_cols:
        df[col] = df[col].astype('category')


    # convert counted DataFrame columns to the int dtype
    int_cols = ['bathroomcnt', 'bedroomcnt', 'rawcensustractandblock',
                'yearbuilt', 'assessmentyear', 'censustractandblock']

    for col in int_cols:
        df[col] = df[col].astype(int)

    '''
    columns that I left as floats:
    calculatedfinishedsquarefeet,
    finishedsquarefeet12, 
    latitude, longitude, lotsizesquarefeet, 
    structuretaxvaluedollarcnt, taxvaluedollarcnt, 
    landtaxvaluedollarcnt, taxamount, logerror
    '''

    return df

def rename_and_order_columns(norm_X, X):
    
    # rename and order columns
    full_X = pd.DataFrame()
    full_X['logerror'] = X.logerror
    full_X['bath'] = norm_X.bathroomcnt
    full_X['bed'] = norm_X.bedroomcnt
    full_X['bedbath'] = full_X.bath + full_X.bed
#     full_X['fullbath'] = norm_X.fullbathcnt
#     full_X['calcbath'] = norm_X.calculatedbathnbr 
#     full_X['roomcnt'] = norm_X.roomcnt 
    full_X['totsqft'] = norm_X.calculatedfinishedsquarefeet 
    full_X['finsqft'] = norm_X.finishedsquarefeet12 
    full_X['year'] = norm_X.yearbuilt
    full_X['land_tax_val'] = norm_X.landtaxvaluedollarcnt
    full_X['struct_tax_val'] = norm_X.structuretaxvaluedollarcnt 
    full_X['land_struct_tax_val'] = full_X['land_tax_val'] + full_X['struct_tax_val']
    full_X['tax_val'] = norm_X.taxvaluedollarcnt 
    full_X['tax'] = norm_X.taxamount
    full_X['zip'] = X.regionidzip
    full_X['regionidcity'] = X.regionidcity
    full_X['regionidcounty'] = X.regionidcounty
    full_X['fips'] = X.fips  
    full_X['latitude'] = X.latitude
    full_X['longitude'] = X.longitude
    full_X['lotsize'] = norm_X.lotsizesquarefeet 
    full_X['bldgqualtype'] = X.buildingqualitytypeid
    full_X['hvac'] = X.heatingorsystemdesc
    full_X['landusecode'] = X.propertycountylandusecode
    full_X['landusedesc'] = X.propertylandusedesc
    full_X['propzone'] = X.propertyzoningdesc
    full_X['rawcensus'] = X.rawcensustractandblock
    full_X['census'] = X.censustractandblock
    full_X['assessmentyr'] = X.assessmentyear
    full_X['transdate'] = X.transactiondate 
    
    return full_X


def standardize_data(X):
    norm_X = X
    norm_cols = ['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 
                 'finishedsquarefeet12', 'yearbuilt', 'landtaxvaluedollarcnt',
                 'taxamount', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt',
                 'lotsizesquarefeet'] 
    
    for col in norm_cols:
        norm_X[col] = (X[col] - X[col].min()) / (X[col].max() - X[col].min())
    
    full_X = rename_and_order_columns(norm_X, X)
    
    return full_X



def drop_standardized_outliers(df):
    
    new_df = df.copy()

    keys = ['bath','bed','totsqft', 'struct_tax_val','land_tax_val', 'lotsize', 'tax']
    # have to match the standardized data
    values = [(
                (1-df.bath.min())/(df.bath.max()-df.bath.min()),
                (7-df.bath.min())/(df.bath.max()-df.bath.min())
              ), 
                  
              (    
                (1-df.bed.min())/(df.bed.max()-df.bed.min()),
                (7-df.bed.min())/(df.bed.max()-df.bed.min())
              ),
              
              (
                (500-df.totsqft.min())/(df.totsqft.max()-df.totsqft.min()),
                (8000-df.totsqft.min())/(df.totsqft.max()-df.totsqft.min())
              ),
               
              (
                (25000-df.struct_tax_val.min()) / 
                      (df.struct_tax_val.max()-df.struct_tax_val.min()),
                (2000000-df.struct_tax_val.min()) / 
                      (df.struct_tax_val.max()-df.struct_tax_val.min())
              ),
                  
              (
                (10000-df.land_tax_val.min()) / 
                      (df.land_tax_val.max()-df.land_tax_val.min()),
                (2500000-df.land_tax_val.min()) / 
                      (df.land_tax_val.max()-df.land_tax_val.min())
              ),
              (
                (500-df.lotsize.min())/(df.lotsize.max()-df.lotsize.min()),
                (8000-df.lotsize.min())/(df.lotsize.max()-df.lotsize.min())
              ),
              (
                (500-df.tax.min())/(df.tax.max()-df.tax.min()),
                (8000-df.tax.min())/(df.tax.max()-df.tax.min())
              )]

    dictionary = dict(zip(keys, values))
    
    for key, value in dictionary.items():
        new_df = df[df[key] >= value[0]]
        new_df = df[df[key] <= value[1]]          
            
            
    return new_df


# The code below from Codeup's curriculum.
def drop_outliers(df):
    
    new_df = df.copy()

    keys = ['bathroomcnt','bedroomcnt','calculatedfinishedsquarefeet', 
            'structuretaxvaluedollarcnt','landtaxvaluedollarcnt']

    values = [(1,7), (1,7), (500,8000), (25000,2000000), (10000,2500000)]
    dictionary = dict(zip(keys, values))
    
    for key, value in dictionary.items():
        new_df = df[df[key] >= value[0]]
        new_df = df[df[key] <= value[1]]          
            
    return new_df


# The code below inspired by Codeup's curriculum.
def handle_outliers(s, k = 1.5, m = 'iqr'):
    '''
    Given a series and a cutoff value, k, returns the upper outliers for
    the series.

    The values returned will be either 0 (if the point is not an outlier),
    or a number that indicates how far away from the upper or lower bound
    the observation is.
    '''
    s = s.copy()
    if m == 'iqr':
        q1, q3 = s.quantile([.25, .75])
        iqr = q3 - q1
        upper_bound = q3 + k * iqr
        lower_bound = q1 - k * iqr
    #     upper = s.apply(lambda x: max([x - upper_bound, 0]))
    #     lower = s.apply(lambda x: max([lower_bound - x, 0]))
    
    elif m == 'std':
        # TODO: handle outliers using standard deviation.
        #     df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
        pass
    elif m == 'pcnt':
        # TODO: handle outliers by top or bottom 1%
        pass

    
    
    return (upper_bound, lower_bound)


# The code below inspired by Codeup's curriculum.
def create_outlier_df(df, k = 1.5, m = 'iqr'):
    '''
    Create and return a new dataframe with only the outliers 
    to all numeric columns in the given dataframe.
    '''
   # create a new dataframe for outliers only
    out_df = pd.DataFrame()
    
    for col in df.select_dtypes('number'):
        upper, lower = handle_outliers(df[col], k, m)
        out_df[col + '_upper_outliers'] = upper
        out_df[col + '_lower_outliers'] = lower

    return out_df


# tried to do a better job at preparing data... 
# ended up not using this due to time constraints.
def prepare_zillow():
    # Creating and returning dataframe here assuming aquire created
    # the csv file previously.
    
    # get the zillow data and set the customer_id as the index
    print('Reading Zillow data...')
    zillow_df = pd.read_csv('zillow_data.csv')
    
    print('Preparing and cleaning Zillow data...')
    # make the parcelid the index so we don't have the extra index column
    zillow_df.set_index('parcelid', inplace=True)
    # the id was added by SQL in creating file and is not needed
    zillow_df.drop(columns='id', inplace=True) 
    # print the summary
#     df_summary(zillow_df)
    
    # keep only single unit properties
    zillow_df = keep_only_single_unit_properties(zillow_df)
    
    # drop unitcnt column now
    zillow_df = zillow_df.drop(columns=['unitcnt'])
    
    # dropping columns with more than 45% data missing in a column
    # and dropping rows with more than 25% data missing in the row
    zillow_df = data_prep(
        zillow_df,
        cols_to_remove=[],
        prop_required_column=.55,
        prop_required_row=.75
    )
    
    # fill calculatedbathnbr and fullbathcnt with bathroomcnt
    zillow_df = fix_bathroom_cnts(zillow_df)
    
    # drop the rows with more than specified percentage of nans in any fields 
    zillow_df = data_prep(
        zillow_df,
        cols_to_remove=[],
        prop_required_column=.55,
        prop_required_row=1
    )
    
    # data is now clean, so convert the column datatypes appropriately
    zillow_df = convert_number_columns_to_appropriate_datatype(zillow_df)

    # use Maggie's function to drop hard-coded outliers
    zillow_df = drop_outliers(zillow_df)
   
    # then use my function to find iqr outliers and then drop them
    for col in zillow_df.select_dtypes('number'):
        upper, lower = handle_outliers(zillow_df[col], 1.5)
        zillow_df = zillow_df.loc[(zillow_df[col] >= lower) & (zillow_df[col] <= upper)]
    print('after my function, roomcnt still looks good')
    print(zillow_df.select_dtypes('number').sample(3))
        
    # standardize some data and reorder and rename columns
    zillow_df = standardize_data(zillow_df)
    print('after standardize_data, somehow, it turned to all Nans...')
    print(zillow_df.select_dtypes('number').sample(3))
    
    print('Zillow data is now ready for analysis!')
    
    return zillow_df


def prepare_zillow_without_outliers():
    # Creating and returning dataframe here assuming aquire created
    # the csv file previously.
    
    # get the zillow data and set the customer_id as the index
    print('Reading Zillow data...')
    zillow_df = pd.read_csv('zillow_data.csv')
    
    print('Preparing and cleaning Zillow data...')
    # make the parcelid the index so we don't have the extra index column
    zillow_df.set_index('parcelid', inplace=True)
    # the id was added by SQL in creating file and is not needed
    zillow_df.drop(columns='id', inplace=True) 
    # print the summary
#     df_summary(zillow_df)
    
    # keep only single unit properties
    zillow_df = keep_only_single_unit_properties(zillow_df)
    
    # drop unitcnt column now
    zillow_df = zillow_df.drop(columns=['unitcnt'])
    
    # dropping columns with more than 45% data missing in a column
    # and dropping rows with more than 25% data missing in the row
#     zillow_df = data_prep(
#         zillow_df,
#         cols_to_remove=[],
#         prop_required_column=.55,
#         prop_required_row=.75
#     )
    
    zillow_df = fix_bathroom_cnts(zillow_df)
    zillow_df = fill_with_median(zillow_df, ['buildingqualitytypeid', 'yearbuilt'])
    zillow_df = fill_with_none(zillow_df, 'heatingorsystemdesc')
    
    # Impute the values in land square feet using linear regression
    # with landtaxvaluedollarcnt as x and estimated land square feet as y.
    impute_missing(zillow_df)
    
    # print(missing_values_col(zillow_df))
    # print(missing_values_row(zillow_df))
    
    # Added code from Ednalyn de Dios to aggressively limit outliers
    # Remove outliers and nonsensical observations
    # TODO: do this using function with selectable method.
    zillow_df = zillow_df[zillow_df.bathroomcnt <= 15]
    zillow_df = zillow_df[zillow_df.bedroomcnt <= 13]
    zillow_df = zillow_df[zillow_df.calculatedbathnbr <= 15]
    zillow_df = zillow_df[zillow_df.calculatedfinishedsquarefeet <= 14000]
    zillow_df = zillow_df[zillow_df.fullbathcnt <= 15]
    zillow_df = zillow_df[zillow_df.latitude >= 33500000]
    zillow_df = zillow_df[zillow_df.lotsizesquarefeet <= 2000000]
    zillow_df = zillow_df[zillow_df.landtaxvaluedollarcnt <= 20000000]
    
    # drop the fullbath and calcbath columns 
    # as they duplicate bathroomcnt and are less accurate
#     zillow_df.loc[(zillow_df['bath'] != zillow_df['fullbath'])]
#     zillow_df.loc[(zillow_df['bath'] != zillow_df['calcbath'])]
    zillow_df = zillow_df.drop(columns=['fullbathcnt', 'calculatedbathnbr'], axis=0)
    
    # Drop the erroneous zip code value of 399675.00
#     zillow_df['zip'].loc[(zillow_df['zip'] == 399675.00)].count()
    zillow_df = zillow_df.loc[(zillow_df['regionidzip'] != 399675.00)]
#     zillow_df['zip'].loc[(zillow_df['zip'] == 399675.00)].count()
    
    # drop roomcnt because I can't figure out why it's getting Nan values put in it
    zillow_df = zillow_df.drop(columns=['roomcnt'], axis=0)
    
    
    # drop the rows with nans in ANY fields
    zillow_df = data_prep(
        zillow_df,
        cols_to_remove=[],
        prop_required_column=.55,
        prop_required_row=1
    )
    
    # data is now clean, so convert the column datatypes appropriately
    zillow_df = convert_number_columns_to_appropriate_datatype(zillow_df)
    
    # standardize some data and reorder and rename columns
    norm_cols = ['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 
                 'finishedsquarefeet12', 'yearbuilt', 'landtaxvaluedollarcnt',
                 'taxamount', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt',
                 'lotsizesquarefeet'] 
    
    zillow_df = drop_outliers(zillow_df)

    zillow_df = standardize_data(zillow_df)
    
    print('Zillow data is now ready for analysis!')
    
    return zillow_df
