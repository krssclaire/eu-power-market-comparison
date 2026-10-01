'''
This script contains all user inputs variables necessary for the ENTSO-E API request
> For specific country codes and timezones visit: https://github.com/EnergieID/entsoe-py/blob/master/entsoe/mappings.py
'''

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

print('msg: "config.py" executed')