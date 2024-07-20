import unittest
import json
from pathlib import Path
from json_processor.processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "date": "1999/10/10 10:15:15",
            "text": "sdfg fgfgf ffgfgrrrt sdfgsdf bmbmbmbp",
            "list": ["bar", "baz", "foo", "bar", "baz", 5]
        }
        self.invalid_data = "{invalid_json: true}"

        self.valid_file_path = Path("valid.json")
        self.invalid_file_path = Path("invalid.json")

        with self.valid_file_path.open('w') as file:
            json.dump(self.valid_data, file)

        with self.invalid_file_path.open('w') as file:
            file.write(self.invalid_data)

    def tearDown(self):
        self.valid_file_path.unlink(missing_ok=True)
        self.invalid_file_path.unlink(missing_ok=True)

    def test_data_processing(self):
        processor = DataProcessor(self.valid_file_path)
        processor.process_data()
        output_file_path = Path("processed.json")
        processor.save_processed_data(output_file_path)

        with output_file_path.open('r') as file:
            processed_data = json.load(file)

        self.assertEqual(processed_data["date"], "2021/10/10 10:15:15")
        self.assertEqual(processed_data["text"], "pbmbmbmbfdsgfdstrrrgfgfffgfgfgfds")
        self.assertEqual(processed_data["list"], ["bar", "baz", "foo", 5])

        output_file_path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()