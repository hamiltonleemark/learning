"""
Learning about numpy.
"""
import numpy
from sklearn import datasets
import sklearn.preprocessing


def test_datasets():
    """ Test datasets. """

    digits = datasets.load_digits()
    features = digits["data"]
    assert features[0].any()

def test_minmax():
    """ learning how to handle min max. """

    feature = numpy.array(
        [[500.5],
         [-100.1],
         [0],
         [100.1],
         [900.9]]
    )
    minmax_scale = sklearn.preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled_feature = minmax_scale.fit_transform(feature)

    assert scaled_feature.tolist() == [[0.6], [0. ], [0.1], [0.2], [1. ]]


def test_standardscaling():
    """ learning how to handle Standardscaling. """

    feature = numpy.array(
        [[500.5],
         [-100.1],
         [0],
         [100.1],
         [900.9]]
    )
    standard_scale = sklearn.preprocessing.StandardScaler()
    scaled_feature = standard_scale.fit_transform(feature)

    assert scaled_feature.tolist() == [
        [ 0.59308025], [-1.02441135], [-0.75482941], [-0.48524748],
        [ 1.67140798]]
