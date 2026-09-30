from pathlib import Path
from src.loaders import CSVDataLoader

from src.database import create_database

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

    create_database(
        training_data,
        ideal_data,
    )


if __name__ == "__main__":
    main()