""" Miners in the game. """

import logging
import sympy

import ifc
IMPURE = 0.5
NORMAL = 1.0
PURE = 2.0

PREFIX = "miner"


class Ifc(ifc.Producer):
    """ Abstract interface for miners. """
    def __init__(self, speed, material, purity):

        if purity not in [IMPURE, NORMAL, PURE]:
            raise ValueError(f"{purity} unsupported")

        self.speed = speed
        self.material = material
        self.purity = purity
        self.per_min = speed * purity

    def __str__(self):
        return f"{self.material} {self.per_min}/m"

    def __repr__(self):
        return str(self)

    def is_producer(self, item):
        """ Return True if this miner produces this item. """
        return self.material == item

    def is_source(self):
        return True

    @property
    def inputs(self):
        """ Miners do not have inputs. """
        return []

    def equation(self):
        """ REturn the equation for a miner. """
        var1 = sympy.symbols(self.material + "_output")
        equation = sympy.Eq(var1, self.per_min)

        logging.info("%s: miner equation %s", PREFIX, equation)

        return (set([var1]), [equation])


class MK1(Ifc):
    """ Mark 1 miner. """
    def __init__(self, material, purity):
        super().__init__(60, material, purity)


class MK2(Ifc):
    """ Mark 2 miner. """
    def __init__(self, material, purity):
        super().__init__(120, material, purity)


class MK3(Ifc):
    """ Mark 3 miner. """
    def __init__(self, material, purity):
        super().__init__(240, material, purity)
