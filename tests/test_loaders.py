import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.exceptions import DataLoadError, DataValidationError
from src.loaders import CSVDataLoader

class TestDataLoader(unittest.TestCase):

    def test_load_valid_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data.csv"

            pd.DataFrame({"x": [1.0, 2.0], "y": [3.0, 4.0]}).to_csv(path, index=False)

            loader = CSVDataLoader(path, ["x", "y"])
            result = loader.load()

            self.assertEqual(len(result), 2)

    def test_missing_file_raises_data_load_error(self):
        loader = CSVDataLoader("non_existent_file.csv", ["x", "y"])
        with self.assertRaises(DataLoadError):
            loader.load()

    def test_missing_columns_raises_validation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data.csv"
            pd.DataFrame({"x": [1.0]}).to_csv(path, index=False)

            loader = CSVDataLoader(path, ["x", "y"])
            with self.assertRaises(DataValidationError):
                loader.load()

if __name__ == "__main__":
    unittest.main()