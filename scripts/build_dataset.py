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
    '''
    Checks whether all datasets use the same timezone
    '''
    price_tz = prices['datetime_UTC'].dt.tz
    load_tz = load['datetime_UTC'].dt.tz
    generation_tz = generation['datetime'].dt.tz

    assert price_tz == load_tz == generation_tz, \
        'Datasets do not use the same timezone'
    print('MSG: timezone compatibility passed')

def check_frequency(prices, load, generation):
    '''
    Checks if all datasets have hourly frequency
    '''
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
    '''
    Compares the first and last timestamps of all datasets
    '''
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

def check_unique_timestamps(df, column, dataset_name):
    '''
    Check timestamp validity and uniqueness
    '''
    if df[column].isna().any():
        raise ValueError(
            f'{dataset_name}: missing timestamps found'
        )
    
    duplicates = df[column].duplicated(keep=False)

    if duplicates.any():
        examples = (
            df.loc[duplicates, column]
            .head(5)
            .tolist()
        )
        raise ValueError(
            f'{dataset_name}: {duplicates.sum()} rows '
            f'with duplicated timestamps. Examples: {examples}'
        )

    print(f'MSG: {dataset_name} timestamps are unique')

def check_timestamp_alignment(prices, load, generation):
    '''
    Checks if all datasets contain the same timestamps within their common time range
    '''
    # find the common time range
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
    print(f'{common_start} -> {common_end}')

    # stop if the datasets have no overlapping time range
    if common_start > common_end:
        print('WARNING: datasets have no common time range')
        return False

    # collect timestamps from each dataset in the common range
    timestamp_sets = {
        'prices': set(
            prices.loc[
                prices['datetime_UTC'].between(
                    common_start, common_end
                ),
                'datetime_UTC'
            ]
        ),
        'load': set(
            load.loc[
                load['datetime_UTC'].between(
                    common_start, common_end
                ),
                'datetime_UTC'
            ]
        ),
        'generation': set(
            generation.loc[
                generation['datetime'].between(
                    common_start, common_end
                ),
                'datetime'
            ]
        )
    }

    # reference: all timestamps observed in at least one dataset
    all_timestamps = set().union(*timestamp_sets.values())

    print('\n--- TIMESTAMP ALIGNMENT ---')

    # check which timestamps are absent from each dataset
    all_aligned = True

    for name, timestamps in timestamp_sets.items():
        missing_timestamps = all_timestamps - timestamps
        print(f'{name}: {len(timestamps)} timestamps')
        print(
            f'Missing from {name}: '
            f'{len(missing_timestamps)}'
        )

        if missing_timestamps:
            all_aligned = False
            print(
                'Examples:',
                sorted(missing_timestamps)[:5]
            )

    if all_aligned:
        print('MSG: timestamp alignment passed')
    else:
        print('WARNING: timestamp misalignment detected')

    return all_aligned


# MAIN VALIDATION ORCHESTRATOR
def check_compatibility(prices, load, generation):
    '''
    Verifies the global compatibility among prices, load and 
    generation datasets
    '''
    # timestamps validity and uniqueness
    check_unique_timestamps(load, 'datetime_UTC', 'load')
    check_unique_timestamps(prices, 'datetime_UTC', 'prices')
    check_unique_timestamps(generation, 'datetime', 'generation')

    # timezone and time coverage
    check_timezone(prices, load, generation)
    check_time_span(prices, load, generation)

    # alignment and hourly continuity
    check_frequency(prices, load, generation)
    check_timestamp_alignment(prices, load, generation)

    print('\nMSG: dataset compatibility check completed')


# DATASET BUILDERS / MERGERS
def build_national_dataset(prices, load, generation):
    '''
    Creates the dataset for national aggregated dataset 
    '''
    # select relevant columns from each dataframe
    prices_df = prices[['datetime_UTC', 'Italia']].copy()
    load_df = load[['datetime_UTC', 'Totale Italia']].copy()
    generation_df = generation.copy()

    # rename columns
    prices_df = prices_df.rename(columns={'Italia': 'PUN'})
    load_df = load_df.rename(columns={'Totale Italia': 'National Load'})
    generation_df = generation_df.rename(columns={'datetime': 'datetime_UTC'})

    # merge prices and load keeping all price timestamps
    national = prices_df.merge(
        load_df, 
        on='datetime_UTC', 
        how='left',
        validate='one_to_one'
    )
    
    # add generation preserving the price timeline
    national = national.merge(
        generation_df, 
        on='datetime_UTC', 
        how='left',
        validate='one_to_one'
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

def build_zonal_dataset(prices, load, generation, zone, mappings):
    '''
    Creates the dataset for zonal datasets
    '''
    # get GME bidding zone name
    bz_name = mappings[f'{zone}']

    # select relevant columns from each dataframe
    prices_df = prices[['datetime_UTC', f'{bz_name}']].copy()
    load_df = load[['datetime_UTC', f'{bz_name}']].copy()
    generation_df = generation.copy()

    # rename columns
    prices_df = prices_df.rename(columns={f'{bz_name}': f'PZ_{zone}'})
    load_df = load_df.rename(columns={f'{bz_name}': f'Load_{zone}'})
    generation_df = generation_df.rename(columns={'datetime': 'datetime_UTC'})

    # merge prices and load keeping all price timestamps
    zonal = prices_df.merge(
        load_df, 
        on='datetime_UTC', 
        how='left',
        validate='one_to_one'
    )
    
    # add generation preserving the price timeline
    zonal = zonal.merge(
        generation_df, 
        on='datetime_UTC', 
        how='left',
        validate='one_to_one'
    )

    # get local hour from local datetime --> for analysis purposes
    zonal['datetime_local'] = (
        zonal['datetime_UTC']
        .dt.tz_convert('Europe/Rome')
    )
    zonal['local_hour'] = zonal['datetime_local'].dt.hour

    # reorder columns
    base_columns = [
        'datetime_UTC',
        'datetime_local',
        'local_hour',
        f'PZ_{zone}',
        f'Load_{zone}'
    ]
    generation_columns = [
        col for col in zonal.columns
        if col not in base_columns
    ]
    zonal = zonal[
        base_columns + generation_columns
    ]

    print(zonal.head())
    print(zonal.columns.tolist())

    return zonal


# EXPORT
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


# EXECUTION
'''
# national case
generation = load_clean_data(clean_data_path, 'generation', COUNTRY_CODE)
prices = load_clean_data(clean_data_path, 'prices', None)
load = load_clean_data(clean_data_path, 'load', None)
check_compatibility(prices, load, generation)
national_df = build_national_dataset(prices, load, generation)

export_processed_dataset(national_df, COUNTRY_CODE)
'''

# zonal case
prices = load_clean_data(clean_data_path, 'prices', None)
load = load_clean_data(clean_data_path, 'load', None)

for zone in ZONES:
    generation = load_clean_data(clean_data_path, 'generation', zone)
    check_compatibility(prices, load, generation)
    zonal_df = build_zonal_dataset(prices, load, generation,zone, ZONE_MAPPING)
    export_processed_dataset(zonal_df, zone)