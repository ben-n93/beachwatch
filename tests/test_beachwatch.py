"""
Tests for beachwatch.py
"""

from datetime import datetime

import pytest
import requests

from beachwatch.beachwatch import get_beaches, Beach


@pytest.fixture
def api_json():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [151.278267, -33.891157]},
                "properties": {
                    "id": "405ce99c-7a0b-43f7-8d28-2ee0b65eebb5",
                    "siteName": "Bondi Beach",
                    "pollutionForecast": "Unlikely",
                    "pollutionForecastTimeStamp": "2024-06-18T03:30:04.62+00:00",
                    "latestResult": "Good",
                    "latestResultRating": 4,
                    "latestResultObservationDate": "2024-06-14T10:00:00+10:00",
                },
            }
        ],
    }


def test_http_error_raises_exception(requests_mock):
    """Test that an exception is raised if the web API returns
    a client or server error.
    """
    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson", status_code=400
    )
    with pytest.raises(requests.exceptions.HTTPError):
        get_beaches()


def test_nonexistent_beach_name(requests_mock):
    """Test that a ValueError is raised when the API returns a blank
    response (indiciating the beach does not exist).
    """
    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson",
        json={"type": "FeatureCollection", "features": []},
    )
    with pytest.raises(ValueError):
        get_beaches("Goose Beach")


def test_nonexistent_beach_name_with_valid_beach_name(requests_mock, api_json):
    """Test that a ValueError is raised when the API returns a blank
    response (indiciating the beach does not exist), even if one
    of the beach names passed is valid.
    """
    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson", json=api_json
    )
    with pytest.raises(ValueError):
        get_beaches("Bondi Beach", "Goose Beach")


def test_nonexistent_beaches_names_in_value_error_message(requests_mock):
    """Test that the ValueError produced when the API returns a blank
    response (indiciating the beach does not exist) returns the name of
    the beach or beaches that do not exist.
    """
    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson",
        json={"type": "FeatureCollection", "features": []},
    )
    with pytest.raises(ValueError) as exc_info:
        get_beaches("Goose Beach")

    assert "Goose Beach" in str(exc_info.value)


def test_no_argument_passed_works(requests_mock, api_json):
    """Test that when no argument is passed no exception is returned."""
    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson",
        json=api_json,
    )
    get_beaches()


def test_beach_object_created(requests_mock, api_json):
    """Test that a Beach object is created."""

    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson", json=api_json
    )
    assert isinstance(get_beaches("Bondi Beach")[0], Beach)


def test_datetime_conversion(requests_mock, api_json):
    """Test that date strings are succesfully converted to
    attributes to datetime objects.
    """
    requests_mock.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson", json=api_json
    )

    assert isinstance(
        get_beaches("Bondi Beach")[0].pollution_forecast_timestamp, datetime
    )
    assert isinstance(
        get_beaches("Bondi Beach")[0].latest_result_observation_timestamp, datetime
    )
