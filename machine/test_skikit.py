"""
Learning about numpy.
"""
from sklearn import datasets


def test_datasets():
    """ Test datasets. """

    digits = datasets.load_digits()
    features = digits["data"]
    assert features[0].any()
