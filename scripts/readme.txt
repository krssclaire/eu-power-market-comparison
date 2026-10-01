Scripts plan:
* config.py
* download.py               /raw/entose
    clean_prices.py         /clean
    clean_load.py
    clean-generation.py
    validate.py
    build_dataset.py




RAW DATA
   ↓
1. Load raw file
   ↓
2. Inspect dimensions
   ↓
3. Inspect MultiIndex
   ↓
4. Standardize datetime
   ↓
5. Remove duplicated observations
   ↓
6. Handle missing values
   ↓
7. Standardize column names
   ↓
8. Validate frequency
   ↓
9. Save cleaned dataset