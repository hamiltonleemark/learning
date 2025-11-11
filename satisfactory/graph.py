""" Holds graph implementation. """

import logging
import ifc

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

    def id_get(self):
        """ Get vertex id. """
        return str(self.recipe)

    def __repr__(self):
        return self.__str__()

    def equations(self, variables):
        """ Return variables and equations. """

        outputs = [item.recipe for item in self.neighbors]
        return self.recipe.equations(outputs)


class Edge():
    """ Edge in graph. """

    def __init__(self, production=0, consumption=0):
        self.production = production
        self.consumption = consumption


class Graph():
    """ Sparse graph. """
    def __init__(self):
        self.vertices = {}

    def vertex_adjacent(self, vertex):
        """ Get adjacent vertices. """
        adjacent = [item for item in self.vertices.values()
                    if vertex in item.neighbors]
        return adjacent

    def vertex_find_by_value(self, value):
        """ Find vertex by value. """

        key = str(value)
        if key in self.vertices:
            return self.vertices[key]
        raise ValueError("vertex not found")

    def vertex_add(self, value):
        """ add a vertex. """

        if not isinstance(value, ifc.Producer):
            raise ValueError("value is not recipe")

        key = str(value)

        if key not in self.vertices:
            self.vertices[key] = Vertex(value)
        return self.vertices[key]

    def edge_add(self, u_value, v_value):
        """ Add an edge. """

        if not isinstance(u_value, ifc.Producer):
            raise ValueError("u_value is not a recipe")

        if not isinstance(v_value, ifc.Producer):
            raise ValueError("v_value is not a recipe")

        logging.info("%s: edge add %s %s", PREFIX, u_value, v_value)

        u_vertex = self.vertex_add(u_value)
        v_vertex = self.vertex_add(v_value)
        if u_vertex in v_vertex.neighbors:
            logging.info("%s: edge exists %s %s", PREFIX, u_value, v_value)
            return False
        #u_vertex.neighbors.append(v_vertex)
        v_vertex.neighbors.append(u_vertex)
        return True

    def show(self):
        """ Show graph content. """

        print("graph vertices")
        for (key, value) in self.vertices.items():
            neighbors = [str(item.recipe) for item in value.neighbors]
            print(f"show neighbors {key}: {neighbors}")
