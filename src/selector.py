from dataclasses import dataclass
import math
import pandas as pd

from src.exceptions import DataValidationException

@dataclass(frozen=True)
class SelectionResult:
    # store the matching training function result 
    training_func: str
    ideal_func: str
    sse: float
    max_deviation: float
    threshold: float

class IdealFunctionSelector:
    def __init__(
            self,
            training_data: pd.DataFrame,
            ideal_data: pd.DataFrame,
    ) -> None:
        # initialize selector with training and ideal data
        self.training_data = training_data
        self.ideal_data = ideal_data

    @staticmethod
    def calculate_sse(
        training_values: pd.Series,
        ideal_values: pd.Series,
    ) -> float:
        # calculate the sum of squared y-deviations

        diff = training_values - ideal_values

        return float(
            (diff ** 2).sum()
        )

    def select(
            self,
    ) -> list[SelectionResult]:
        # select the ideal function for each training function

        training = (
            self.training_data
                .set_index("x")
                .sort_index()
        )

        ideal = (
            self.ideal_data
                .set_index("x")
                .sort_index()
        )

        if not training.index.equals(ideal.index):
            raise DataValidationException("Training and ideal data must have the same x-values.")

        results: list[SelectionResult] = []

        for training_column in training.columns:
            best_ideal = None
            best_sse = math.inf

            for ideal_column in ideal.columns:
                sse = self.calculate_sse(
                    training[training_column],
                    ideal[ideal_column],
                )

                if sse < best_sse:
                    best_sse = sse
                    best_ideal = ideal_column

            if best_ideal is None:
                raise DataValidationException(f"No ideal function found for training function '{training_column}'.")

            deviations = abs(training[training_column] - ideal[best_ideal])

            max_deviation = float(deviations.max())
            threshold = (max_deviation * math.sqrt(2))

            results.append(
                SelectionResult(
                    training_func = training_column,
                    ideal_func = best_ideal,
                    sse = best_sse,
                    max_deviation = max_deviation,
                    threshold = threshold,
                )
            )

        return results

'''
temporarily remove to test the new IdealFunctionSelector class

def find_best_ideal_function(
    training_values: pd.Series,
    ideal_data: pd.DataFrame,
) -> tuple[str, float]:
    # find the ideal function with the smallest sse

    best_function = ""
    best_sse = float("inf")

    for column in ideal_data.columns:
        if column == "x":
            continue

        sse = calculate_sse(
            training_values,
            ideal_data[column],
        )

        if sse < best_sse:
            best_sse = sse
            best_function = column

    return best_function, best_sse

def select_ideal_functions(
    training_data: pd.DataFrame,
    ideal_data: pd.DataFrame,
) -> list[dict]:
    """Select one ideal function for each training function."""

    results = []

    for training_column in training_data.columns:
        if training_column == "x":
            continue

        best_function, sse = find_best_ideal_function(
            training_data[training_column],
            ideal_data,
        )

        results.append(
            {
                "training_function": training_column,
                "ideal_function": best_function,
                "sse": sse,
            }
        )

    return results
'''