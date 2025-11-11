""" Holds all recipes. """
import logging
import sympy

# pylint: no-else-return

PREFIX = "equations"


def _one_output(recipe, filter_variables=None):
    """ Return recipe equation. """

    if filter_variable is None:
        filter_variable = []

    prefix = f"{PREFIX}._one_output"

    variables = set()
    equations = []

    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    for item in recipe.inputs:
        ivar = sympy.symbols(item.material + "_output")
        if ivar in filter_variables:
            continue
        variables.add(ivar)
        ineq = sympy.Eq(item.per_min*mvar, ivar)
        equations.append(ineq)
        logging.debug("%s: recipe %s in equation: %s", prefix, recipe, ineq)

    ovar = sympy.symbols(recipe.material + "_output")
    if ovar in filter_variables:
        return (variables, equations)
    variables.add(ovar)
    outeq = sympy.Eq(recipe.output.per_min*mvar, ovar)
    equations.append(outeq)

    return (variables, equations)


def _two_output(recipe, outputs, filter_variables):
    """ Return recipe equation. """

    prefix = f"{PREFIX}._two_output"

    if filter_variables is None:
        filter_variables = []

    variables = set()
    equations = []

    ##
    # Setup input equations
    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    for item in recipe.inputs:
        ivar = sympy.symbols(item.material + "_output")
        if ivar in filter_variables:
            continue
        variables.add(ivar)
        ineq = sympy.Eq(item.per_min*mvar, ivar)
        equations.append(ineq)
        logging.debug("%s: in equation: %s", prefix, ineq)

    ovar = sympy.symbols(recipe.output.material + "_output")
    if ovar in filter_variables:
        return (variables, equations)
    variables.add(ovar)

    ##
    # Setup output equations
    ovar1 = sympy.symbols(outputs[0].material)
    ovar2 = sympy.symbols(outputs[1].material)
    variables.add(ovar1)
    variables.add(ovar2)

    eq = outputs[0].input_get(recipe.material).per_min*ovar1 + \
            outputs[1].input_get(recipe.material).per_min*ovar2
    outeq = sympy.Eq(eq, ovar)
    equations.append(outeq)
    logging.debug("%s: in in equation: %s", prefix, outeq)
    ##

    return (variables, equations)


def get(recipe, outputs, filter_variables):
    """ Return recipe equation. """

    if len(outputs) in [0, 1]:
        return _one_output(recipe, filter_variables)
    elif len(outputs) == 2:
        return _two_output(recipe, outputs, filter_variables)

    raise NotImplementedError(f"{PREFIX} only supports 1 or 2 inputs")
