import satisfactory
import material

class IronIngot(satisfactory.Recipe):
    def __init__(self):
        super().__init__(
            [satisfactory.Input(material.IRON_ORE, 30)],
            material.IRON_INGOT, 30)


class IronPlate(satisfactory.Recipe):
    def __init__(self):
        super().__init__(
            [satisfactory.Input(material.IRON_INGOT, 30)],
            material.IRON_PLATE, 20)


class IronRod(satisfactory.Recipe):
    def __init__(self):
        super().__init__(
            [satisfactory.Input(material.IRON_INGOT, 15)],
            material.IRON_ROD, 15)


class Screws(satisfactory.Recipe):
    def __init__(self):
        super().__init__(
            [satisfactory.Input(material.IRON_ROD, 10)],
            material.SCREWS, 40)


class ReinforcedIronPlate(satisfactory.Recipe):
    def __init__(self):
        super().__init__(
            [satisfactory.Input(material.IRON_PLATE, 10),
             satisfactory.Input(material.SCREWS, 60)],
             material.REINFORCED_IRON_PLATE, 40)
