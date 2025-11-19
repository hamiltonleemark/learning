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


def test_numpy_name_dependency():
    """ Test the nump module functionality. """

    rows = ["Ore output",
            "Ingot", "Ingot output",
            "Plate", "Rod", "Screws", "Reinforced Plate",
            "Plate output", "Rod output", "Screw output",
            "Reinforced Plate output",
            "Ingot output 1", "Ingot output 2"]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output

    #    Oo,  I, Io, P,  R,  S,  RP, Po, Ro, So, RPo, Io1, Io2
    A = numpy.array([
        [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0, 0, 0], # Oo = 120       x
        [ -1, 30, 0,  0,  0,  0,  0,  0,  0,  0,   0, 0, 0], # 30*I = Oo      x
        [ 0,  30,-1,  0,  0,  0,  0,  0,  0,  0,   0, 0, 0], # Io = 30*I

        [ 0,  0, -1,  0,  0,  0,  0,  0,  0,  0,   0, 1, 1], # Io1 + Io2 = Io x
        [ 0,  0,  0, 30,  0,  0,  0,  0,  0,  0,   0,-1, 0], # 30P = Io1 x
        [ 0,  0,  0,  0, 15,  0,  0,  0,  0,  0,   0, 0,-1], # 15R = Io2 x

        [ 0,  0,  0, 20,  0,  0,  0, -1,  0,  0,   0, 0, 0], # 20P = Po       x
        [ 0,  0,  0,  0,  0, 10,  0,  0, -1,  0,   0, 0, 0], # 10S = Ro       x
        [ 0,  0,  0,  0, 15,  0,  0,  0, -1,  0,   0, 0, 0], # 15R = Ro       x
        [ 0,  0,  0,  0,  0, 40,  0,  0,  0, -1,   0, 0, 0], # 40S = So       x
        [ 0,  0,  0,  0,  0,  0, 10, -1,  0,  0,   0, 0, 0], # 10RP = Po      x
        [ 0,  0,  0,  0,  0,  0, 60,  0,  0, -1,   0, 0, 0], # 60RP = So      x
        [ 0,  0,  0,  0,  0,  0, 40,  0,  0,  0,  -1, 0, 0], # 40RP = RPo     x
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_numpy_modular():
    """ Test the nump module functionality. """

    rows = [
        "Ingot output",
        "Plate", "Rod", "Screws", "Reinforced Plate",
        "Plate output", "Rod output 1",
        "Screw output",
        "Reinforced Plate output",
        "Ingot output 1", "Ingot output 2",
        "Rod output 2", "Rod output",
        "Modular"
    ]

    # Oo = Ore output
    # I = Ingot
    # Io = Ingot output

    #    Io, P, R, S,RP,Po,Ro1,So,RPo,Io1,Io2,Ro2,Ro,M
    A = numpy.array([
        [ 1, 0, 0, 0, 0, 0,  0, 0,  0,  0,  0,  0, 0, 0], # Io = 120
        [-1, 0, 0, 0, 0, 0,  0, 0,  0,  1,  1,  0, 0, 0], # Io1 + Io2 = Io x
        [ 0,30, 0, 0, 0, 0,  0, 0,  0, -1,  0,  0, 0, 0], # 30P = Io1 x
        [ 0, 0,15, 0, 0, 0,  0, 0,  0,  0, -1,  0, 0, 0], # 15R = Io2 x
        [ 0,20, 0, 0, 0,-1,  0, 0,  0,  0,  0,  0, 0, 0], # 20P = Po       x
        [ 0, 0, 0,10, 0, 0, -1, 0,  0,  0,  0,  0, 0, 0], # 10S = Ro1       x
        [ 0, 0,15, 0, 0, 0, -1, 0,  0,  0,  0,  0, 0, 0], # 15R = Ro       x
        [ 0, 0, 0,40, 0, 0,  0,-1,  0,  0,  0,  0, 0, 0], # 40S = So       x
        [ 0, 0, 0, 0,10,-1,  0, 0,  0,  0,  0,  0, 0, 0], # 10RP = Po      x
        [ 0, 0, 0, 0,60, 0,  0,-1,  0,  0,  0,  0, 0, 0], # 60RP = So      x
        [ 0, 0, 0, 0, 5, 0,  0, 0, -1,  0,  0,  0, 0, 0], # 5RP = RPo     x
        [ 0, 0, 0, 0, 0, 0,  0, 0,  0,  0,  0, -1, 0,12], # 12M = Ro2
        [ 0, 0, 0, 0, 0, 0,  0, 0,  1,  0,  0,  0, 0, 3], # 3M = RPo
        [ 0, 0, 0, 0, 0, 0,  1, 0,  0,  0,  0,  1,-1, 0], # Ro = Ro1 + Ro2
    ])

    B = numpy.array([120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_modular_prod_only():
    """ Test the nump module functionality. """


    # RIP = Reinforced Iron Plate assemblers
    # P = Iron Plate constructors
    # ROD = Iron Rod constructors
    # SCR = Screw constructors
    # ING = Iron Smelters (Iron Ore → Ingot)

    # 12M = 5RIP
    # 24M = 14ROD
    # 30RIP = 30P
    # 60RIP= 40SCR
    # 10SCR +24M = 15ROD
    # 30ING = 30P + 15ROD
    # 2M = X
    # 30ING = ORE
    # ORE = 240


    #    M,RIP,ROD,  P,SCR,ING,ORE
    A = numpy.array([
        [12,-5,  0,  0,  0,  0, 0], # 12M = 5RIP
        [24, 0,-14,  0,  0,  0, 0], # 24M = 14ROD
        [ 0,30,  0,-30,  0,  0, 0], # 30RIP = 30P
        [ 0, 0,  0, 60,-40,  0, 0], # 60RIP = 40SCR
        [ 0, 0,-15,-30,  0, 30, 0], # 30ING = 30P + 15ROD
        [ 0, 0,  0,  0,  0, 30,-1], # 30ING = ORE
        [ 0, 0,  0,  0,  0,  0, 1], # ORE = 240
    ])

    B = numpy.array([0, 0, 0, 0, 0, 0, 240])

    rows = [
        "Modular", "Reinforced Plate", "Rod",
        "Plate", "Screws", "Ingot", "Ore"
    ]

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)


def test_reinforced_prod_only():
    """ Test the nump module functionality. """


    # RIP = Reinforced Iron Plate assemblers
    # P = Iron Plate constructors
    # ROD = Iron Rod constructors
    # SCR = Screw constructors
    # ING = Iron Smelters (Iron Ore → Ingot)

    # 30RIP = 30P
    # 60RIP= 40SCR
    # 10SCR +24M = 15ROD
    # 30ING = 30P + 15ROD
    # 2M = X
    # 30ING = ORE
    # ORE = 240


    #    RIP,ROD,  P,SCR,ING,ORE
    A = numpy.array([
        [30,  0,-30,  0,  0, 0], # 30RIP = 30P
        [ 0,  0, 60,-40,  0, 0], # 60RIP = 40SCR
        [ 0,-15,-30,  0, 30, 0], # 30ING = 30P + 15ROD
        [ 0,  0,  0,  0, 30,-1], # 30ING = ORE
        [ 0,  0,  0,  0,  0, 1], # ORE = 240
    ])

    B = numpy.array([0, 0, 0, 0, 0, 0, 240])

    rows = [
        "Modular", "Reinforced Plate", "Rod",
        "Plate", "Screws", "Ingot", "Ore"
    ]

    x = numpy.linalg.solve(A, B)
    print(x)
    df = pandas.DataFrame(x, index=rows)
    print(df)
