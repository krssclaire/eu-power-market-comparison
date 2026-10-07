'''
This script contains a set of general functions that can be used for data 
cleaning process to the ENTSO-E collected raw data
'''

# import libraries
import pandas as pd
from config import *

# define raw dataset path
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'


# LOADING
def load_raw_data(raw_data_path, dataset_type, zone, year):
    '''
    Loads the raw ENTSO-E dataset corresponding to the selected variable 
    type and bidding zone
    '''
    # read csv file from specific folder
    df = pd.read_csv(
        raw_data_path 
        / f'{dataset_type}' 
        / f'{zone}'
        / f'{zone}-{year}-{dataset_type}.csv'
    )

    print(f'MSG: {dataset_type} data loaded')

    return df

# TRANSFORMATION    
def convert_datetime(df, datetime_col='datetime'):
    '''
    Converts the datetime column after renaming process, in order to 
    correctly treat the datetime data type
    '''
    # convert datetime column to its correct datatype
    df = df.copy()
    df[datetime_col] = pd.to_datetime(
        df[datetime_col], 
        utc=True
    )

    timezone = df[datetime_col].dt.tz

    print(f'MSG: date column converted to datetime in {timezone} time zone')
    
    return df

def check_input_frequency(df):
    '''
    Checks if each hour has four quart-hourly observations
    '''
    hourly_counts = (
        df
        .set_index('datetime')
        .resample('h')
        .size()
    )

    print(f'Number of observations per hour: {hourly_counts.value_counts().sort_index()}')

def to_hourly(df, datetime_col='datetime', value_cols=None):
    '''
    Takes a dataframe with quarter-hourly data to hourly frequency by 
    calculating the arithmetic mean

    If the input data are already hourly, no resampling is performed.
    If the input data are sub-hourly, hourly means are calculated.
    '''
    # preliminary check
    if value_cols is None:
        raise ValueError('value_cols must be specifies')

    # DataFrame convertion from quarter-hourly to hourly granularity
    df = df.copy()

    # check input frequency
    frequency = (
        df[datetime_col]
        .sort_values()
        .diff()
        .dropna()
        .mode()[0]
    )

    if frequency == pd.Timedelta(hour=1):
        print('MSG: data already at hourly frequency')
        return df
    else:
        df = (
            df
            .set_index(datetime_col)
            .resample('h')[value_cols]
            .mean()
            .reset_index()
        )
        print(f'MSG: data converted from {frequency} to hourly frequency')
        return df


# EXPORT
def export_table(df, zone, year, var_type):
    '''
    Exports the cleanes dataset to the corresponding clean data folder    
    '''
    # define clean dataset path
    output_path = PROJECT_ROOT / 'dataset' / 'clean' / f'{var_type}'

    # create folder if non-existent
    output_path.mkdir(parents=True, exist_ok=True)

    # save in CSV format
    df.to_csv(output_path / f'{zone}-{year}-{var_type}.csv', index=False)

    print(f'MSG: {var_type} cleaned data exported to {output_path}')