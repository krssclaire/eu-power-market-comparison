'''
This script downloads data retrieved from the ENTSO API and stores it into the /raw subfolders based on the type of data (prices, 
generation, load).
> Note: Line 40-41 are to comment/uncomment based on the zone. Some have aggregated generation results which requires the uncomments of 
        those lines, while others don't and will produce a MultiIndex error. 
'''

# import libraries
from entsoe import EntsoePandasClient
from dotenv import load_dotenv
import os
import pandas as pd
from pathlib import Path
from scripts import config
import time

# script start time execution
start = time.time()

# access entsoe data through protected API_KEY
load_dotenv()
API_KEY = os.getenv('ENTSOE_API_KEY')       # get ENTSOE_API_KEY from ".env"
client = EntsoePandasClient(api_key=API_KEY)

# user editable input
start = pd.Timestamp(config.START_DATE, tz=config.TIMEZONE)
end = pd.Timestamp(config.END_DATE, tz=config.TIMEZONE)
country_codes = config.ZONES   

# define raw dataset folder path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
raw_dataset_path = PROJECT_ROOT / 'dataset' / 'raw' / 'entsoe'

for country_code in country_codes:
    # get data in Pandas DF
    prices = client.query_day_ahead_prices(country_code, start=start, end=end)
    print(f'{country_code} PRICES data retrieved')
    
    load = client.query_load(country_code, start=start, end=end)
    print(f'{country_code} LOAD data retrieved')
    generation = client.query_generation(country_code, start=start, end=end)
    print(f'{country_code} GENERATION data retrieved')
    
    # keep only actual aggregated generation --> comment for non Multiindex aggregation datasets
    # generation = generation.xs("Actual Aggregated", axis=1, level=1)
    #print(f'{country_code} GENERATION Actual Aggregated kept')

    # save locally to csv
    prices.to_csv(f'{raw_dataset_path}/prices/{country_code}-prices.csv')
    print(f'Saved {country_code} PRICES data into{raw_dataset_path}')
    load.to_csv(f'{raw_dataset_path}/load/{country_code}-load.csv')
    print(f'Saved {country_code} LOAD data into{raw_dataset_path}')
    generation.to_csv(f'{raw_dataset_path}/generation/{country_code}-generation.csv')
    print(f'Saved {country_code} GENERATION data into{raw_dataset_path}')

# SCRIPT PERFORMANCE --> time should depend on the amount of data retrieved
end = time.time()
print(f'Execution time: {end - start}')