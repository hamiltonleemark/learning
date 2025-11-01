class Input():
    def __init__(self, item, per_min):
        self.item = item
        self.per_min = per_min


class Output():
    def __init__(self, item, per_min):
        self.item = item
        self.per_min = per_min


class Recipe():
    def __init__(self, inputs, item, output_per_min):

        if not inputs:
            raise Value(f"{item} inputs none")

        if not output_per_min:
            raise Value(f"{item} output_per_min")

        self.inputs = inputs
        self.item = item
        self.output = Output(item, output_per_min)
