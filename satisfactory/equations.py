""" Holds all recipes. """
import sympy

PREFIX = "equations"

def _output_only(recipe):
    """ Return recipe equation. """

    variables = set()
    equations = []

    mvar = sympy.symbols(recipe.output.material)
    variables.add(mvar)
    ovar = sympy.symbols(recipe.output.material+"_output")
    variables.add(ovar)

    equation = sympy.Eq(mvar*recipe.output.per_min, ovar)
    equations.append(equation)

    return (variables, equations)

def _one_output(recipe):
    """ Return recipe equation. """

    variables = set()
    equations = []

    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    for item in recipe.inputs:
        ivar = sympy.symbols(item.material + "_output")
        variables.add(ivar)
        ineq = sympy.Eq(item.per_min*mvar, ivar)
        equations.append(ineq)

    ovar = sympy.symbols(recipe.material + "_output")
    variables.add(ovar)
    outeq = sympy.Eq(recipe.output.per_min*mvar, ovar)
    equations.append(outeq)

    return (variables, equations)


def _two_output(recipe, outputs):
    """ Return recipe equation. """

    variables = set()
    equations = []

    ##
    # Setup input equations
    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    for item in recipe.inputs:
        ivar = sympy.symbols(item.material + "_output")
        variables.add(ivar)
        ineq = sympy.Eq(item.per_min*mvar, ivar)
        equations.append(ineq)

    ovar = sympy.symbols(recipe.output.material + "_output")
    variables.add(ovar)

    ##
    # Setup output equations
    ovar1 = sympy.symbols(outputs[0].material)
    ovar2 = sympy.symbols(outputs[1].material)
    variables.add(ovar1)
    variables.add(ovar2)

    eq = outputs[0].input_get(recipe.material).per_min*ovar1 + \
         outputs[1].input_get(recipe.material).per_min*ovar2
    equation = sympy.Eq(eq, ovar)
    equations.append(equation)
    ##

    return (variables, equations)


def get(recipe, outputs):
    """ Return recipe equation. """

    if len(outputs) in [0, 1]:
        return _one_output(recipe)

    if len(outputs) == 2:
        return _two_output(recipe, outputs)

    raise NotImplementedError(f"{PREFIX} only supports 1 or 2 inputs")
