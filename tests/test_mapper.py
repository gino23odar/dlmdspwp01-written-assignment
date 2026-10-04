import unittest

import pandas as pd

from src.mapper import TestPointMapper
from src.selector import SelectionResult
from src.exceptions import MappingError

class TestTestPointMapper(unittest.TestCase):

    def test_assigns_point_inside_threshold(self):
        ideal = pd.DataFrame({
            "x": [0.0],
            "y2": [1.0],
        })

        test = pd.DataFrame({
            "x": [0.0],
            "y": [1.05],
        })

        selection = [
            SelectionResult(
                training_func="y1",
                ideal_func="y2",
                sse=0.0,
                max_deviation=0.05,
                threshold=0.1,
            )
        ]

        result = TestPointMapper(ideal, selection).map_points(test)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["ideal_func"], 2)
        self.assertAlmostEqual(result.iloc[0]["delta_y"], 0.05)
