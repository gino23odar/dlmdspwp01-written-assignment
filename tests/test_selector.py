import unittest
import math
import pandas as pd

from src.selector import IdealFunctionSelector

class TestIdealFunctionSelection(unittest.TestCase):
    
    def test_calculate_sse(self):
        training = pd.Series([1.0, 2.0, 3.0])
        ideal = pd.Series([1.0, 2.0, 4.0])
        result = (IdealFunctionSelector.calculate_sse(training, ideal))

        self.assertAlmostEqual(result, 1.0)

    def test_select_ideal_functions(self):
        training = pd.DataFrame({
            "x": [0.0, 1.0, 2.0],
            "y1": [1.0, 2.0, 3.0],
        })

        ideal = pd.DataFrame({
            "x": [0.0, 1.0, 2.0],
            "y1": [10.0, 20.0, 30.0],
            "y2": [1.0, 2.0, 3.1],
        })

        selector = IdealFunctionSelector(training, ideal).select()

        self.assertEqual(len(selector), 1)

        results = selector[0]

        self.assertEqual(results.training_func, "y1")
        self.assertEqual(results.ideal_func, "y2")
        self.assertAlmostEqual(results.sse, 0.01)
        self.assertAlmostEqual(results.max_deviation, 0.1)
        self.assertAlmostEqual(results.threshold, 0.1*math.sqrt(2))

if __name__ == "__main__":
    unittest.main()