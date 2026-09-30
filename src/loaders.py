# classes to load datasets

from pathlib import Path
import pandas as pd

from src.exceptions import DataLoadError, DataValidationError

class DataLoader:
    
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    