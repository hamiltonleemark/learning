""" Test symbolic py. """

import sympy

def test_basic():
    """ Test basic concept. """
    var1 = sympy.symbols('IIo')
    var2 = sympy.symbols('IR')

    equation = var1*30 - var2*30
    print(equation)


def test_subs():
    """ Handle multiple length variables. """

    var1 = sympy.symbols('IIo')
    var2 = sympy.symbols('IR')

    equation = sympy.Eq(var1*30 - var2*30, 0)
    print("lhs:", equation.lhs)
    print("rhs:", equation.rhs)
    for arg in equation.lhs.args:
        print("arg:", arg, arg.as_coefficients_dict())
        for (var, value) in arg.as_coefficients_dict().items():
            print("  ", var, value)


def test_multiple():
    """ Handle multiple length variables. """

    var1 = sympy.symbols("var1")
    var2 = sympy.symbols("var2")

    eq1 = 30*var1 + 20*var2 - 100
    print(eq1)

    eq2 = 30*var1 + 20*var2 -100
    print(eq2)
    ans = sympy.solve([eq1, eq2], [var1, var2])
    print(ans)
