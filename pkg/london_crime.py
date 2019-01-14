"""LondonCrime

Given a CSV file with longtitude and latitude fields, it accumulates the
row count per coordinate (long, lat) and returns a GeoJSON which can be
used as a data source for Mapbox APIs.

Usage:
    london_crime.py <input>
    london_crime.py (-h | --help)

Options:
    <input>             Inout csv file with longtitude and latitude fields.
    -h --help           Show this screen.
"""
import sys
import json
import pandas as pd
from pathlib import Path
from docopt import docopt


# ----------------------------------------------------------------------------
# Module level methods


def main():
    arguments = docopt(__doc__, version='0.1')

    input_file = arguments['<input>']

    basename = Path(input_file).resolve().stem

    london_crime = LondonCrime(input_file)

    data = london_crime.to_geojson()

    with open('geojson/{}.geojson'.format(basename), 'w') as output:
        json.dump(data, output)


# ----------------------------------------------------------------------------
# LondonCrime class


class LondonCrime():
    def __init__(self, csv):
        self._df = pd.read_csv(csv).dropna(subset=['Longitude', 'Latitude'])
        self._df['Coordinate'] = \
            self._df.apply(lambda x: (x['Longitude'], x['Latitude']), axis=1)

        self._crime_sr = self._df.groupby(['Coordinate', 'Crime type']).size()

        crime_freq_sr = self._df.groupby('Coordinate').size()
        self._min_crime_count = int(crime_freq_sr.min())
        self._max_crime_count = int(crime_freq_sr.max())

    def to_geojson(self):
        # TODO - use https://github.com/frewsxcv/python-geojson
        geojson = {
            "type": "FeatureCollection",
            "minCrimeCount": self._min_crime_count,
            "maxCrimeCount": self._max_crime_count,
            "features": []
        }

        last_coord = None
        data = None

        for (coord, crime_type), crime_count in self._crime_sr.iteritems():

            # Create a new data if it's the new location
            if coord != last_coord:
                if data is not None:
                    geojson['features'].append(data)

                # Re-initialise the data
                data = {
                    'type': 'Feature',
                    'properties': {
                        'totalCrimeCount': 0,
                        'crimeCountPerType': {}
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': []
                    }
                }

            data['properties']['totalCrimeCount'] += crime_count
            data['properties']['crimeCountPerType'][crime_type] = crime_count
            data['geometry']['coordinates'] = [coord[0], coord[1]]

            last_coord = coord

        return geojson

    def min_freq(self):
        return self._crime_sr.min()

    def max_freq(self):
        return self._crime_sr.max()


if __name__ == '__main__':
    main()
