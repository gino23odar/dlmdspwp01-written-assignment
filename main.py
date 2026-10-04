from pathlib import Path
from src.loaders import CSVDataLoader
from src.database import DatabaseManager
from src.selector import IdealFunctionSelector
from src.mapper import TestPointMapper
from src.visualizer import AssignmentVisualizer

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

    selector = IdealFunctionSelector(training_data, ideal_data)
    selections = selector.select()

    mapper = TestPointMapper(ideal_data, selections)

    mapped_data = mapper.map_points(test_data)

    database.save_dataframe(mapped_data, "test_results")

    visualizer = AssignmentVisualizer("output/visualization.html")
    visualization_path = visualizer.create(training_data, ideal_data, selections)
    print(f"Visualization saved to: {visualization_path}")

    print(f"\nMapped test points: " f"\nMapped test points: " f"{len(mapped_data)} / {len(test_data)}")

    for selection in selections:
        print(
            f"{selection.training_func} -> "
            f"{selection.ideal_func} "
            f"(SSE={selection.sse:.6f}, "
            f"max deviation={selection.max_deviation:.6f}, "
            f"threshold={selection.threshold:.6f})"
        )
    database.close()

if __name__ == "__main__":
    main()