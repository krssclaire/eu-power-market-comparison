'''
This script contains all user inputs variables necessary
> For specific country codes and timezones visit: https://github.com/EnergieID/entsoe-py/blob/master/entsoe/mappings.py
'''
from pathlib import Path

# variable for global project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# variables for ENTSO-E API requests
START_DATE = '20150101'
END_DATE = '20150115' 
COUNTRY_CODE = 'IT'
TIMEZONE = 'Europe/Rome'
ZONES = [
    'IT_NORD'
    #'IT_CNOR',
    #'IT_CSUD',
    #'IT_SUD',
    #'IT_CALA',
    #'IT_SICI',
    #'IT_SARD'
]

# other
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
print('msg: "config.py" executed')