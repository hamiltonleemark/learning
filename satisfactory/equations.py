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
            mvar = sympy.symbols(item)
            variables.add(mvar)
            if value == 2:
                ovar1 = sympy.symbols(item)
                ovar2 = sympy.symbols(item)
                eq = ovar1 + ovar2
                outeq = sympy.Eq(eq, mvar)
                problems.append(outeq)
            else:
                return (variables, problems)
        return (variables, problems)


VAR_OUT_GEN= VariableOutpuGenerator()


def _one_output(recipe, orecipe):
    """ Return recipe equation. """

    prefix = f"{PREFIX}._one_output"

    variables = set()
    equations = []

    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    ovar = sympy.symbols(orecipe.output.material)
    variables.add(ovar)

    outeq = sympy.Eq(orecipe.output.per_min*mvar,
                     orecipe.inputs[0].per_min*ovar)
    equations.append(outeq)

    return (variables, equations)


def _two_output(recipe, outputs):
    """ Return recipe equation. """

    prefix = f"{PREFIX}._two_output"

    variables = set()
    equations = []

    ##
    # Setup input equations
    mvar = sympy.symbols(recipe.material)
    variables.add(mvar)

    ##
    # Setup output equations
    ovar1 = sympy.symbols(outputs[0].material)
    ovar2 = sympy.symbols(outputs[1].material)
    variables.add(ovar1)
    variables.add(ovar2)

    # pylint: disable=line-too-long
    eq = outputs[0].input_get(recipe.material).per_min*ovar1 + outputs[1].input_get(recipe.material).per_min*ovar2
    outeq = sympy.Eq(recipe.output.per_min*mvar, eq)
    equations.append(outeq)
    logging.debug("%s: in out equation: %s", prefix, outeq)
    ##
    return (variables, equations)


def get(recipe, outputs):
    """ Return recipe equation. """

    if len(outputs) == 0:
        return (set(), [])
    elif len(outputs) == 1:
        return _one_output(recipe, outputs[0])
    elif len(outputs) == 2:
        return _two_output(recipe, outputs)
    else:
        raise ValueError("output amount not supported %d" % len(outputs))
        
