import pandas as pd

def sort_col_val(df_name):
    df = df_name.copy()
    df_cols = df_name.columns
    for col in df_cols:
        print('Sorted by ' + str(col) + ':')
        print('Head:')
        print(df[[col]].sort_values(by=[col]).head(3).T)
        print(' ')
        print('Tail: ')
        print(df[[col]].sort_values(by=[col]).tail(3).T)
        print('-----')


# The code below inspired by Michael P. Moran's missing_vals_df().
def missing_values_col(df):
    """
    Write or use a previously written function to return the
    total missing values and the percent missing values by column.
    """
    df = df.copy()
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
    df = df.copy()
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

def df_summary(df):
    # pd.options.display.max_columns = 4 # this prints ONLY 4 columns
    # rather than wrapping and printing 4 per row
    
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print('--- Top and Bottom:')
    print(sort_col_val(df), end='\n\n')

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')    
    print(f'--- Shape:\n{df.shape}', end='\n\n')

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(f'--- Info:\n')
    print(df.info(), end='\n\n')
    
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # A sparse array is one that contains mostly zeros and few non-zero 
    # entries. A dense array contains mostly non-zeros.
    print(f'--- Check if all ftypes are dense:\n')
    print('A sparse array is one that contains mostly zeros and few non-zero')
    print('entries. A dense array contains mostly non-zeros.')
    print(df.ftypes.value_counts(), end='\n\n')
    
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(f'--- Descriptions:')
    print(df.describe(include='all'), end='\n\n')

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #print(f'--- Nulls By Column:\n{df.isna().sum()}', end='\n\n')
    print(f'---Nulls By Columns:')
    print(missing_values_col(df), end='\n\n')
    
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(f'--- Summary of Nulls by Rows:')
    print(missing_values_row(df), end='\n\n')
       
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(f'--- amount of missing values in columns:')
    print(amount_of_missing_values_in_columns(df), end='\n\n')
    
#     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#     print('--- Value Counts of the following columns:')
#     columns = ['hvac', 'landusedesc', 'regionidcounty', 'fips', 'bldgqualtype']
#     for col in columns:
#         print(col, df[col].value_counts(dropna=False))
#     print()
#     print()
#     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                                
#     print('df.age.value_counts binned:')
#     print(df.age.value_counts(bins=[18, 26, 32, 40, 50, 80]), end='\n\n')
    
#     print('df.select_dtypes("number"):')
#     for col in df.select_dtypes('number'):
#           print(col)
#           print(df[col].value_counts(bins=4))
#     print()
#     print()