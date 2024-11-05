"""
Beachwatch is a Python wrapper for the NSW government's Beachwatch API[1]_

.. [1] https://beachwatch.nsw.gov.au/waterMonitoring/beachwatchDataFeeds
"""

from dataclasses import dataclass
from datetime import datetime

from dateutil import parser
import requests


def get_beaches(*names):
    """Create a list of Beach objects.

    Parameters
    ----------
    *names : tuple of str, optional
            The name or names of NSW beaches.

    Returns
    -------
    list
        A list of Beach objects.

    Raises
    ------
    ValueException
        If the API returns no data for one of the beach names passed to this
        function, which would indicate that the beach does not exist in the
        Beachwatch database.
    """

    def create_beach(beach):
        """Create a Beach object."""

        properties = beach["properties"]
        geometry = beach["geometry"]
        latestResultRating = properties.get("latestResultRating")
        try:
            latestResultRating = int(latestResultRating)
        except TypeError:
            pass
        pollution_forecast_timestamp = properties.get("pollutionForecastTimeStamp")
        try:
            pollution_forecast_timestamp = parser.isoparse(pollution_forecast_timestamp)
        except TypeError:
            pass
        latest_result_observation_timestamp = properties.get(
            "latestResultObservationDate"
        )
        try:
            latest_result_observation_timestamp = parser.isoparse(
                latest_result_observation_timestamp
            )
        except TypeError:
            pass
        beach = Beach(
            properties.get("id"),
            properties.get("siteName"),
            properties.get("pollutionForecast"),
            pollution_forecast_timestamp,
            properties.get("latestResult"),
            latestResultRating,
            latest_result_observation_timestamp,
            geometry,
        )

        return beach

    if names:
        parameters = [
            ("site_name", name) for name in names
        ]  # In case a user passes multiple beach names.

        response = requests.get(
            "https://api.beachwatch.nsw.gov.au/public/sites/geojson",
            params=parameters,
            timeout=15,
        )
        response.raise_for_status()
        if response.json() == {"type": "FeatureCollection", "features": []} or len(
            response.json()["features"]
        ) != len(names):
            returned_beach_names = [
                feature["properties"]["siteName"]
                for feature in response.json()["features"]
            ]
            invalid_beaches = list(set(names) - set(returned_beach_names))
            raise ValueError(
                f"The following beaches does not exist or does not exist in the Beachwatch database: {invalid_beaches}"
            )

        beaches = [create_beach(beach) for beach in response.json()["features"]]
        return beaches
    # All beaches.
    response = requests.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson", timeout=15
    )
    response.raise_for_status()
    beaches = [create_beach(beach) for beach in response.json()["features"]]
    return beaches


@dataclass
class Beach:
    """A NSW beach.

    Attributes
    ----------
    id : str
         Unknown but likely a unique ID within the Beatchwatch database/dataset.
    name : str
         The name of the beach.
    pollution_forecast : str
         The latest water quality pollution forecast.
    pollution_forecast_timestamp : datetime.datetime
         What time the forecast was issued by Beachwatch.
    latest_result : str
         A water quality rating based on the number of bacteria (enterococci)
         in the most recent water sample.
    latest_result_rating : int
        The latest water quality result, rated from 1 to 4 to indicate
        suitability for swimming.
    latest_result_observation_timestamp : datetime.datetime
         The most recent sampling date.
    geometry : dict
         A GeoJSON feature with the coordinates of the beach.
    """

    identifier: str
    name: str
    pollution_forecast: str
    pollution_forecast_timestamp: datetime
    latest_result: str
    latest_result_rating: int
    latest_result_observation_timestamp: datetime
    geometry: dict
