# eu-power-market-comparison

Relationship between the electricity price and the renewable generation.  
Italian case study and its bidding zones.

Notes:
* ENTSO-E data is in real-time
  Link: https://www.entsoe.eu/data/power-stats/ 
* TERNA and GME Load definitions are different
  Link: https://gme.mercatoelettrico.org/it-it/Home/Glossario

## Project Structure
```
eu-power-market-comparison/
│
├── dataset/
│   ├── raw/
│   │   ├── entsoe/
│   │   │    └── generation/
│   │   │           ├── IT/
│   │   │           |    ├── IT-2015-generation.csv
│   │   │           |    ├── IT-2016-generation.csv
│   │   │           |    ├── IT-2017-generation.csv
│   │   │           |    ├── IT-2018-generation.csv
│   │   │           |    ├── IT-2019-generation.csv
│   │   │           |    ├── IT-2020-generation.csv
│   │   │           |    ├── IT-2021-generation.csv
│   │   │           |    ├── IT-2022-generation.csv
│   │   │           |    ├── IT-2023-generation.csv
│   │   │           |    ├── IT-2024-generation.csv
│   │   │           |    ├── IT-2025-generation.csv
│   │   │           |    └── IT-2026-generation.csv
│   │   │           ├── IT_CALA/
│   │   │           |    ├── IT_CALA-2021-generation.csv
│   │   │           |    ├── IT_CALA-2022-generation.csv
│   │   │           |    ├── IT_CALA-2023-generation.csv
│   │   │           |    ├── IT_CALA-2024-generation.csv
│   │   │           |    ├── IT_CALA-2025-generation.csv
│   │   │           |    └── IT_CALA-2026-generation.csv
│   │   │           ├── IT_CNOR/
│   │   │           |    ├── IT_CNOR-2015-generation.csv
│   │   │           |    ├── IT_CNOR-2016-generation.csv
│   │   │           |    ├── IT_CNOR-2017-generation.csv
│   │   │           |    ├── IT_CNOR-2018-generation.csv
│   │   │           |    ├── IT_CNOR-2019-generation.csv
│   │   │           |    ├── IT_CNOR-2020-generation.csv
│   │   │           |    ├── IT_CNOR-2021-generation.csv
│   │   │           |    ├── IT_CNOR-2022-generation.csv
│   │   │           |    ├── IT_CNOR-2023-generation.csv
│   │   │           |    ├── IT_CNOR-2024-generation.csv
│   │   │           |    ├── IT_CNOR-2025-generation.csv
│   │   │           |    └── IT_CNOR-2026-generation.csv
│   │   │           ├── IT_CSUD/
│   │   │           |    ├── IT_CSUD-2015-generation.csv
│   │   │           |    ├── IT_CSUD-2016-generation.csv
│   │   │           |    ├── IT_CSUD-2017-generation.csv
│   │   │           |    ├── IT_CSUD-2018-generation.csv
│   │   │           |    ├── IT_CSUD-2019-generation.csv
│   │   │           |    ├── IT_CSUD-2020-generation.csv
│   │   │           |    ├── IT_CSUD-2021-generation.csv
│   │   │           |    ├── IT_CSUD-2022-generation.csv
│   │   │           |    ├── IT_CSUD-2023-generation.csv
│   │   │           |    ├── IT_CSUD-2024-generation.csv
│   │   │           |    ├── IT_CSUD-2025-generation.csv
│   │   │           |    └── IT_CSUD-2026-generation.csv
│   │   │           ├── IT_NORD/
│   │   │           |    ├── IT_NORD-2015-generation.csv
│   │   │           |    ├── IT_NORD-2016-generation.csv
│   │   │           |    ├── IT_NORD-2017-generation.csv
│   │   │           |    ├── IT_NORD-2018-generation.csv
│   │   │           |    ├── IT_NORD-2019-generation.csv
│   │   │           |    ├── IT_NORD-2020-generation.csv
│   │   │           |    ├── IT_NORD-2021-generation.csv
│   │   │           |    ├── IT_NORD-2022-generation.csv
│   │   │           |    ├── IT_NORD-2023-generation.csv
│   │   │           |    ├── IT_NORD-2024-generation.csv
│   │   │           |    ├── IT_NORD-2025-generation.csv
│   │   │           |    └── IT_NORD-2026-generation.csv
│   │   │           ├── IT_SUD/
│   │   │           |    ├── IT_SUD-2015-generation.csv
│   │   │           |    ├── IT_SUD-2016-generation.csv
│   │   │           |    ├── IT_SUD-2017-generation.csv
│   │   │           |    ├── IT_SUD-2018-generation.csv
│   │   │           |    ├── IT_SUD-2019-generation.csv
│   │   │           |    ├── IT_SUD-2020-generation.csv
│   │   │           |    ├── IT_SUD-2021-generation.csv
│   │   │           |    ├── IT_SUD-2022-generation.csv
│   │   │           |    ├── IT_SUD-2023-generation.csv
│   │   │           |    ├── IT_SUD-2024-generation.csv
│   │   │           |    ├── IT_SUD-2025-generation.csv
│   │   │           |    └── IT_SUD-2026-generation.csv
│   │   │           ├── IT_SARD/
│   │   │           |    ├── IT_SARD-2015-generation.csv
│   │   │           |    ├── IT_SARD-2016-generation.csv
│   │   │           |    ├── IT_SARD-2017-generation.csv
│   │   │           |    ├── IT_SARD-2018-generation.csv
│   │   │           |    ├── IT_SARD-2019-generation.csv
│   │   │           |    ├── IT_SARD-2020-generation.csv
│   │   │           |    ├── IT_SARD-2021-generation.csv
│   │   │           |    ├── IT_SARD-2022-generation.csv
│   │   │           |    ├── IT_SARD-2023-generation.csv
│   │   │           |    ├── IT_SARD-2024-generation.csv
│   │   │           |    ├── IT_SARD-2025-generation.csv
│   │   │           |    └── IT_SARD-2026-generation.csv
│   │   │           └── IT_SICI/
│   │   │                ├── IT_SICI-2015-generation.csv
│   │   │                ├── IT_SICI-2016-generation.csv
│   │   │                ├── IT_SICI-2017-generation.csv
│   │   │                ├── IT_SICI-2018-generation.csv
│   │   │                ├── IT_SICI-2019-generation.csv
│   │   │                ├── IT_SICI-2020-generation.csv
│   │   │                ├── IT_SICI-2021-generation.csv
│   │   │                ├── IT_SICI-2022-generation.csv
│   │   │                ├── IT_SICI-2023-generation.csv
│   │   │                ├── IT_SICI-2024-generation.csv
│   │   │                ├── IT_SICI-2025-generation.csv
│   │   │                └── IT_SICI-2026-generation.csv
│   │   ├── gme/
│   │   |    ├── load/
│   │   |    │      ├── GME-load-2015.xlsx
│   │   |    │      ├── GME-load-2016.xlsx
│   │   |    │      ├── GME-load-2017.xlsx
│   │   |    │      ├── GME-load-2018.xlsx
│   │   |    │      ├── GME-load-2019.xlsx
│   │   |    │      ├── GME-load-2020.xlsx
│   │   |    │      ├── GME-load-2021.xlsx
│   │   |    │      ├── GME-load-2022.xlsx
│   │   |    │      ├── GME-load-2023.xlsx
│   │   |    │      ├── GME-load-2024.xlsx
│   │   |    │      ├── GME-load-2025.xlsx
│   │   |    │      └── GME-load-2026.xlsx
│   │   |    └── prices/
│   │   |           ├── PUN/
│   │   |           |     ├── GME-PUNi-2015.xlsx
│   │   |           |     ├── GME-PUNi-2016.xlsx
│   │   |           |     ├── GME-PUNi-2017.xlsx
│   │   |           |     ├── GME-PUNi-2018.xlsx
│   │   |           |     ├── GME-PUNi-2019.xlsx
│   │   |           |     ├── GME-PUNi-2020.xlsx
│   │   |           |     ├── GME-PUNi-2021.xlsx
│   │   |           |     ├── GME-PUNi-2022.xlsx
│   │   |           |     ├── GME-PUNi-2023.xlsx
│   │   |           |     ├── GME-PUNi-2024.xlsx
│   │   |           |     ├── GME-PUNi-2025.xlsx
│   │   |           |     └── GME-PUNi-2026.xlsx
│   │   |           └──  PZ/
│   │   |                 ├── GME-PZ-2015.xlsx
│   │   |                 ├── GME-PZ-2016.xlsx
│   │   |                 ├── GME-PZ-2017.xlsx
│   │   |                 ├── GME-PZ-2018.xlsx
│   │   |                 ├── GME-PZ-2019.xlsx
│   │   |                 ├── GME-PZ-2020.xlsx
│   │   |                 ├── GME-PZ-2021.xlsx
│   │   |                 ├── GME-PZ-2022.xlsx
│   │   |                 ├── GME-PZ-2023.xlsx
│   │   |                 ├── GME-PZ-2024.xlsx
│   │   |                 ├── GME-PZ-2025.xlsx
│   │   |                 └── GME-PZ-2026.xlsx
|   |   └── terna/
|   |         └── generation
|   |                 └── TERNA-generation-test.xlsx
│   ├── clean/
│   │   ├── generation/
|   |   |     ├── IT_CALA-generation.csv
|   |   |     ├── IT_CNOR-generation.csv
|   |   |     ├── IT_CSUD-generation.csv
|   |   |     ├── IT_NORD-generation.csv
|   |   |     ├── IT_SARD-generation.csv
|   |   |     ├── IT_SICI-generation.csv
|   |   |     ├── IT_SUD-generation.csv
|   |   |     └── IT-generation.csv
│   │   ├── load/
|   |   |     └── load-clean.csv
│   │   ├── prices/
|   |   |   ├── pun-index-clean.csv
|   |   |   └── zonal-prices-clean.csv
│   │   └── it_merged-dataset.csv
|   | 
│   ├── filled/
│   │   └── IT.csv
│   │
│   └── processed/
│       └── IT.csv
│
├── scripts/
│   ├── __init__.py
│   ├── build_dataset.py
│   ├── cleaning_utils.py
│   ├── config.py
│   ├── download.py
│   ├── generation_cleaner.py
│   ├── validation.py
│   └── readme.md
│
├── notebooks/
│   ├── 00-0_data-cleaning-eda.ipynb
│   ├── 00-1_prices-cleaner.ipynb
│   ├── 00-2_load-cleaner.ipynb
│   ├── 00-3_data-filler.ipynb
│   ├── 01-0_italy.ipynb
│   ├── 01-1_italy-extended.ipynb
│   └── ...
│
└── README.md
```