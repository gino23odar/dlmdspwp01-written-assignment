# classes to load datasets

from pathlib import Path
import pandas as pd

from src.exceptions import DataLoadError, DataValidationException

class DataLoader:
    # base class for inheritance requirement

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def validate_file_exists(self) -> None:
        if not self.path.exists():
            raise DataLoadError(f"File not found: {self.path}")

class CSVDataLoader(DataLoader):
    # load and validate data from csv source files
    
    def __init__(self, path: str | Path, required_columns: list[str]) -> None:
        super().__init__(path)
        self.required_columns = required_columns

    def load(self) -> pd.DataFrame:
        # Loasd the csv file and validate structure
        self.validate_file_exists()

        try:
            dataframe = pd.read_csv(self.path)

        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise DataLoadError(f"Failed to load data from {self.path}: {e}") from e

        missing_columns = [column for column in self.required_columns if column not in dataframe.columns]
        if missing_columns:
            raise DataValidationException(f"Missing required columns in {self.path}: {missing_columns}")
        if dataframe.empty:
            raise DataValidationException(f"Dataframe loaded from {self.path} is empty.")

        return dataframe


    