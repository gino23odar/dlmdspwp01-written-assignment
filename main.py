from src.loaders import DataLoader

def main() -> None:
    # load the supplied datasets

    training_data = DataLoader("data/train.csv", ["x", "y1", "y2", "y3", "y4"],).load()

    ideal_columns = [
        "x",
        *[f"y{i}" for i in range(1, 51)],
    ]

    ideal_data = DataLoader("data/ideal.csv", ideal_columns).load()

    test_data = DataLoader("data/test.csv", ["x", "y"]).load()

    print(f"Training dataset: {training_data.shape}")

    print(f"Ideal dataset: {ideal_data.shape}")

    print(f"Test dataset: {test_data.shape}")


if __name__ == "__main__":
    main()