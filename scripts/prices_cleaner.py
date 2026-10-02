'''
The aim of this script is to apply a data cleaning process to the prices ENTSO-E collected raw data
'''

# import libraries
import pandas as pd
from pathlib import Path
from config import *
import time

# script execution measure
start = time.time()

# define raw dataset path
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'

# defina main function for data cleaning

# LOADING
def load_raw_data(raw_data_path, dataset_type, zone):
    '''
    Loads the raw ENTSO-E dataset corresponding to the selected variable type and bidding zone
    '''
    # read csv file from specific folder
    df = pd.read_csv(
        raw_data_path 
        / f'{dataset_type}' 
        / f'{zone}-{dataset_type}.csv'
    )

    print(f'MSG: {dataset_type} data loaded')

    return df

# TRANSFORMATION
def standardize_prices_columns(df, zone):
    '''
    Renames the columns of the ENTSO-E prices dataset
    '''
    # rename datetime column
    standardized_prices_df = df.rename(
        columns={
            'Unnamed: 0': 'datetime', 
            '0': f'prices_{zone}'
        }
    )
    print(f'MSG: prices columns renamed for {zone}')

    return standardized_prices_df
    
def convert_datetime(df, datetime_col='datetime'):
    '''
    Converts the datetime column after renaming process, in order to correctly treat the datetime data type
    '''
    # convert datetime column to its correct datatype
    df[datetime_col] = pd.to_datetime(
        df[datetime_col]
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
    Takes a dataframe with quarter-hourly data to hourly frequency by calculating the arithmetic mean
    '''
    # preliminary check
    if value_cols is None:
        raise ValueError('value_cols must be specifies')

    # DataFrame convertion from quarter-hourly to hourly granularity
    df = df.copy()
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    df = (
        df
        .set_index(datetime_col)
        .resample('h')[value_cols]
        .mean()
        .reset_index()
    )

    print('MSG: data converted to hourly frequency')

    return df

# VALIDATION
def validate_prices(df, datetime_col, prices_col=None):
    ''' 
    Validates the cleaned prices dataset
    '''
    # check required columns: datetime and prices
    assert datetime_col in df.columns, \
        f'Prices_validator: Missing required column: {datetime_col}'
    
    assert prices_col in df.columns, \
        f'Prices_validator: Missing required column: {prices_col}'

    # check datetime
    assert pd.api.types.is_datetime64_any_dtype(df[datetime_col]), \
        f'Prices_validator: Datetime column is not in datetime format'

    # check datetime duplicates
    assert df[datetime_col].duplicated().sum() == 0, \
        f'Prices_validator: Duplicated timestamps found'

    # check chronological order
    assert df[datetime_col].is_monotonic_increasing, \
        f'Prices_validator: Datetime column is not sorted'

    # check missing prices
    assert df[prices_col].isna().sum() == 0, \
        f'Prices_validator: Missing prices'

    print('MSG: prices validation passed')

# MAIN CLEANING PIPELINE
def clean_prices(zone):
    '''
    Complete cleaning pipeline for ENTSO-E day-ahead prices
    '''
    
    # load raw data
    df = load_raw_data(
        raw_dataset_path,
        dataset_type='prices',
        zone=zone
    )
    
    # standardize columns
    df = standardize_prices_columns(df, zone)
    
    # convert datetime
    df = convert_datetime(df)

    # check frequency
    check_input_frequency(df)
    
    # convert to hourly frequency
    df = to_hourly(
        df,
        datetime_col='datetime',
        value_cols=[f'prices_{zone}']
    )
    
    # validate cleaned data
    validate_prices(
        df,
        datetime_col='datetime',
        prices_col=f'prices_{zone}'
    )
    
    return df
    
# EXPORT
def export_table(df, zone, var_type='prices'):
    '''
    Exports the cleanes dataset to the corresponding clean data folder    
    '''
    # define clean dataset path
    output_path = PROJECT_ROOT / 'dataset' / 'clean' / f'{var_type}'

    # create folder if non-existent
    output_path.mkdir(parents=True, exist_ok=True)

    # save in CSV format
    df.to_csv(output_path / f'{zone}-{var_type}.csv', index=False)

    print(f'MSG: {var_type} cleaned data exported to {output_path}')

# EXECUTION
if __name__ == '__main__':
    for zone in ZONES:
        # clean zonal prices
        prices = clean_prices(zone)
        # export cleaned zonal prices
        export_table(prices, zone)


# SCRIPT PERFORMANCE --> time should depend on the amount of data retrieved
end = time.time()
print(f'Execution time: {end - start}')