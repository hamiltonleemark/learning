import satisfactory
import material

class IronIngot(satisfactory.Recipe):
    def __init__(self):
        super().__init__(satisfactory.Input(material.IRON_ORE, 30),
                         material.IRON_INGOT, 30)


class IronPlate(satisfactory.Recipe):
    def __init__(self):
        super().__init__(satisfactory.Input(material.IRON_INGOT, 30),
                         material.IRON_PLATE, 20)
