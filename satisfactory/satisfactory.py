""" handle calculating build solutions base on requirements and recipes. """

import logging
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

    logging.info("%s: graph_vertex_add input %s", PREFIX, input_recipe)
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
        print(f"{PREFIX}: graph build {current_recipe} {item}")
        next_recipe = cookbook.find(item.material)
        rgraph = _graph_vertex_add(rgraph, cookbook, current_recipe,
                                   next_recipe)
    return rgraph


def maximize(miners, cookbook, material):
    """ Given a miner purity determine optimal recipes. """

    logging.info("%s: maximize %s", PREFIX, material)

    for miner in miners:
        cookbook.miner_add(miner)
    rgraph = _graph_build(cookbook, material)
    logging.info("%s: cookbook %s", PREFIX, cookbook)

    return rgraph
