""" handle calculating build solutions base on requirements and recipes. """

# pylint: disable=too-many-locals
# pylint: disable=consider-using-f-string

import logging
import sympy
import graph
import ifc

PREFIX = "satisfactory"


def _graph_vertex_add(rgraph, cookbook, current_recipe, input_recipe):
    """ Recursively add vertices to graph. """

    logging.info("%s: vertex add %s %s", PREFIX, current_recipe, input_recipe)

    if not isinstance(current_recipe, ifc.Producer):
        raise ValueError("current recipe is not a recipe")

    if not isinstance(input_recipe, ifc.Producer):
        raise ValueError("input recipe is not a recipe")

    rgraph.edge_add(current_recipe, input_recipe)

    for item in input_recipe.inputs:
        next_recipe = cookbook.find(item.material)
        rgraph = _graph_vertex_add(rgraph, cookbook, input_recipe, next_recipe)
    return rgraph


def _graph_build(cookbook, material):
    """ Return relevent recipes. """

    logging.info("%s: graph build", PREFIX)

    rgraph = graph.Graph()

    current_recipe = cookbook.find(material)
    rgraph.vertex_add(current_recipe)

    for item in current_recipe.inputs:
        next_recipe = cookbook.find(item.material)
        rgraph = _graph_vertex_add(rgraph, cookbook, current_recipe,
                                   next_recipe)
    return rgraph


def maximize(miners, cookbook, material):
    """ Given a miner purity determine optimal recipes. """

    logging.info("%s: maximize %s", PREFIX, material)

    for item in miners:
        cookbook.miner_add(item)

    rgraph = _graph_build(cookbook, material)
    rgraph.show()

    equations = []
    variables = set()

    for (_, vertex) in rgraph.vertices.items():
        (mvars, meqs) = vertex.equations()
        equations += meqs
        variables |= mvars

    logging.info("%s: variables %s", PREFIX, variables)
    for equation in equations:
        logging.info("%s: equation %s", PREFIX, equation)

    ans = sympy.solve(equations, variables)
    return ans
