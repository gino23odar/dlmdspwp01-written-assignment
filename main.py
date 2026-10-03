from pathlib import Path
from src.loaders import CSVDataLoader
from src.database import DatabaseManager
from src.selector import select_ideal_functions

def main() -> None:
    # load the supplied datasets

    training_data = CSVDataLoader("data/train.csv", ["x", "y1", "y2", "y3", "y4"]).load()

    ideal_columns = [
        "x",
        *[f"y{i}" for i in range(1, 51)],
    ]

    ideal_data = CSVDataLoader("data/ideal.csv", ideal_columns).load()
    test_data = CSVDataLoader("data/test.csv", ["x", "y"]).load()

    print(f"Training dataset: {training_data.shape}")
    print(f"Ideal dataset: {ideal_data.shape}")
    print(f"Test dataset: {test_data.shape}")

    Path("output").mkdir(
        exist_ok=True
    )

    database = DatabaseManager(
        "output/assignment.db"
    )

    database.save_dataframe(
        training_data,
        "training_data",
    )

    database.save_dataframe(
        ideal_data,
        "ideal_functions",
    )

    selections = select_ideal_functions(
        training_data,
        ideal_data,
    )

    print("\nSelected ideal functions:")

    for selection in selections:
        print(
            f"{selection['training_function']} -> "
            f"{selection['ideal_function']} "
            f"(SSE={selection['sse']:.6f})"
        )
    database.close()

if __name__ == "__main__":
    main()