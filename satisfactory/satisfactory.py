""" handle calculating build solutions base on requirements and recipes. """

import logging
import graph
import ifc
import numpy
import sympy
import pandas
import recipe
import miner

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

    for (key, vertex) in rgraph.vertices.items():
        if isinstance(vertex.recipe, miner.Ifc):
            var1 = sympy.symbols(vertex.recipe.material + "_output")
            equation = sympy.Eq(var1, vertex.recipe.per_min)
            logging.info("%s: miner equation %s", PREFIX, equation)
            print("MARK: ", equation)
        elif isinstance(vertex.recipe, recipe.Recipe):
            out1 = sympy.symbols(vertex.recipe.material + "_output")
            num1 = sympy.symbols(vertex.recipe.material)
            equation = sympy.Eq(vertex.recipe.output.per_min*num1, out1)
            print("MARK: output", equation)

            assert len(vertex.recipe.inputs) == 1, "single input only"

            in1 = sympy.symbols(vertex.recipe.inputs[0].material + "_output")
            equation = sympy.Eq(vertex.recipe.inputs[0].per_min*num1,
                                in1)
            print("MARK: ", equation)
        else:
            raise ValueError(f"{PREFIX} unknown recipe type")

    #columns = [miner.material + " output", "value"]
    #equation = numpy.array([1, miner.per_min])
    #pd = pandas.DataFrame(equation, index=columns)
    #print("MARK: ", equation, pd)
    #equations.append(pd)

    return rgraph
