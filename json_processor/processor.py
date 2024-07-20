import json
from datetime import datetime
from pathlib import Path


class DataProcessor:
    def __init__(self, input_file_path: Path):
        self.input_file_path = input_file_path
        self.data = self._read_json()

    def _read_json(self):
        try:
            with self.input_file_path.open('r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Bad input")
            return {}

    def process_data(self):
        print("\nBefore processing:", json.dumps(self.data, indent=4))  # Add newline before printing

        def _handle_value_transformation(value):
            if isinstance(value, str):
                try:
                    # Attempt to parse value as a datetime
                    dt = datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
                    # Change the year to 2021 and format it back to the same datetime string format
                    return dt.replace(year=2021).strftime("%Y/%m/%d %H:%M:%S")
                except ValueError:
                    # If it's not a valid datetime, remove all whitespaces and reverse the string
                    return ''.join(value.split()).strip()[::-1]
            elif isinstance(value, list):
                # If it's a list, remove duplicates while preserving the order
                return list(dict.fromkeys(value))
            # Return the value unchanged if it's not a string or a list
            return value

        # Apply _handle_value_transformation function to each key-value pair in self.data dictionary
        self.data = {k: _handle_value_transformation(v) for k, v in self.data.items()}

        print("\nAfter processing:", json.dumps(self.data, indent=4))  # Add newline before printing

    def save_processed_data(self, output_file_path: Path):
        with output_file_path.open('w') as file:
            json.dump(self.data, file, indent=4)


def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m data_processor <input_file> <output_file>")
        return
    input_file_path = Path(sys.argv[1])
    output_file_path = Path(sys.argv[2])
    processor = DataProcessor(input_file_path)
    processor.process_data()
    processor.save_processed_data(output_file_path)


if __name__ == "__main__":
    main()