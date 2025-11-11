""" handle calculating build solutions base on requirements and recipes. """

# pylint: disable=too-many-locals
# pylint: disable=consider-using-f-string

import logging
import sympy
import graph
import ifc

PREFIX = "satisfactory"


def _graph_edge_add(rgraph, cookbook, current_recipe, input_recipe):
    """ Recursively add vertices to graph. """

    if not isinstance(current_recipe, ifc.Producer):
        raise ValueError("current recipe is not a recipe")

    if not isinstance(input_recipe, ifc.Producer):
        raise ValueError("input recipe is not a recipe")

    if not rgraph.edge_add(current_recipe, input_recipe):
        return rgraph

    for item in input_recipe.inputs:
        next_recipe = cookbook.find(item.material)
        rgraph = _graph_edge_add(rgraph, cookbook, input_recipe, next_recipe)
    return rgraph


def _graph_build(cookbook, material):
    """ Return relevent recipes. """

    logging.info("%s: graph build", PREFIX)

    rgraph = graph.Graph()

    current_recipe = cookbook.find(material)

    for item in current_recipe.inputs:
        next_recipe = cookbook.find(item.material)
        rgraph = _graph_edge_add(rgraph, cookbook, current_recipe,
                                   next_recipe)
    return rgraph


def _depth_first_search(rgraph, start_vertex, visited={}, distance=0):
    """ Depth first search of graph. """

    prefix = "%s.dfs" % PREFIX
    logging.info("%s: visiting: %s distance %d", prefix, start_vertex.recipe,
                 distance)

    current = visited.get(start_vertex, -1)
    visited[start_vertex] = max(distance, current)
    if current >= distance:
        return visited

    for neighbor in rgraph.vertex_adjacent(start_vertex):
        #if neighbor not in visited:
        _depth_first_search(rgraph, neighbor, visited, distance + 1)

    return visited


def _dfs_ascending(visited):
    """ Return in ascending order. """

    visited = [item for item in visited.items()]
    visited = sorted(visited, key=lambda item: item[1])
    visited.reverse()
    return visited


def maximize(miners, cookbook, material):
    """ Given a miner purity determine optimal recipes. """

    logging.info("%s: maximize %s", PREFIX, material)

    for item in miners:
        cookbook.miner_add(item)

    rgraph = _graph_build(cookbook, material)
    rgraph.show()

    equations = []
    variables = set()

    ##
    # Calculate recipe
    start_vertex = rgraph.vertex_find_by_value(material)
    visited = _depth_first_search(rgraph, start_vertex)
    visited = _dfs_ascending(visited)
    for (vertex, distance) in visited:
        logging.info("%s visited %s distance %d", PREFIX, vertex, distance)
    ##

    for (vertex, _) in visited:
        (mvars, meqs) = vertex.equations(variables)
        equations += meqs
        variables |= mvars

    equations = _prune_redundant(equations)

    logging.info("%s: variables %d equations %d", PREFIX, len(variables),
                 len(equations))
    logging.info("%s: variables %s", PREFIX, variables)
    for equation in equations:
        logging.info("%s: equation %s", PREFIX, equation)

    ans = sympy.solve(equations, variables)
    return ans
