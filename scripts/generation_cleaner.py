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
    Loads the raw ENTSO-E dataset corresponding to the selected 
    dataset type, bidding zone and year
    '''
    # define file path
    file_path = (
        raw_data_path
        / dataset_type
        / zone
        / f'{zone}-{year}-{dataset_type}.csv'
    )

    # inspect first two rows to identify MultiIndex structure
    preview = pd.read_csv(
        file_path,
        header=None,
        nrows=2
    )

    has_multiindex = (
        len(preview) >= 2
        and 'Actual Aggregated' in preview.iloc[1].astype(str).values
    )

    # filter 
    if has_multiindex:
        df = pd.read_csv(
            file_path, 
            header=[0, 1]
        )
        print(f'MSG: {zone} {year} loaded with MultiIndex structure')
    else:
        df = pd.read_csv(file_path)
        print(f'MSG: {zone} {year} loaded with standard structure')

    return df

# TRANSFORMATION
def keep_actual_aggregated(df, zone, year):
    '''
    Keeps only Actual Aggregated generation series 
    and removes the MultiIndex structure when present 
    '''
    # identify MultiIndex structure
    if isinstance(df.columns, pd.MultiIndex):
        # keep datetime column
        first_col = df.columns[0]

        # get generation aggregated columns
        aggregated_cols = (
            df.columns.get_level_values(1) == 'Actual Aggregated'
        )

        # keep datetime column + Actual Aggregated columns
        df = df.loc[
            :,
            [first_col] + list(df.columns[aggregated_cols])
        ]

        # flatten MultiIndex
        df.columns = [
            'datetime' if col == first_col else col[0]
            for col in df.columns
        ]
        print(f'MSG: {zone} {year} - kept Actual Aggregated generation')
    else:
        df = df.rename(columns={df.columns[0]: 'datetime'})
        print(f'MSG: {zone} {year} - no MultiIndex detected')

    print(df.columns.tolist())
    return df        

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
    
    # get timezone for check
    timezone = df[datetime_col].dt.tz

    print(f'MSG: date column converted to datetime in {timezone} time zone')
    return df

def check_input_frequency(df):
    '''
    Detects the most common time interval between observations
    '''
    frequency = (
        df['datetime']
        .sort_values()
        .diff()
        .dropna()
        .mode()
        .iloc[0]
    )

    print(f'MSG: detected input frequency: {frequency}')
    return frequency

def gen_to_hourly(df):
    '''
    Converts generation data to hourly frequency 

    Existing hourly observatoins are preserved, while sub-hourly 
    observations are aggregated using the hourly mean
    '''
    # select generation columns
    df = df.copy()
    generation_cols = [
        col for col in df.columns
        if col != 'datetime'
    ]

    # hourly resampling
    hourly = (
        df.set_index('datetime')[generation_cols]
        .resample('h')
        .mean()
        .reset_index()
    )

    print('MSG: generation data standardized to hourly frequency')
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
def export_table(df, zone, var_type):
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

# MAIN CLEANING PIPELINE
def clean_generation(zone):
    # array for final concatenation
    yearly_data = []

    for year in YEARS:
        df = load_raw_data(
            raw_dataset_path,
            dataset_type='generation',
            zone=zone,
            year=year
        )

        df = keep_actual_aggregated(
            df,
            zone,
            year
        )

        df = convert_datetime(df)

        yearly_data.append(df)

    # concatenate all years
    generation = pd.concat(
        yearly_data,
        axis=0,
        ignore_index=True,
        sort=False
    )
    print(f'MSG: {zone} yearly generation datasets concatenated')

    check_input_frequency(generation)

    generation = gen_to_hourly(generation)

    validate_generation(generation, 'datetime', generation.columns[1:])

    return generation

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