""" Holds graph implementation. """

import logging
import ifc
import recipe

PREFIX = "graph"

class Vertex():
    """ Graph vertex. """

    def __init__(self, item):
        self.recipe = item
        self.neighbors = []

    def __str__(self):
        """ Content content. """
        # pylint: disable=consider-using-f-string

        return "%s: %s" % (str(self.recipe),
                           ",".join([str(item.recipe) for item in self.neighbors]))

    def __repr__(self):
        return self.__str__()


class Edge():
    """ Edge in graph. """

    def __init__(self, production=0, consumption=0):
        self.production = production
        self.consumption = consumption


class Graph():
    """ Sparse graph. """
    def __init__(self):
        self.vertices = {}

    def vertex_add(self, value):
        """ add a vertex. """

        if not isinstance(value, ifc.Producer):
            raise ValueError("value is not recipe")

        key = str(recipe)

        if key not in self.vertices:
            self.vertices[key] = Vertex(recipe)
        return self.vertices[key]

    def sources_get(self):
        """ List of vertices that are miners. """

        for _, value in self.vertices.items():
            if value.recipe.is_source():
                return [value]
        return []

    def edge_add(self, u_value, v_value):
        """ Add an edge. """

        if not isinstance(u_value, ifc.Producer):
            raise ValueError("u_value is not a recipe")

        if not isinstance(v_value, ifc.Producer):
            raise ValueError("v_value is not a recipe")

        logging.info("%s: edge add %s %s", PREFIX, u_value, v_value)

        u_vertex = self.vertex_add(u_value)
        v_vertex = self.vertex_add(v_value)
        u_vertex.neighbors.append(v_vertex)
        v_vertex.neighbors.append(u_vertex)

    def show(self):
        """ Show graph content. """

        print("graph vertices")
        for (key, value) in self.vertices.items():
            neighbors = [str(item.recipe) for item in value.neighbors]
            print(f"{key}: {neighbors}")
