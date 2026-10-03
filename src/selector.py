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