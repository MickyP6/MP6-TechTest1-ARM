import json
from typing import Optional, TypedDict

import pandas as pd


class ResponseData(TypedDict):
    time: int
    value: int
    topic_id: int
    topic_name: str
    datetime: str


def _check_required_columns(df: pd.DataFrame) -> bool:
    """
    Checks that the data received is the intended format.
    """
    return all(col in df for col in ["time", "value"])


def _generate_topic_col(df: pd.DataFrame) -> None:
    """
    Add topic columns in order they were exploded
    """
    df["topic_id"] = df.groupby("time").cumcount() + 1
    df["topic_name"] = df["topic_id"].map({1: "rugby", 2: "football", 3: "tennis"})


def _format_date_col(df: pd.DataFrame) -> None:
    """
    Formats date column to be stringified so can be parsed into front-end.
    """
    df["datetime"] = pd.to_datetime(df["time"], unit="s")
    df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d")


def _format_data(data: Optional[str]) -> pd.DataFrame:
    """
    This function trims the dataset of unneeded columns and maps the topic names to their
    respective values. It formats the date as strings for the front-end to consume.
    """
    df = pd.json_normalize(json.loads(data)["default"]["timelineData"])

    if not _check_required_columns(df):
        raise ValueError("The data from the API is not in the expected format")

    df = df[["time", "value"]]
    df = df.explode("value")
    _generate_topic_col(df)
    _format_date_col(df)

    return df


def _get_static_data() -> pd.DataFrame:
    """
    This is a backup should the Google API unexpectedly throw an error.
    """
    return pd.read_csv("/work/static/data/sample_data.csv")


def jsonify_data(data: Optional[str]) -> ResponseData:
    """
    This is calls the other functions to clean data from the API.
    If nothing is received because google keeps 429'ing their own endpoints,
    it will use a sample set previously obtained from google scraping.
    """
    if data is None:
        df = _get_static_data()

    else:
        try:
            df = _format_data(data)
        except ValueError:
            df = _get_static_data()

    return df.to_json(orient="records")
