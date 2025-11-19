""" Holds all recipes. """
import ifc
import material
import equations

PREFIX = "recipe"


class Input():
    """ An input material and the amount required per minute. """
    def __init__(self, item , per_min):
        self.material = item
        self.per_min = per_min

    def __str__(self):
        return f"{self.material} {self.per_min}/m"


class Output():
    """ An output material and its production rate. """
    def __init__(self, item, per_min):
        self.material = item
        self.per_min = per_min

    def __str__(self):
        return f"{self.material} {self.per_min}/m"


class Recipe(ifc.Producer):
    """ A recipe for producing a material from inputs. """
    def __init__(self, inputs, output_material, output_per_min):
        super().__init__()

        if not inputs:
            raise ValueError(f"{inputs} inputs none")

        if not output_per_min:
            raise ValueError(f"{output_per_min} output_per_min")

        self.inputs = inputs
        self.output = Output(output_material, output_per_min)

    @property
    def material(self):
        """ The material produced by this recipe. """

        return self.output.material

    def input_get(self, imat):
        """ Return the input of the given material. """
        for item in self.inputs:
            if item.material == imat:
                return item
        raise ValueError("{PREFIX} recipe %s does not take {imat}")

    def is_source(self):
        return False

    def is_producer(self, item):
        return self.output.material == item

    def __str__(self):
        return self.output.material

    def __repr__(self):
        return str(self)

    def equations(self, outputs):
        """ Return recipe equations. """

        return equations.get(self, outputs)


class CookBook():
    """ A collection of recipes. """
    def __init__(self, recipes=None):
        if recipes is None:
            recipes = []
        self.recipes = recipes

    def miner_add(self, miner):
        """ Add a miner recipe to the cookbook. """

        self.recipes.append(miner)

    def recipe_add(self, recipe):
        """ Add a recipe to the cookbook. """

        self.recipes.append(recipe)

    def sources_get(self):
        """ List of sources. """

        return [item for item in self.recipes if item.is_source()]

    def find(self, item):
        """ Return the recipe for the given material. """

        for recipe in self.recipes:
            if recipe.is_producer(item):
                return recipe
        raise ValueError(f"{PREFIX} could not find recipe for {item}")

    def __iadd__(self, other):
        """ Combine two cookbooks. """
        self.recipes += other.recipes
        return self

    def __str__(self):
        """ Return all of the recipes. """

        return ", ".join([str(item.material) for item in self.recipes])


class IronIngot(Recipe):
    """ Recipe for Iron Ingot. """
    def __init__(self):
        super().__init__([Input(material.IRON_ORE, 30)],
                         material.IRON_INGOT, 30)


class IronPlate(Recipe):
    """ Recipe for Iron Plate. """
    def __init__(self):
        super().__init__([Input(material.IRON_INGOT, 30)],
                        material.IRON_PLATE, 20)


class IronRod(Recipe):
    """ Recipe for Iron Rod. """
    def __init__(self):
        super().__init__([Input(material.IRON_INGOT, 15)],
                         material.IRON_ROD, 15)


class Screws(Recipe):
    """ Recipe for Screws. """
    def __init__(self):
        super().__init__([Input(material.IRON_ROD, 10)], material.SCREWS, 40)


class ReinforcedIronPlate(Recipe):
    """ Recipe for Reinforced Iron Plate. """
    def __init__(self):
        super().__init__([Input(material.IRON_PLATE, 30),
                          Input(material.SCREWS, 60)],
                         material.REINFORCED_IRON_PLATE, 5)


class ModularFrame(Recipe):
    """ Recipe for Reinforced Iron Plate. """
    def __init__(self):
        super().__init__([Input(material.REINFORCED_IRON_PLATE, 3),
                          Input(material.IRON_ROD, 12)],
                         material.MODULAR_FRAME, 2)


STANDARD = CookBook([IronIngot(), IronPlate(), IronRod(), Screws(),
                     ReinforcedIronPlate(), ModularFrame()])
