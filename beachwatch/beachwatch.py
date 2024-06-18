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
    *names : tuple, optional
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
        Beachwatch records/database.
    """

    def create_beach(beach):
        """Create a Beach object."""

        properties = beach["properties"]
        geometry = beach["geometry"]
        pollution_forecast_timestamp = properties["pollutionForecastTimeStamp"]
        pollution_forecast_timestamp = parser.isoparse(pollution_forecast_timestamp)
        latest_result_observation_timestamp = properties["latestResultObservationDate"]
        latest_result_observation_timestamp = parser.isoparse(
            latest_result_observation_timestamp
        )
        beach = Beach(
            properties["id"],
            properties["siteName"],
            properties["pollutionForecast"],
            pollution_forecast_timestamp,
            properties["latestResult"],
            int(properties["latestResultRating"]),
            latest_result_observation_timestamp,
            geometry,
        )

        return beach

    if names:
        parameters = [
            ("site_name", name) for name in names
        ]  # In case a user passes multiple beach names.

        data = requests.get(
            "https://api.beachwatch.nsw.gov.au/public/sites/geojson",
            params=parameters,
            timeout=15,
        )
        if data.json() == {"type": "FeatureCollection", "features": []} or len(
            data.json()["features"]
        ) != len(names):
            returned_beach_names = [
                feature["properties"]["siteName"] for feature in data.json()["features"]
            ]
            invalid_beaches = list(set(names) - set(returned_beach_names))
            raise ValueError(
                f"The following beaches does not exist or does not exist in the Beachsafe database: {invalid_beaches}"
            )

        beaches = [create_beach(beach) for beach in data.json()["features"]]
        return beaches
    # All beaches.
    data = requests.get(
        "https://api.beachwatch.nsw.gov.au/public/sites/geojson", timeout=15
    )
    beaches = [create_beach(beach) for beach in data.json()["features"]]
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
    latest_result_observation_timestamp : str
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
