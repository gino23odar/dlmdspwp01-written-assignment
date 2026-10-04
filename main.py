from pathlib import Path

from src.loaders import CSVDataLoader
from src.database import DatabaseManager
from src.selector import IdealFunctionSelector
from src.mapper import TestPointMapper
from src.visualizer import AssignmentVisualizer

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

def main() -> None:
    # load the supplied datasets

    training_columns = ["x", "y1", "y2", "y3", "y4"]
    ideal_columns = ["x", *[f"y{i}" for i in range(1,51)]]
    test_columns = ["x", "y"]


    training_data = CSVDataLoader(DATA_DIR/"train.csv", training_columns).load()
    ideal_data = CSVDataLoader(DATA_DIR/"ideal.csv", ideal_columns).load()
    test_data = CSVDataLoader(DATA_DIR/"test.csv", test_columns).load()

    database = DatabaseManager(
        "OUTPUT_DIR/assignment.db"
    )

    try:
        database.save_dataframe(training_data, "training_data")
        database.save_dataframe(ideal_data, "ideal_functions")

        selector = IdealFunctionSelector(training_data, ideal_data)
        selections = selector.select()
        
        mapper = TestPointMapper(ideal_data, selections)
        mapped_data = mapper.map_points(test_data)
        
        database.save_dataframe(mapped_data, "test_results")

        visualizer = AssignmentVisualizer(OUTPUT_DIR/"visualization.html")
        visualization_path = visualizer.create(training_data, ideal_data, test_data, mapped_data, selections)

        print("Selected functions:")

        for selection in selections:
            print(
                f"{selection.training_func} -> "
                f"{selection.ideal_func} "
                f"| SSE={selection.sse:.6f}"
                f"| max deviation={selection.max_deviation:.6f}"
                f"| threshold={selection.threshold:.6f})"
            )

        print(f"Unamapped test points: {len(test_data) - len(mapped_data)}")
        print(f"\nDB: {OUTPUT_DIR/'assignment.db'}")
        print(f"Vis: {visualization_path}")

    finally:
        database.close()

    Path("output").mkdir(
        exist_ok=True
    )

if __name__ == "__main__":
    main()