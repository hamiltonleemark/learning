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

    rows = ["Ore output",
            "Ingot", "Ingot output",
            "Plate", "Rod", "Screws", "Reinforced Plate",
            "Plate output", "Rod output", "Screw output",
            "Reinforced Plate output"]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output

    #    Oo,  I, Io, P,  R,  S,  RP, Po, Ro, So, RPo
    A = numpy.array([
        [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0], # Oo = 120       x
        [ -1, 30, 0,  0,  0,  0,  0,  0,  0,  0,  0], # 30*I = Oo      x
        [ 0,  30,-1,  0,  0,  0,  0,  0,  0,  0,  0], # Io = 30*I
        [ 0,  0, -1, 30, 15,  0,  0,  0,  0,  0,  0], # 30P + 15R = Io x
        [ 0,  0,  0, 20,  0,  0,  0, -1,  0,  0,  0], # 20P = Po       x
        [ 0,  0,  0,  0,  0, 10,  0,  0, -1,  0,  0], # 10S = Ro       x
        [ 0,  0,  0,  0, 15,  0,  0,  0, -1,  0,  0], # 15R = Ro       x
        [ 0,  0,  0,  0,  0, 40,  0,  0,  0, -1,  0], # 40S = So       x
        [ 0,  0,  0,  0,  0,  0, 10, -1,  0,  0,  0], # 10RP = Po      x
        [ 0,  0,  0,  0,  0,  0, 60,  0,  0, -1,  0], # 60RP = So      x
        [ 0,  0,  0,  0,  0,  0, 40,  0,  0,  0, -1], # 40RP = RPo     x
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_numpy_screws():
    """ Test the nump module functionality. """

    rows = ["Ore output", "Ingot", "Ingot output",
            "Rod", "Screws", "Rod output", "Screw output"]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output

    #    Oo,  I, Io,  R,  S, Ro,  So
    A = numpy.array([
        [ 1,  0,  0,  0,  0,  0,  0],  # Oo = 120
        [-1, 30,  0,  0,  0,  0,  0],  # 30*I = Oo
        [ 0, 30, -1,  0,  0,  0,  0],  # Io = 30*I
        [ 0,  0, -1, 15,  0,  0,  0],  # 15R = Io
        [ 0,  0,  0,  0, 10, -1,  0],  # 10S = Ro
        [ 0,  0,  0, 15,  0, -1,  0],  # 15R = Ro
        [ 0,  0,  0,  0, 40,  0, -1],  # 40S = So
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_numpy_two_items():
    """ Understand what to do when there are two final outputs.
        
    Need to assing a contraint on one of them. In this case, S =  6.
    """

    rows = ["Ore output", "Ingot", "Ingot output", "Plate", "Rod",
            "Screws", "Plate output", "Rod output", "Screw output"]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output
    #    Oo,  I, Io, P,  R,  S,  Po, Ro, So
    A = numpy.array([
        [ 1,  0,  0,  0,  0,  0,  0,  0,  0], # Oo = 120
        [ -1, 30, 0,  0,  0,  0,  0,  0,  0], # 30*I = Oo
        [ 0,  30,-1,  0,  0,  0,  0,  0,  0], # Io = 30*I
        [ 0,  0, -1, 30, 15,  0,  0,  0,  0], # 30P + 15R = Io
        [ 0,  0,  0, 20,  0,  0, -1,  0,  0], # 20P = Po
        [ 0,  0,  0,  0,  0, 10,  0, -1,  0], # 10S = Ro
        [ 0,  0,  0,  0, 15,  0,  0, -1,  0], # 15R = Ro
        [ 0,  0,  0,  0,  0, 40,  0,  0, -1], # 40S = So
        [ 0,  0,  0,  0,  0,  1,  0,  0,  0], # S = 6
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0, 0, 6])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_top_down():
    """ Test the nump module functionality. """

    rows = ["Ore output", "Ingot", "Ingot output", "Plate", "Rod", "Screws",
            "Reinforced Plate", "Plate output", "Rod output", "Screw output",
            "Reinforced Plate output"]

    # RPo = 40RP

    # RP = 10Po + 60So
    # Po = 20P
    # So = 40S
    # P = 30 Io1
    # S = 10Ro
    # Ro = 15R
    # R = 15Io2
    # Io1 + Io2 = 120
    #[  -1, 40,  0,  0,  0,   0,  0,  0,  0,   0], # RPo = 40RP

    A = numpy.array([
        # RP, Po, So,  P, Io1,  S, Ro,  R, Io2,
        [ -1, 10, 60,  0,   0,  0,  0,  0,   0], # RP = 10Po + 60So
        [  0, -1,  0, 20,   0,  0,  0,  0,   0], # Po = 20*P
        [  0,  0, -1,  0,   0, 40,  0,  0,   0], # So =  40S
        [  0,  0,  0, -1,  30,  0,  0,  0,   0], # P = 30Io1
        [  0,  0,  0,  0,   0, -1, 10,  0,   0], # S = 10Ro
        [  0,  0,  0,  0,   0,  0, -1, 15,   0], # Ro = 15R
        [  0,  0,  0,  0,   0,  0,  0, -1,  15], # R = 15Io2
        [  0,  0,  0,  0,   1,  0,  0,  0,   1], # Io1 + Io2 = 120
    ])

    B = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 120])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_numpy_screws():
    """ Test the nump module functionality. """

    rows = ["Ore output", "Ingot", "Ingot output",
            "Rod", "Screws", "Rod output", "Screw output"]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output

    #    Oo,  I, Io,  R,  S, Ro,  So
    A = numpy.array([
        [ 1,  0,  0,  0,  0,  0,  0],  # Oo = 120
        [-1, 30,  0,  0,  0,  0,  0],  # 30*I = Oo
        [ 0, 30, -1,  0,  0,  0,  0],  # Io = 30*I
        [ 0,  0, -1, 15,  0,  0,  0],  # 15R = Io
        [ 0,  0,  0,  0, 10, -1,  0],  # 10S = Ro
        [ 0,  0,  0, 15,  0, -1,  0],  # 15R = Ro
        [ 0,  0,  0,  0, 40,  0, -1],  # 40S = So
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_numpy_two_items():
    """ Understand what to do when there are two final outputs.
        
    Need to assing a contraint on one of them. In this case, S =  6.
    """

    rows = ["Ore output", "Ingot", "Ingot output", "Plate", "Rod",
            "Screws", "Plate output", "Rod output", "Screw output"]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output
    #    Oo,  I, Io, P,  R,  S,  Po, Ro, So
    A = numpy.array([
        [ 1,  0,  0,  0,  0,  0,  0,  0,  0], # Oo = 120
        [ -1, 30, 0,  0,  0,  0,  0,  0,  0], # 30*I = Oo
        [ 0,  30,-1,  0,  0,  0,  0,  0,  0], # Io = 30*I
        [ 0,  0, -1, 30, 15,  0,  0,  0,  0], # 30P + 15R = Io
        [ 0,  0,  0, 20,  0,  0, -1,  0,  0], # 20P = Po
        [ 0,  0,  0,  0,  0, 10,  0, -1,  0], # 10S = Ro
        [ 0,  0,  0,  0, 15,  0,  0, -1,  0], # 15R = Ro
        [ 0,  0,  0,  0,  0, 40,  0,  0, -1], # 40S = So
        [ 0,  0,  0,  0,  0,  1,  0,  0,  0], # S = 6
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0, 0, 6])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)
