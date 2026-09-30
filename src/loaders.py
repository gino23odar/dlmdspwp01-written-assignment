# classes to load datasets

from pathlib import Path
import pandas as pd

from src.exceptions import DataLoadError, DataValidationError

class DataLoader:
    # Load and validat data from csv source files
    
    def __init__(self, path: str | Path, required_columns: list[str]) -> None:
        self.path = Path(path)
        self.required_columns = required_columns

    def load(self) -> pd.DataFrame:
        # Loasd the csv file and validate structure
        if not self.path.exists():
            raise DataLoadError(f"File not found: {self.path}")

        try:
            dataframe = pd.read_csv(self.path)

        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise DataLoadError(f"Failed to load data from {self.path}: {e}") from e

        missing_columns = [column for column in self.required_columns if column not in dataframe.columns]
        if missing_columns:
            raise DataValidationError(f"Missing required columns in {self.path}: {missing_columns}")
        if dataframe.empty:
            raise DataValidationError(f"Dataframe loaded from {self.path} is empty.")

        return dataframe


    