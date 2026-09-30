from src.loaders import DataLoader

def main() -> None:
    # load the supplied datasets

    training_data = DataLoader("data/train.csv").load()

    ideal_data = DataLoader("data/ideal.csv").load()

    test_data = DataLoader("data/test.csv").load()

    print("Training data:")
    print(training_data.head())

    print("Ideal data:")
    print(ideal_data.head())

    print("Test data:")
    print(test_data.head())


if __name__ == "__main__":
    main()