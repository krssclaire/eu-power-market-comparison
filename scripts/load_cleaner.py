'''
Applies a data cleaning process to the load ENTSO-E collected raw data
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

# define raw dataset path
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'

# TRANSFORMATION
def standardize_load_columns(df, zone):
    '''
    Renames the columns of the ENTSO-E load dataset
    '''
    # rename datetime column
    standardized_load_df = df.rename(
        columns={
            'Unnamed: 0': 'datetime', 
            'Actual Load': f'load_{zone}'
        }
    )
    print(f'MSG: load columns renamed for {zone}')

    return standardized_load_df

# VALIDATION
def validate_load(df, datetime_col, load_col=None):
    ''' 
    Validates the cleaned load dataset
    '''
    # check required columns: datetime and load
    assert datetime_col in df.columns, \
        f'Load_validator: Missing required column: {datetime_col}'
    
    assert load_col in df.columns, \
        f'Load_validator: Missing required column: {load_col}'

    # check datetime
    assert pd.api.types.is_datetime64_any_dtype(df[datetime_col]), \
        f'Load_validator: Datetime column is not in datetime format'

    # check datetime duplicates
    assert df[datetime_col].duplicated().sum() == 0, \
        f'Load_validator: Duplicated timestamps found'

    # check chronological order
    assert df[datetime_col].is_monotonic_increasing, \
        f'Load_validator: Datetime column is not sorted'

    # check missing load
    assert df[load_col].isna().sum() == 0, \
        f'Load_validator: Missing load'

    print('MSG: load validation passed')

# MAIN CLEANING PIPELINE
def clean_load(zone):
    '''
    Complete cleaning pipeline for ENTSO-E load
    '''
    
    # load raw data
    df = load_raw_data(
        raw_dataset_path,
        dataset_type='load',
        zone=zone
    )
    
    # standardize columns
    df = standardize_load_columns(df, zone)
    
    # convert datetime
    df = convert_datetime(df)

    # check frequency
    check_input_frequency(df)
    
    # convert to hourly frequency
    df = to_hourly(
        df,
        datetime_col='datetime',
        value_cols=[f'load_{zone}']
    )
    
    # validate cleaned data
    validate_load(
        df,
        datetime_col='datetime',
        load_col=f'load_{zone}'
    )
    
    return df
    
# EXECUTION
if __name__ == '__main__':
    # script start time execution
    start = time.time()

    # script execution
    for zone in ZONES:
        # clean zonal prices
        load = clean_load(zone)
        # export cleaned zonal load
        export_table(load, zone, var_type='load')

    # scripts end time execution
    end = time.time()
    # print time of script execution
    print(f'Execution time: {end - start}')