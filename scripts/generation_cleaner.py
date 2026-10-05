'''
Applies a data cleaning process to the generation ENTSO-E collected raw data
'''

# import libraries
import pandas as pd
import time
from config import *
from cleaning_utils import (
    load_raw_data,
    convert_datetime,
    check_input_frequency,
    export_table
)

# define raw dataset path
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'

# TRANSFORMATION
def standardize_generation_columns(df, zone):
    '''
    Renames the columns of the ENTSO-E generation dataset
    '''
    # rename datetime column
    standardized_generation_df = df.rename(
        columns={
            'Unnamed: 0': 'datetime'
        }
    )
    print(f'MSG: generation columns renamed for {zone}')

    return standardized_generation_df

def gen_to_hourly(df, datetime_col, cols=None):
    '''
    Converts quarterly-hour data to hourly granularity.
    If an hour has incomplete data, that hour is set to NA
    '''
    if cols is None:
        raise ValueError('Columns must be specified')

    df = df.copy()
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    # get missing values percentage per columns
    missing_pct = (
        df[cols]
        .isna()
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    # calculate hourly averages
    hourly = (
        df
        .set_index(datetime_col)
        .resample('h')[cols]
        .mean()
        .reset_index()
    )

    print(missing_pct)
    print('MSG: generation data converted to hourly frequency')

    return hourly

# generation = generation_data.columns[1:]

# VALIDATION
def validate_generation(df, datetime_col, generation_cols):
    ''' 
    Validates the cleaned generation dataset
    '''
    # check required columns: datetime and generation
    assert datetime_col in df.columns, \
        f'generation_validator: Missing required column: {datetime_col}'

    for col in generation_cols:
        assert col in df.columns, \
            f'generation_validator: Missing required column: {col}'

    # check datetime
    assert pd.api.types.is_datetime64_any_dtype(df[datetime_col]), \
        f'generation_validator: Datetime column is not in datetime format'

    # check datetime duplicates
    assert df[datetime_col].duplicated().sum() == 0, \
        f'generation_validator: Duplicated timestamps found'

    # check chronological order
    assert df[datetime_col].is_monotonic_increasing, \
        f'generation_validator: Datetime column is not sorted'

    print('MSG: generation validation passed')

# MAIN CLEANING PIPELINE
def clean_generation(zone):
    '''
    Complete cleaning pipeline for ENTSO-E generation
    '''
    
    # generation raw data
    df = load_raw_data(
        raw_dataset_path,
        dataset_type='generation',
        zone=zone
    )
    
    # standardize columns
    df = standardize_generation_columns(df, zone)
    
    # convert datetime
    df = convert_datetime(df)

    # check frequency
    check_input_frequency(df)
    
    # convert to hourly frequency
    df = gen_to_hourly(
        df,
        datetime_col='datetime',
        cols=df.columns[1:]
    )
    
    # validate cleaned data
    validate_generation(
        df,
        datetime_col='datetime',
        generation_cols=df.columns.drop('datetime')
    )

    return df

# EXECUTION
if __name__ == '__main__':
    # script start time execution
    start = time.time()

    zone = 'IT_NORD'

    # script execution
    #for zone in ZONES:
        # clean zonal prices
    generation = clean_generation(zone)
    # export cleaned zonal generation
    export_table(generation, zone, var_type='generation')

    # scripts end time execution
    end = time.time()
    # print time of script execution
    print(f'Execution time: {end - start}')