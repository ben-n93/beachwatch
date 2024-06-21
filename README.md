# beachwatch 🏖️

<p align="center">
    <a href="https://github.com/ben-n93/beachwatch/actions/workflows/tests.yml/badge.svg"><img src="https://github.com/ben-n93/beachwatch/actions/workflows/tests.yml/badge.svg"           alt="Testing"></a>
    <a href="https://codecov.io/gh/ben-n93/beachwatch"><img src="https://codecov.io/gh/ben-n93/beachwatch/graph/badge.svg?token=XUMK0D4J9X"/></a>
    <a href="https://pypi.org/project/beachwatch/"><img src="https://img.shields.io/pypi/pyversions/beachwatch" alt="versions"></a>
    <a href="https://github.com/ben-n93/beachwatch/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/beachwatch" alt="License"></a>
</p>

`beachwatch` is a Python wrapper for the NSW Government's [Beachwatch API](https://beachwatch.nsw.gov.au/waterMonitoring/beachwatchDataFeeds).

In their own words:

*"Beachwatch and our partners monitor water quality at swim sites to ensure that recreational water environments are managed as safely as possible so that as many people as possible can benefit from using the water."*

With this package you can retrieve data about a NSW beach's water pollution forecast, water quality rating, coordinates and more.

## Installation

```
pip install beachwatch
```

## Usage

There is only one function - `get_beaches()` function, which returns `Beach` objects:

```py
>>> get_beaches() # Returns a list of all Beach objects.
>>> get_beaches("Bondi Beach") # Returns a list with the specified beach.
>>> get_beaches("Bondi Beach", "Whale Beach") # Returns a list with the specifies beaches.
```

The `Beach` object:
``` py
class Beach:
    """A NSW beach.

    Attributes
    ----------
    identifier : str
         Unknown but likely a unique ID within the Beachwatch database.
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
```

Note that the `Beach` object is not meant to be instantiated directly.

### Example
``` py
>>> bondi = get_beaches("Bondi Beach")[0]
>>> bondi.pollution_forecast
    'Good'
```
## Important 

Beachwatch notes on their website that forecasts *"are predictions of water quality only and are not 100% accurate.
Beachwatch cannot guarantee the accuracy of any of the results or outputs from this model. Any reliance you place on such information is strictly at your own risk."*
