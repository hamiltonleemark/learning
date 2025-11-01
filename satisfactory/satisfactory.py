class Input():
    def __init__(self, item, per_min):
        self.item = item
        self.per_min = per_min


class Output():
    def __init__(self, item, per_min):
        self.item = item
        self.per_min = per_min


class Recipe():
    def __init__(self, item, inputs=None, outputs=None):

        self.item = item
        self.inputs = inputs
        self.outputs = outputs

        if not self.input:
            raise Value(f"{item} input none")
        if not self.output:
            raise Value(f"{item} output none")
