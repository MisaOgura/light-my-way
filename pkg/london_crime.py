import pandas as pd


class LondonCrime():
    def __init__(self, csv):
        self._df = pd.read_csv(csv).dropna(subset=['Longitude', 'Latitude'])
        self._df['Coordinate'] = \
            self._df.apply(lambda x: (x['Longitude'], x['Latitude']), axis=1)

        self._crime_freq_sr = self._df.groupby('Coordinate').size()

    def to_geojson(self):
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

