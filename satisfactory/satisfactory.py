""" handle calculating build solutions base on requirements and recipes. """

import logging
import graph

PREFIX = "satisfactory"


def _graph_vertex_add(rgraph, cookbook, output_material, input_material):
    """ Recursively add vertices to graph. """

    logging.info("%s: graph_vertex_add input %s", PREFIX, input_material)
    current = cookbook.find(input_material)
    rgraph.edge_add(output_material, current.material)
    for item in current.inputs:
        rgraph = _graph_vertex_add(rgraph, cookbook, current.material,
                                   item.material)
    return rgraph

def _graph_build(cookbook, material):
    """ Return relevent recipes. """

    rgraph = graph.Graph()

    current = cookbook.find(material)
    rgraph.vertex_add(current)

    for item in current.inputs:
        rgraph = _graph_vertex_add(rgraph, cookbook, current.material,
                                   item.material)

    return rgraph


def maximize(miners, cookbook, material):
    """ Given a miner purity determine optimal recipes. """

    logging.info("%s: maximize %s", PREFIX, material)

    for miner in miners:
        cookbook.miner_add(miner)
    rgraph = _graph_build(cookbook, material)
    logging.info("%s: cookbook %s", PREFIX, cookbook)
    return rgraph
