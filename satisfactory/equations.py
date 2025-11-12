""" Holds all recipes. """
import logging
import sympy


# pylint: disable=no-else-return
PREFIX = "equations"


class VariableOutpuGenerator():
    """ Generate unique variable names. """

    def __init__(self):

        self._counter = {}

    def set(self, mat, value):
        """ Set material output. """

        self._counter[mat] = value

    def get(self, mat):
        """ Return unique variable name. """

        if mat not in self._counter:
            return f"{mat}_output"

        counter = self._counter.get(mat)
        name = f"{mat}_output_{counter}"
        counter = counter + 1
        self._counter[mat] = counter
        return name

    def equations(self):
        """ Return the variables that represent the same output. """

        variables = set()
        problems = []
        for (item, value) in self._counter.items():
            mvar = sympy.symbols(item+"_output")
            variables.add(mvar)
            if value == 2:
                ovar1 = sympy.symbols(item+"_output_0")
                ovar2 = sympy.symbols(item+"_output_1")
                eq = ovar1 + ovar2
                outeq = sympy.Eq(eq, mvar)
                problems.append(outeq)
            else:
                raise ValueError(f"dependent output {value} not supported")
        return (variables, problems)


VAR_OUT_GEN= VariableOutpuGenerator()


def _one_output(recipe):
    """ Return recipe equation. """

    prefix = f"{PREFIX}._one_output"

    variables = set()
    equations = []

    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    for item in recipe.inputs:
        ivar = sympy.symbols(VAR_OUT_GEN.get(item.material))
        ineq = sympy.Eq(item.per_min*mvar, ivar)

        variables.add(ivar)
        equations.append(ineq)
        logging.debug("%s: recipe %s in equation: %s", prefix, recipe, ineq)

    ovar = sympy.symbols(recipe.material+"_output")
    variables.add(ovar)
    outeq = sympy.Eq(recipe.output.per_min*mvar, ovar)
    equations.append(outeq)

    return (variables, equations)


def _two_output(recipe, outputs):
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

    # [ 0,  30,-1,  0,  0,  0,  0,  0,  0,  0,  0], # Io = 30*I

    for item in recipe.inputs:
        ivar = sympy.symbols(item.material + "_output")
        variables.add(ivar)
        ineq = sympy.Eq(item.per_min*mvar, ivar)
        equations.append(ineq)
        logging.debug("%s: in equation: %s", prefix, ineq)

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
    outeq = sympy.Eq(eq, ovar)
    equations.append(outeq)
    logging.debug("%s: in out equation: %s", prefix, outeq)
    ##
    return (variables, equations)


def get(recipe):
    """ Return recipe equation. """

    return _one_output(recipe)
