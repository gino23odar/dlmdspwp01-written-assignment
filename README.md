# DLMDSPWP01 Assignment - project files

Implementation of the official Programming with Python written assignment for the DLMDSPWP01 course.

## Overview

The application processes the training, ideal function and test datasets provided for this assignment.

The workflow consists of the following steps:

1. Loading and validating the provided CSV datasets
2. Storing training data and ideal functions in SQLite
3. Selecting an ideal function for each training fucntion by minimizing the sum of squared y-error
4. Calculating the max deviation between training func and selected ideal func
5. Using max deviation * sqrt(2) as the threshold for mapping observations
6. Mapping qualifying test observations to the closest valid selected ideal func
7. Storing mappings and deviations in SQLite
8. Interactive Bokeh visualization generation
9. Running unit and integration tests for the entire pipeline

## Requirements

- Python 3.12
- pandas
- pathlib
- SQLAlchemy
- Bokeh

## Installation

After creating a Python venv:
 
>    On windows: 
    `
    py -3.12 -m venv .venv
    .venv\Scripts\Activate.ps1
    `

>   ...install dependencies:
    `powershell
    pip install -r requirements.txt
    `

## Input Data

Place the provided course datasets in (not included in the repo as instructed):

    data/
        train.csv
        ideal.csv
        test.csv



## Running the Application

Run:

```powershell
python main.py
```

It should generate:

```text
output/
    assignment.db
    visualization.html
```

DB should contain:

```text
training_data
ideal_functions
test_results
```

The test-results table stores:

```text
x
y
delta_y
ideal_function
```
## Running the tests:

```powershell
python -m unittest discover -s tests -v
```

## Project Structure

```text
dlmdspwp01-written-assignment/
│
├── data/
│   ├── train.csv
│   ├── ideal.csv
│   └── test.csv
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── exceptions.py
│   ├── loaders.py
│   ├── mapper.py
│   ├── selector.py
│   └── visualizer.py
│
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_integration.py
│   ├── test_loaders.py
│   ├── test_mapper.py
│   ├── test_selector.py
│   └── test_visualizer.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
