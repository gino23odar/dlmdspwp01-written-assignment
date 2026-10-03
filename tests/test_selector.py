import unittest
import pandas as pd

from src.selector import (
    calculate_sse,
    select_ideal_functions,
)

class TestIdealFunctionSelection(unittest.TestCase):
    
    def test_calculate_sse(self):
        training = pd.Series([1.0, 2.0, 3.0])
        ideal = pd.Series([1.0, 2.0, 4.0])
        result = calculate_sse(training, ideal)

        self.assertAlmostEqual(result, 1.0)

    def test_select_ideal_functions(self):
        training = pd.DataFrame({
            "x": [0.0, 1.0, 2.0],
            "y1": [1.0, 2.0, 3.0],
            "y2": [4.0, 5.0, 6.0],
        })

        ideal = pd.DataFrame({
            "x": [0.0, 1.0, 2.0],
            "y1": [10.0, 20.0, 30.0],
            "y2": [1.0, 2.0, 3.1],
            "y3": [4.1, 5.0, 6.0]
        })

        results = select_ideal_functions(training, ideal)

        self.assertEqual(len(results), 2)

        results_by_training = {result["training_function"]: result for result in results}

        self.assertEqual(results_by_training["y1"]["ideal_function"], "y2")
        self.assertAlmostEqual(results_by_training["y1"]["sse"], 0.01)
        self.assertEqual(results_by_training["y2"]["ideal_function"], "y3")
        self.assertAlmostEqual(results_by_training["y2"]["sse"], 0.01)

if __name__ == "__main__":
    unittest.main()