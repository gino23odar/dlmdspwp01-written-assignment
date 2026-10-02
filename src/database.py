from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine


class DatabaseManager:
    # manage assignment data stored in SQLite

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:
        path = Path(database_path).resolve()

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.engine: Engine = create_engine(
            f"sqlite:///{path.as_posix()}"
        )

    def save_dataframe(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
    ) -> None:
        # Save a DataFrame as a database table

        dataframe.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False,
        )

    def read_table(
        self,
        table_name: str,
    ) -> pd.DataFrame:
        # Read a database table

        return pd.read_sql_table(
            table_name,
            self.engine,
        )

    def table_exists(
        self,
        table_name: str,
    ) -> bool:
        # Return whether a table exists

        inspector = inspect(self.engine)

        return (
            table_name
            in inspector.get_table_names()
        )

    def close(self) -> None:
        # close database connections held by the SQLAlchemy engine

        self.engine.dispose()