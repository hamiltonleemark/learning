
IMPURE = 0.5
NORMAL = 1.0
PURE = 2.0


class Ifc():
    def __init__(self, speed, material, purity):
        self.speed = speed
        self.material = material
        self.purity = purity
        self.per_min = speed * purity


class MK1(Ifc):
    def __init__(self, material, purity):
        super().__init__(60, material, purity)


class MK2(Ifc):
    def __init__(self, material, purity):
        super().__init__(120, material, purity)


class MK3(Ifc):
    def __init__(self, material, purity):
        super().__init__(240, material, purity)
