import pandas as pd
from sqlalchemy import create_engine

def create_database(training_data: pd.DataFrame, ideal_data: pd.DataFrame) -> None:
    # creates a sqlite db and persists the source datasets

    engine = create_engine("sqlite:///output/assignment.db")

    training_data.to_sql("training_data", engine, if_exists="replace", index=False)
    ideal_data.to_sql("ideal_functions", engine, if_exists="replace", index=False)