class Input():
    def __init__(self, item, per_min):
        self.item = item
        self.per_min = per_min


class Output():
    def __init__(self, item, per_min):
        self.item = item
        self.per_min = per_min


class Recipe():
    def __init__(self, item, rinput, output_per_min):

        if not rinput:
            raise Value(f"{item} input none")

        if not output_per_min:
            raise Value(f"{item} output_per_min")

        self.item = item
        self.input = input
        self.output = Output(item, output_per_min)
