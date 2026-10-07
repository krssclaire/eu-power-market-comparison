'''
Assesses if the single datasets are ready to be used
'''

import pandas as pd
import time
from config import *

# define clean dataset path
clean_data_path = PROJECT_ROOT / 'dataset' / 'clean'

# LOAD
def load_clean_data(data_path, dataset_type, zone):
    '''
    Loads the raw ENTSO-E dataset corresponding to the selected 
    dataset type and bidding zone
    '''
    if dataset_type == 'generation':
        df = pd.read_csv(
            data_path
            / dataset_type
            / f'{zone}-{dataset_type}.csv'
        )
    elif dataset_type == 'load':
        df = pd.read_csv(
            data_path
            / dataset_type
            / 'load-clean.csv'
        )
    else:
        df = pd.read_csv(
            data_path
            / dataset_type
            / 'zonal-prices-clean.csv'
        )

    # restore datetime datatype after CSV import
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(
            df['datetime'],
            utc=True
        )

    if 'datetime_UTC' in df.columns:
        df['datetime_UTC'] = pd.to_datetime(
            df['datetime_UTC'],
            utc=True
        )

    return df

# VALIDATION PROCESS
def validate_datetime(df, datetime_col):
    '''
    Asserts datetime statements (missing dt, incorrect datatype)
    '''
    assert datetime_col in df.columns, \
        f'Missing required column: {datetime_col}'
    assert pd.api.types.is_datetime64_any_dtype(df[datetime_col]), \
        'Datetime column is not in datetime format'
    assert df[datetime_col].notna().all(), \
        'Missing timestamps found'

    if df[datetime_col].dt.tz is None:
        raise AssertionError(
            'Datetime column is timezone-naive'
        )
    print('MSG: datetime validation passed')

def check_duplicates(df, datetime_col):
    '''
    Checks for datetime duplicates
    '''
    # count duplicates
    duplicates = df[datetime_col].duplicated().sum()

    assert duplicates == 0, \
        f'Duplicated timestamps found: {duplicates}'
    print('MSG: duplicate timestamp check passed')

def check_sorted(df, datetime_col):
    '''
    Checks if the date is correctly sorted
    '''
    assert df[datetime_col].is_monotonic_increasing, \
        'Datetime column is not sorted'
    print('MSG: datetime sorting check passed')

def check_frequency(df, datetime_col):
    '''
    Checks that the frequency is the one desired
    '''
    frequency = df[datetime_col].diff().dropna()

    print('\n--- OBSERVED FREQUENCIES ---')
    print(frequency.value_counts().head())

    expected_delta = pd.Timedelta(hours=1)

    unexpected = frequency[frequency != expected_delta]

    if len(unexpected) > 0:
        print(
            f'WARNING: {len(unexpected)} '
            'unexpected time intervals found'
        )
        print(unexpected.head())
    else:
        print('MSG: frequency validation passed')

def check_missing_values(df, exclude_cols=None):
    '''
    Checks other missing values and retruns for each columns 
    the number of missing values
    '''
    if exclude_cols is None:
        exclude_cols = []

    # get columns to inspect
    cols = [
        col for col in df.columns
        if col not in exclude_cols
    ]

    # get missing values
    missing = df[cols].isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print('MSG: no missing values found')
    else:
        print('\n--- MISSING VALUES ---')
        print(missing)

def check_numeric_columns(df, exclude_cols=None):
    '''
    Checks if columns have numeric values and reports which
    ones don't have numeric values
    '''
    if exclude_cols is None:
        exclude_cols = ['datetime']

    non_numeric = df[
        [col for col in df.columns if col not in exclude_cols]
    ].select_dtypes(exclude='number').columns

    if len(non_numeric) > 0:
        raise AssertionError(
            f'Non-numeric columns found: {list(non_numeric)}'
        )

    print('MSG: numeric columns validation passed')

# MAIN VALIDATION PIPELINE
def validate_dataset(df, datetime_col, check_numeric=False):
    validate_datetime(df, datetime_col)
    check_duplicates(df, datetime_col)
    check_sorted(df, datetime_col)
    check_frequency(df, datetime_col)
    check_missing_values(df, exclude_cols=[datetime_col])

    if check_numeric:
        check_numeric_columns(
            df,
            exclude_cols=[datetime_col]
        )

    print('\nMSG: dataset validation completed')

# EXECUTION
types = ['generation', 'prices', 'load']

for var_type in types:
    # script execution measure
    start = time.time()

    # filter by variable type
    if var_type == 'generation':
        datetime_column = 'datetime'
        for zone in ZONES:
            print(f'\n_____________{zone} VALIDATION_____________')
            df = load_clean_data(clean_data_path, var_type, zone)
            validate_dataset(df, datetime_column)
    else:
        datetime_column = 'datetime_UTC'
        df = load_clean_data(clean_data_path, var_type, None)
        validate_dataset(df, datetime_column)

    # scripts end time execution
    end = time.time()
    # print time of script execution
    print(f'Execution time: {end - start}')