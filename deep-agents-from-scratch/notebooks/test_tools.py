import pytest 
from notebooks import utils


def test_reducer_syntax():
    """ Learning how to user reducer. """

    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {'d': 4, 'e': 5, 'f': 6}

    dict3 = {**dict1, **dict2}
    print(dict3)
