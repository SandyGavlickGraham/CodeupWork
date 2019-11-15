# Eric Escalante's code:
import pandas as pd
from datetime import datetime

def get_data():
    df = pd.read_csv('http://python.zach.lol/access.log',          
                  engine='python',
                  header=None,
                  index_col=False,
                  names=['ip', 'timestamp', 'request_method', 'status', 'size', 'request_agent'],
                  sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                  na_values='-',
                  usecols=[0, 3, 4, 5, 6, 8],
                  skip_blank_lines=True)

    df.timestamp = df.timestamp.str.replace('[', '')
    df.timestamp = df.timestamp.str.replace(']', '')
    df.timestamp= pd.to_datetime(df.timestamp.str.replace(':', ' ', 1)) 

    df.request_method = df.request_method.str.replace('"', '')

    df = df.set_index('timestamp')
    df = df.tz_localize('utc').tz_convert('America/Chicago')
    
    return(df)

if __name__ == '__main__':
    new_df = get_data()
    print(new_df.head(3).append(new_df.tail(3)))