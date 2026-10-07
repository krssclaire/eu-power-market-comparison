'''
Assesses if the datasets are ready to use, by verifying:
- same timezone
- same granularity
- ordered datetime
- unique datetime
- same time span
- percentage of missing values
- gaps
'''

import pandas as pd
import time
from config import *
from cleaning_utils import load_raw_data

# script execution measure
start = time.time()

# define raw dataset path
dataset_path = PROJECT_ROOT / 'dataset' / 'clean'

def validate_datetime(df, datetime_col='datetime'):
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

def check_duplicates(df, datetime_col='datetime'):

    duplicates = df[datetime_col].duplicated().sum()

    assert duplicates == 0, \
        f'Duplicated timestamps found: {duplicates}'

    print('MSG: duplicate timestamp check passed')

def check_sorted(df, datetime_col='datetime'):

    assert df[datetime_col].is_monotonic_increasing, \
        'Datetime column is not sorted'

    print('MSG: datetime sorting check passed')

def check_frequency(df, datetime_col='datetime', expected='h'):

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

    if exclude_cols is None:
        exclude_cols = []

    cols = [
        col for col in df.columns
        if col not in exclude_cols
    ]

    missing = df[cols].isna().sum()

    missing = missing[missing > 0]

    if missing.empty:
        print('MSG: no missing values found')
    else:
        print('\n--- MISSING VALUES ---')
        print(missing)

def check_numeric_columns(df, exclude_cols=None):

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

def check_missing_timestamps():
    return

def validate_dataset(
    df,
    datetime_col='datetime',
    check_numeric=False
):

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
types = ['prices', 'load', 'generation']

for var_type in types:
    for zone in ZONES:
        for year in YEARS:
            input_path = dataset_path / f'{var_type}'
            load_raw_data(input_path, var_type, zone, year)