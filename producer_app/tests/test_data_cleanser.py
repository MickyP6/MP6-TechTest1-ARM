import json
from unittest.mock import patch

import pandas as pd
import pytest

import data_cleanser as dc


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {"time": [123, 123, 123, 234, 234, 345], "value": [345, 456, 256, 274, 838, 205]}
    )


@pytest.fixture
def expected_df():
    return pd.DataFrame(
        {
            "time": [123, 123, 123, 234, 234, 345],
            "value": [345, 456, 256, 274, 838, 205],
            "topic_id": [1, 2, 3, 1, 2, 1],
            "topic_name": ["rugby", "football", "tennis", "rugby", "football", "rugby"],
            "datetime": [
                "1970-01-01",
                "1970-01-01",
                "1970-01-01",
                "1970-01-01",
                "1970-01-01",
                "1970-01-01",
            ],
        }
    )


def test_check_required_cols_returns_true(mock_df):
    assert dc._check_required_columns(mock_df)


def test_check_required_cols_return_false(mock_df):
    df = mock_df.copy()
    df.drop(columns=["value"], inplace=True)
    assert not dc._check_required_columns(df)


def test_generate_correct_col_topics(mock_df, expected_df):
    df = mock_df.copy()
    dc._generate_topic_col(df)
    assert df.equals(expected_df.drop(columns=["datetime"]))


def test_format_date_cols_return_correct_format(mock_df, expected_df):
    df = mock_df.copy()
    dc._format_date_col(df)
    assert df["datetime"].equals(expected_df["datetime"])


def test_format_data_matches_expected_output(mock_df, expected_df):
    mock_data = mock_df.to_dict(orient="records")
    mock_json = json.dumps({"default": {"timelineData": mock_data}})
    df = dc._format_data(mock_json)
    assert df.equals(expected_df)


@patch("data_cleanser._get_static_data")
def test_jsonify_data_in_None_out_static(patched_file):
    patched_file.return_value = pd.read_csv("static/data/sample_data.csv")
    response = dc.jsonify_data(None)
    assert response == pd.read_csv("static/data/sample_data.csv").to_json(orient="records")
