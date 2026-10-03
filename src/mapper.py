import pandas as pd

from src.selector import SelectionResult


class TestPointMapper:
    # map test obs to selected functions

    def __init__(self, ideal_data: pd.DataFrame, selection_results: list[SelectionResult]) -> None:
        self.ideal_data = ideal_data
        self.selections = selection_results

    @staticmethod
    def function_num(column_name: str) -> int:
        # convert ideal-func column name to simple integer 

        return int(column_name.removeprefix("y"))

    def map_points(self, test_data: pd.DataFrame) -> pd.DataFrame:
        # map the test points that pass deviation threshold

        ideal = (self.ideal_data.set_index("x"))
        mapped_rows = []

        for row in test_data.itertuples(index=False):
            x_val = float(row.x)
            y_val = float(row.y)

            for selection in self.selections:
                ideal_y = ideal.at[x_val, selection.ideal_func]

                deviation = abs(y_val - ideal_y)

                if(deviation <= selection.threshold):
                    mapped_rows.append(
                        {
                            "x": x_val,
                            "y": y_val,
                            "delta_y": deviation,
                            "ideal_func": self.function_num(selection.ideal_func),
                        }
                    )

                    break

        return pd.DataFrame(mapped_rows, columns=["x", "y", "delta_y", "ideal_func"])