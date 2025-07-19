"""
Learning about numpy.
"""
import pandas

def test_pandas():
    """ Test pandas. """

    dictionary = {
        "Name": ["Jack", "Steven"],
        "Age": [38, 25],
        "Driver": [True, False]
    }
    dataframe = pandas.DataFrame(dictionary)
    assert dataframe is not None


def test_outliers():
    """ Testing outliers. """

    houses = pandas.DataFrame()
    houses["Price"] = [533433, 392333, 293222, 4322032]
    houses["Bathrooms"] = [2, 3.5, 2, 116]
    houses["Square_Feet"] = [1500, 2500, 1500, 48000]

    print(houses[houses['Bathrooms'] < 20])
