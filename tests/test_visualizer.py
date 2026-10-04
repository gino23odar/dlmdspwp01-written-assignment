import tempfile
import unittest

from pathlib import Path

import pandas as pd

from src.selector import SelectionResult
from src.visualizer import AssignmentVisualizer

class TestAssignmentVisualizer(unittest.TestCase):
    def test_create_gen_html_file(self):
        training = pd.DataFrame({"x": [0.0, 1.0], "y1": [1.0, 2.0]})
        ideal = pd.DataFrame({"x": [0.0, 1.0], "y1": [1.0, 2.0]})
        test = pd.DataFrame({"x": [0.0], "y": [1.0]})
        mapped = pd.DataFrame({"x": [0.0], "y": [1.0], "ideal_func": [1], "delta_y": [0.0]})

        selections = [
            SelectionResult(
                training_func="y1",
                ideal_func="y1",
                sse=0.0,
                max_deviation=0.0,
                threshold=0.1,
            )
        ]

        with tempfile.TemporaryDirectory() as directory:

            output_path = Path(directory) / "visualization.html"

            result = AssignmentVisualizer(output_path).create(training, ideal, test, mapped, selections)

            self.assertTrue(output_path.exists())
            self.assertGreater(result.stat().st_size, 0)

if __name__ == "__main__":
    unittest.main()