'''
Assesses if all the datasets are ready to be merged
'''
import pandas as pd
import time
from config import *
from validation import load_clean_data

# define clean dataset path
clean_data_path = PROJECT_ROOT / 'dataset' / 'clean'


# CHECK COMPATIBILITY BETWEEN THE DATASETS
def check_timezone(prices, load, generation):
    """
    Checks whether all datasets use the same timezone
    """
    price_tz = prices['datetime_UTC'].dt.tz
    load_tz = load['datetime_UTC'].dt.tz
    generation_tz = generation['datetime'].dt.tz

    assert price_tz == load_tz == generation_tz, \
        'Datasets do not use the same timezone'
    print('MSG: timezone compatibility passed')

def check_frequency(prices, load, generation):
    """
    Checks if all datasets have hourly frequency
    """
    price_freq = prices['datetime_UTC'].diff().dropna().unique()
    load_freq = load['datetime_UTC'].diff().dropna().unique()
    generation_freq = generation['datetime'].diff().dropna().unique()

    expected = pd.Timedelta(hours=1)

    assert set(price_freq) == {expected}, \
        'Prices do not have hourly frequency'
    assert set(load_freq) == {expected}, \
        'Load does not have hourly frequency'
    assert set(generation_freq) == {expected}, \
        'Generation does not have hourly frequency'

    print('MSG: frequency compatibility passed')


def check_time_span(prices, load, generation):
    """
    Compares the first and last timestamps of all datasets
    """
    spans = {
        'prices': (
            prices['datetime_UTC'].min(),
            prices['datetime_UTC'].max()
        ),
        'load': (
            load['datetime_UTC'].min(),
            load['datetime_UTC'].max()
        ),
        'generation': (
            generation['datetime'].min(),
            generation['datetime'].max()
        )
    }

    print('\n--- DATASET TIME SPANS ---')

    for dataset, (start, end) in spans.items():
        print(f'{dataset}: {start} → {end}')

    starts = [span[0] for span in spans.values()]
    ends = [span[1] for span in spans.values()]

    if len(set(starts)) == 1 and len(set(ends)) == 1:
        print('MSG: time span compatibility passed')
    else:
        print('WARNING: datasets have different time spans')

def check_timestamp_alignment(prices, load, generation):
    """
    Checks if all datasets contain the same timestamps
    within their common time range.
    """
    # find common time range
    common_start = max(
        prices['datetime_UTC'].min(),
        load['datetime_UTC'].min(),
        generation['datetime'].min()
    )
    common_end = min(
        prices['datetime_UTC'].max(),
        load['datetime_UTC'].max(),
        generation['datetime'].max()
    )
    print('\n--- COMMON TIME RANGE ---')
    print(f'{common_start} → {common_end}')

    # extract timestamps within the common range
    price_times = set(
        prices.loc[
            prices['datetime_UTC'].between(common_start, common_end),
            'datetime_UTC'
        ]
    )
    load_times = set(
        load.loc[
            load['datetime_UTC'].between(common_start, common_end),
            'datetime_UTC'
        ]
    )
    generation_times = set(
        generation.loc[
            generation['datetime'].between(common_start, common_end),
            'datetime'
        ]
    )

    # compare timestamp sets
    missing_in_load = price_times - load_times
    missing_in_generation = price_times - generation_times
    missing_in_prices = (
        load_times.union(generation_times) - price_times
    )

    print(f'Price timestamps: {len(price_times)}')
    print(f'Load timestamps: {len(load_times)}')
    print(f'Generation timestamps: {len(generation_times)}')

    print(f'Missing in load: {len(missing_in_load)}')
    print(f'Missing in generation: {len(missing_in_generation)}')
    print(f'Missing in prices: {len(missing_in_prices)}')

    if (
        len(missing_in_load) == 0
        and len(missing_in_generation) == 0
        and len(missing_in_prices) == 0
    ):
        print('MSG: timestamp alignment passed')
    else:
        print('WARNING: timestamp misalignment detected')

# MAIN ORCHESTRATOR
def check_compatibility(prices, load, generation):
    '''
    Verifies the global compatibility among prices, load and 
    generation datasets
    '''
    check_timezone(prices, load, generation)
    check_frequency(prices, load, generation)
    check_time_span(prices, load, generation)
    check_timestamp_alignment(prices, load, generation)

    print('\nMSG: dataset compatibility check completed')

##################  WIP  ###############################

def build_national_dataset(prices, load, generation):
    # select relevant columns from each dataframe
    prices_df = prices[['datetime_UTC', 'Italia']].copy()
    load_df = load[['datetime_UTC', 'Totale Italia']].copy()
    generation_df = generation.copy()

    # rename columns
    prices_df = prices_df.rename(columns={'Italia': 'PUN'})
    load_df = load_df.rename(columns={'Totale Italia': 'National Load'})
    generation_df = generation_df.rename(columns={'datetime': 'datetime_UTC'})

    # merge
    national = prices_df.merge(
        load_df, 
        on='datetime_UTC', 
        how='inner'
    )
    national = national.merge(
        generation_df, 
        on='datetime_UTC', 
        how='inner'
    )

    # get local hour from local datetime --> for analysis purposes
    national['datetime_local'] = (
        national['datetime_UTC']
        .dt.tz_convert('Europe/Rome')
    )
    national['local_hour'] = national['datetime_local'].dt.hour

    # reorder columns
    base_columns = [
        'datetime_UTC',
        'datetime_local',
        'local_hour',
        'PUN',
        'National Load'
    ]
    generation_columns = [
        col for col in national.columns
        if col not in base_columns
    ]
    national = national[
        base_columns + generation_columns
    ]

    print(national.head())
    print(national.columns.tolist())

    return national


def build_zonal_dataset(zone):
    return

def export_processed_dataset(df, zone):
    '''
    Exports the processed dataset to the corresponding folder    
    '''
    # define processed folder path
    output_path = PROJECT_ROOT / 'dataset' / 'processed'

    # create folder if non-existent
    output_path.mkdir(parents=True, exist_ok=True)

    # save in CSV format
    df.to_csv(output_path / f'{zone}.csv', index=False)

    print(f'MSG: {zone} processed data exported to {output_path}')


# LOAD DATA
#for zone in ZONES:
generation = load_clean_data(clean_data_path, 'generation', 'IT')
prices = load_clean_data(clean_data_path, 'prices', None)
load = load_clean_data(clean_data_path, 'load', None)

national_df = build_national_dataset(prices, load, generation)

export_processed_dataset(national_df, 'IT')

'''

check_compatibility(prices, load, generation)

def build_dataset():
    return

dataset = build_dataset(
    prices,
    load,
    generation
)
'''