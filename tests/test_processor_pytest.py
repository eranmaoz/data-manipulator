import os
import pytest
import json
from json_processor.processor import DataProcessor


# Fixture to create JSON files with given data
@pytest.fixture
def create_json(tmp_path):
    def _create_json(data, filename, invalid=False):
        file_path = tmp_path / filename
        with file_path.open('w') as file:
            if invalid:
                file.write(data)
            else:
                json.dump(data, file)
        return file_path

    return _create_json


@pytest.fixture
def load_100_values_file_test_data():
    # Relative path from the test file to the data directory
    file_path = os.path.join(os.path.dirname(__file__), '../data/100_values.json')
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")

    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# Test for processing valid JSON data
def test_basic_data_processing(create_json, tmp_path):
    data = {
        "date": "1999/10/10 10:15:15",
        "text": "sdfg fgfgf ffgfgrrrt sdfgsdf bmbmbmbp",
        "list": ["bar", "baz", "foo", "bar", "baz", 5]
    }
    valid_json = create_json(data, "valid.json")

    output_file_path = tmp_path / "processed.json"
    processor = DataProcessor(valid_json)
    processor.process_data()
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["date"] == "2021/10/10 10:15:15"
    assert processed_data["text"] == "pbmbmbmbfdsgfdstrrrgfgfffgfgfgfds"
    assert processed_data["list"] == ["bar", "baz", "foo", 5]


# Test for handling invalid JSON data
def test_invalid_json_handling(create_json, tmp_path, capsys):
    invalid_json = create_json("{invalid_json: true}", "invalid.json", invalid=True)

    output_file_path = tmp_path / "processed_invalid.json"
    processor = DataProcessor(invalid_json)
    processor.process_data()
    processor.save_processed_data(output_file_path)

    captured = capsys.readouterr()
    print(captured.out)  # Print captured output to the console

    assert "Bad input" in captured.out

    with output_file_path.open('r') as file:
        processed_data = json.load(file)
    assert processed_data == {}


# Test for processing empty JSON data
def test_empty_json(create_json, tmp_path):
    empty_data = {}
    empty_json_path = create_json(empty_data, "empty.json")

    processor = DataProcessor(empty_json_path)
    processor.process_data()
    output_file_path = tmp_path / "processed_empty.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data == {}


# Test for changing date format
def test_datetime_format_change(create_json, tmp_path):
    data = {
        "date": "2023/12/25 15:30:00",
        "other_date": "2021/01/01 12:00:00"
    }
    datetime_json = create_json(data, "datetime.json")

    processor = DataProcessor(datetime_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_datetime.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["date"] == "2021/12/25 15:30:00"
    assert processed_data["other_date"] == "2021/01/01 12:00:00"


# Test for string reversal and whitespace removal
def test_string_reverse_and_whitespace_removal(create_json, tmp_path):
    data = {
        "text": " ab cd ef "
    }
    text_json = create_json(data, "text.json")

    processor = DataProcessor(text_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_text.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["text"] == "fedcba"


# Test for removing duplicates from lists
def test_list_duplicates_removal(create_json, tmp_path):
    data = {
        "list": ["apple", "banana", "apple", "orange"]
    }
    list_json = create_json(data, "list.json")

    processor = DataProcessor(list_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_list.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["list"] == ["apple", "banana", "orange"]


def test_multiple_list_duplicates_removal(create_json, tmp_path):
    data = {
        "list": ["banana", "apple", "banana","banana","banana","banana","banana", "apple", "orange", "banana"]
    }
    list_json = create_json(data, "list.json")

    processor = DataProcessor(list_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_list.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["list"] == ["banana", "apple","orange"]

# Test for removing duplicates from lists
def test_list_preserves_case_sensitivity_and_duplicates(create_json, tmp_path):
    data = {
        "list": ["Apple", "banana", "apple", "orange", "orange"]
    }
    list_json = create_json(data, "list.json")

    processor = DataProcessor(list_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_list.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["list"] == ["Apple", "banana", "apple", "orange"]


# Test for data that needs no processing
def test_no_processing_needed(create_json, tmp_path):
    data = {
        "date": "2021/12/25 15:30:00",
        "list": ["unique", "values", 1, 2, 3]
    }
    no_processing_json = create_json(data, "date_processing.json")

    processor = DataProcessor(no_processing_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_date_processing.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["date"] == "2021/12/25 15:30:00"
    assert processed_data["list"] == ["unique", "values", 1, 2, 3]


def test_extended_invalid_json_handling(create_json, tmp_path, capsys):
    extended_invalid_json = create_json("""
    {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "address": {
            "street": "123 Elm St",
            "city": "Somewhere",
            "zip": 12345,
        },
        "phone_numbers": [1234567890, "0987654321"],
        "invalid_field": unquoted_value,
        "extra_data": {
            "key1": "value1",
            "key2": "value2"
            // Missing closing brace
        }
    }
    """, "extended_invalid.json", invalid=True)

    output_file_path = tmp_path / "processed_extended_invalid.json"
    processor = DataProcessor(extended_invalid_json)
    processor.process_data()
    processor.save_processed_data(output_file_path)

    captured = capsys.readouterr()
    print(captured.out)  # Print captured output to the console

    assert "Bad input" in captured.out

    with output_file_path.open('r') as file:
        processed_data = json.load(file)
    assert processed_data == {}


def test_various_data_types(create_json, tmp_path):
    data = {
        "null_value": None,
        "boolean_true": True,
        "boolean_false": False,
        "integer": 123,
        "float": 123.45,
        "list": ["A", "B", "C", "A"]
    }
    types_json = create_json(data, "types.json")

    processor = DataProcessor(types_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_types.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["null_value"] is None
    assert processed_data["boolean_true"] == True
    assert processed_data["boolean_false"] == False
    assert processed_data["integer"] == 123
    assert processed_data["float"] == 123.45
    assert processed_data["list"] == ["A", "B", "C"]


def test_file_with_special_characters(create_json, tmp_path):
    data = {
        "special_chars": "#%^&*()",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }
    special_chars_json = create_json(data, "special_chars.json")

    processor = DataProcessor(special_chars_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_special_chars.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["special_chars"] == ")(*&^%#"


def test_empty_lists_and_dicts(create_json, tmp_path):
    data = {
        "empty_list": [],
        "empty_dict": {},
        "non_empty_list": [1, 2, 3],
        "non_empty_dict": {"key": "value"},
        "text": "abcd"
    }
    empty_data_json = create_json(data, "empty_data.json")

    processor = DataProcessor(empty_data_json)
    processor.process_data()
    output_file_path = tmp_path / "processed_empty_data.json"
    processor.save_processed_data(output_file_path)

    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    assert processed_data["empty_list"] == []
    assert processed_data["empty_dict"] == {}
    assert processed_data["non_empty_list"] == [1, 2, 3]
    assert processed_data["non_empty_dict"] == {"key": "value"}
    assert processed_data["text"] == "dcba"


def test_data_processing_for_100_values_file(load_100_values_file_test_data, tmp_path):
    # Load the data from the fixture
    data = load_100_values_file_test_data
    valid_json_path = tmp_path / "100_values.json"

    # Save the loaded data to a temporary file
    with valid_json_path.open('w') as file:
        json.dump(data, file)

    output_file_path = tmp_path / "processed_data.json"

    # Initialize DataProcessor with the temporary file path
    processor = DataProcessor(valid_json_path)
    processor.process_data()
    processor.save_processed_data(output_file_path)

    # Read the processed data
    with output_file_path.open('r') as file:
        processed_data = json.load(file)

    # Assert processed data
    assert_100_values_processed_data(processed_data)

    project_output_path = os.path.join(os.path.dirname(__file__), 'processed_data.json')
    os.rename(output_file_path, project_output_path)


def assert_100_values_processed_data(processed_data):
    assert processed_data["value1"] == "2021/10/10 10:15:15"
    assert processed_data["value2"] == "pbmbmbmbfdsgfdstrrrgfgfffgfgfgfds"
    assert processed_data["value3"] == ["bar", "baz", "foo", 5]
    assert processed_data["value4"] == "2021/10/10 10:15:15"
    assert processed_data["value5"] == "5eulavelpmaxe"
    assert processed_data["value6"] == "6eulavelpmaxerehtona"
    assert processed_data["value7"] == [1, 2, 3, 4, 5]
    assert processed_data["value8"] == "2021/01/01 01:01:01"
    assert processed_data["value97"] == ["melon", "berry", "peach"]
    assert processed_data["value98"] == "2021/04/04 04:04:04"
    assert processed_data["value99"] == "99eulavroftxetlanif"
    assert processed_data["value100"] == "derdnuhenoeulav"
