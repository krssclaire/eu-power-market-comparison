'''
This script contains all user inputs variables necessary
> For specific country codes and timezones visit: https://github.com/EnergieID/entsoe-py/blob/master/entsoe/mappings.py
'''
from pathlib import Path

# variable for global project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# variables for ENTSO-E API requests
START_YEAR = 2015
END_YEAR = 2026
COUNTRY_CODE = 'IT'
TIMEZONE = 'Europe/Rome'
ZONES = [
    'IT_NORD',
    'IT_CNOR',
    'IT_CSUD',
    'IT_SUD',  # no MultiIndex for download
    'IT_CALA', # no MultiIndex for downlaad
    'IT_SICI',
    'IT_SARD'
]

# other
YEARS = range(START_YEAR, END_YEAR + 1)

GENERATION_TYPES = {
    'solar': 'Solar',
    'wind': 'Wind Onshore',
    'hydro_run_of_river': 'Hydro Run-of-river and pondage',
    'hydro_reservoir': 'Hydro Water Reservoir',
    'hydro_pumped': 'Hydro Pumped Storage',
    'gas': 'Fossil Gas',
    'coal': 'Fossil Hard coal',
    'oil': 'Fossil Oil',
}

# terminal message for user
print('MSG: "config.py" executed')