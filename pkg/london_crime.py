"""LondonCrime

Given a CSV file with longtitude and latitude fields, it accumulates the
row count per coordinate (long, lat) and returns a GeoJSON which can be
used as a data source for Mapbox APIs.

Usage:
    london_crime.py <input> [-o=<output>]
    london_crime.py (-h | --help)

Options:
    <input>             Inout csv file with longtitude and latitude fields.
    -o=<output>         Output file [default: output.geojson].
    -h --help           Show this screen.
"""

import sys
import json
import pandas as pd
from docopt import docopt


# ----------------------------------------------------------------------------
# Module level methods


def main():
    arguments = docopt(__doc__, version='0.1')

    input_file = arguments['<input>']
    output_file = arguments['-o']

    london_crime = LondonCrime(input_file)

    data = london_crime.to_geojson()

    with open(output_file, 'w') as output:
        json.dump(data, output)


# ----------------------------------------------------------------------------
# LondonCrime class


class LondonCrime():
    def __init__(self, csv):
        self._df = pd.read_csv(csv).dropna(subset=['Longitude', 'Latitude'])
        self._df['Coordinate'] = \
            self._df.apply(lambda x: (x['Longitude'], x['Latitude']), axis=1)

        self._crime_freq_sr = self._df.groupby('Coordinate').size()

    def to_geojson(self):
        # TODO - use https://github.com/frewsxcv/python-geojson
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        for index, value in self._crime_freq_sr.iteritems():
            data = {
                'type': 'Feature',
                'properties': {
                    'crimes': value
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [index[0], index[1]]
                }
            }

            geojson['features'].append(data)

        return geojson

    def min_freq(self):
        return self._crime_freq_sr.min()

    def max_freq(self):
        return self._crime_freq_sr.max()


if __name__ == '__main__':
    main()
