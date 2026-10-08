# The scripts folder
This is a collection of the scripts used for downloading data, data cleaning, validation and merge process.
Scripts name and order execution are described as follows.

| N°| Scripts plan             | Status      | Desciption / Functionality |
|---|--------------------------|-------------|----------------------------|
| 1 | `config.py`              | complete    | Edit downloader and generation data cleaner parameters
| 2 | `download.py`            | complete    | Download raw data from ENTSO-E Transparency Platform through API
| X | `cleaning_utils.py`      | deprecated* | [Contained general function useful for data cleaning]
| 3 | `prices_cleaner.py`      | deprecated* | [This script has been substituted by ipynb file]
| 4 | `load_cleaner.py`        | deprecated* | [This script has been substituted by ipynb file]
| 5 | `generation_cleaner.py`  | complete    | Clean ENTSO generation datasets
| 6 | `validation.py`          | complete    | Checks the single dataset validity for the next step
| 7 | `build_dataset.py`       |  WIP        | Checks all dataset for merging

> Note: deprecated Python scripts marked by (*) have been deprecated following to the decision of usnig GME sources for load and prices variables, due to the mosre complete and quality data.