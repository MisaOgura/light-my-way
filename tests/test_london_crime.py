import json
import pytest
import pandas as pd

from pkg.london_crime import LondonCrime


@pytest.fixture()
def london_crime():
    return LondonCrime('tests/mock.csv')


def test_to_geojson(london_crime):
    with open('tests/mock.geojson', 'r') as expected:
        expected = json.load(expected)

    actual = london_crime.to_geojson()

    assert actual == expected


def test_min_freq(london_crime):
    assert london_crime.min_freq() == 1


def test_max_freq(london_crime):
    assert london_crime.max_freq() == 3
