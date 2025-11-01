import satisfactory
import material

class IronIngot:
    def __init__(self):
        self.name = material.IRON_INGOT
        self.input = satisfactory.Input(material.IRON_ORE, 30)
        self.output = satisfactory.Output(material.IRON_INGOT, 30)
        
        
