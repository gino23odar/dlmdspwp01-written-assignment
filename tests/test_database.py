import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def test_save_and_read_dataframe(self):
        with tempfile.TemporaryDirectory() as directory:

            database = DatabaseManager(
                Path(directory) / "test.db"
            )

            try:
                original = pd.DataFrame(
                    {
                        "x": [1.0, 2.0],
                        "y": [3.0, 4.0],
                    }
                )

                database.save_dataframe(
                    original,
                    "sample",
                )

                self.assertTrue(
                    database.table_exists("sample")
                )

                loaded = database.read_table(
                    "sample"
                )

                pd.testing.assert_frame_equal(
                    original,
                    loaded,
                )

            finally:
                database.close()


if __name__ == "__main__":
    unittest.main()