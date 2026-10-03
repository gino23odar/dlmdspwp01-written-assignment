import pandas as pd


def calculate_sse(
    training_values: pd.Series,
    ideal_values: pd.Series,
) -> float:
    # calculate the sum of squared errors

    difference = training_values - ideal_values

    return float(
        (difference ** 2).sum()
    )


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