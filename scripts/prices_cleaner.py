'''
This script applies a data cleaning process to the prices ENTSO-E collected 
raw data
'''

# import libraries
import pandas as pd
import time
from config import *
from cleaning_utils import (
    load_raw_data,
    convert_datetime,
    check_input_frequency,
    to_hourly,
    export_table
)

# script execution measure
start = time.time()

# define raw dataset path
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'

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

# EXECUTION
if __name__ == '__main__':
    # script start time execution
    start = time.time()

    # cleaner for each zone
    for zone in ZONES:
        # clean zonal prices
        prices = clean_prices(zone)
        # export cleaned zonal prices
        export_table(prices, zone, var_type='prices')

    # scripts end time execution
    end = time.time()
    # print time of script execution
    print(f'Execution time: {end - start}')