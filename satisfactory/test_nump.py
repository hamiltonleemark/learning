""" Test numpy samples. """
import numpy
import pandas

# pylint: disable=invalid-name

def test_numpy_solve_linear():
    """ Test the nump module functionality. """

    A = numpy.array([
        [30, 15,  0,  0,  0,   0,  0],
        [20, 0,   0,  0, -1,   0,  0],
        [0,  0,  10,  0,  0,  -1,  0],
        [0,  0,   0, 10,  -1,  0,  0],
        [0,  15,  0,  0,   0,  -1, 0],
        [0,   0, 40,  0,   0,   0, -1],
        [0,   0,  0, 60,   0,   0, -1]])
    B = numpy.array([120, 0, 0, 0, 0, 0, 0])

    x = numpy.linalg.solve(A, B)
    print(x)
    assert x[0] == 2.0
    assert x[1] == 4.0
    assert x[2] == 6.0
    assert x[3] == 4.0
    assert x[4] == 40.0
    assert x[5] == 60.0
    assert x[6] == 240.0


def test_numpy_name():
    """ Test the nump module functionality. """

    rows = ["Plate", "Rod", "Screws", "Reinforced Plates",
            "Plate output", "Rod output", "Screw output"]

    A = numpy.array([
        [30, 15,  0,  0,  0,   0,  0],
        [20, 0,   0,  0, -1,   0,  0],
        [0,  0,  10,  0,  0,  -1,  0],
        [0,  0,   0, 10,  -1,  0,  0],
        [0,  15,  0,  0,   0,  -1, 0],
        [0,   0, 40,  0,   0,   0, -1],
        [0,   0,  0, 60,   0,   0, -1]])
    B = numpy.array([120, 0, 0, 0, 0, 0, 0], )

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)
