import sympy

def test_basic():
    var1 = sympy.symbols('IIo')
    var2 = sympy.symbols('IR')

    equation = var1*30 - var2*30
    print(equation)


def test_subs():
    var1 = sympy.symbols('IIo')
    var2 = sympy.symbols('IR')

    equation = sympy.Eq(var1*30 - var2*30, 0)
    print("lhs:", equation.lhs)
    print("rhs:", equation.rhs)
    #help(equation.lhs)
    for arg in equation.lhs.args:
        print("arg:", arg, arg.as_coefficients_dict())
        for (var, value) in arg.as_coefficients_dict().items():
            print("  ", var, value)
