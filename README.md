# JSON Data Transformer

This project provides a `DataProcessor` class to process and transform JSON data.

## Features

- Read JSON data from a file
- Process data:
    - Modify datetime values (change the year to 2021)
    - Reverse strings and remove whitespace
    - Remove duplicates from lists
- Save processed data to a new JSON file

## Requirements

- Python 3.10+
- `pytest` (for running tests)

## Installation

```sh
pip install -r requirements.txt