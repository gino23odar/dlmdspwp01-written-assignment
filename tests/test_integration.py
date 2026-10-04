import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.database import DatabaseManager
from src.mapper import TestPointMapper
from src.selector import IdealFunctionSelector

class TestAssignmentWorkflow(unittest.TestCase):
    # test integration of independent components

    def test_selection_mapping_and_database_storage(self):
        training = pd.DataFrame({"x": [0.0, 1.0, 2.0], "y1": [1.0, 2.0, 3.0]})
        ideal = pd.DataFrame({"x": [0.0, 1.0, 2.0], "y1": [10.0, 20.0, 30.0], "y2": [1.0, 2.0, 3.1]})
        test = pd.DataFrame({"x": [0.0, 1.0], "y": [1.05, 5.0]})

        selection = IdealFunctionSelector(training, ideal).select()
        self.assertEqual(selection[0].ideal_func, "y2")

        mapped = TestPointMapper(ideal, selection).map_points(test)
        self.assertEqual(len(mapped), 1)

        with tempfile.TemporaryDirectory() as directory:
            database = DatabaseManager(Path(directory)/"integration.db")

            try:
                database.save_dataframe(mapped, "test_results")
                stored = database.read_table("test_results")

                self.assertEqual(len(stored), 1)

                self.assertEqual(int(stored.iloc[0]["ideal_func"]), 2)

                self.assertAlmostEqual(stored.iloc[0]["delta_y"], 0.05)

            finally:
                database.close()

if __name__ == "__main__":
    unittest.main()


