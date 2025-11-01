""" Holds graph implementation. """

class Vertex():
    """ Graph vertex. """

    def __init__(self, recipe):
        self.recipe = recipe
        self.neighbors = []

class Edge():
    """ Edge in graph. """

    def __init__(self, production=0, consumption=0):
        self.production = production
        self.consumption = consumption


class Graph():
    """ Sparse graph. """
    def __init__(self):
        self.vertices = {}

    def vertex_add(self, recipe):
        """ add a vertex. """

        name = str(recipe)
        if name not in self.vertices:
            self.vertices[name] = Vertex(recipe)
        return self.vertices[name]

    def edge_add(self, u_recipe, v_recipe):
        """ Add an edge. """
        u_vertex = self.vertex_add(u_recipe)
        v_vertex = self.vertex_add(v_recipe)
        u_vertex.neighbors.append(v_vertex)
