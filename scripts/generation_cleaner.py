'''
Applies a data cleaning process to the generation ENTSO-E collected raw data
'''

# import libraries
import pandas as pd
import time
from config import *

# define raw dataset path
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'

# LOADING
def load_raw_data(raw_data_path, dataset_type, zone, year):
    '''
    Loads the raw ENTSO-E dataset corresponding to the selected variable 
    type, bidding zone and year
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


def gen_to_hourly(df, datetime_col, cols=None):
    '''
    Converts quarterly-hour data to hourly granularity
    '''
    if cols is None:
        raise ValueError('Columns must be specified')

    df = df.copy()
    # convert datetime to correct datatype
    df[datetime_col] = pd.to_datetime(df[datetime_col], utc=True)

    # convert generation columns to correct datatype
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

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

    # script execution
    for zone in ZONES:
        # clean zonal prices
        generation = clean_generation(zone)
        # export cleaned zonal generation
        export_table(generation, zone, var_type='generation')

    # scripts end time execution
    end = time.time()
    # print time of script execution
    print(f'Execution time: {end - start}')