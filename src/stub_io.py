class StubIO:
    def __init__(self, inputs=None):
        self.inputs = inputs or []
        self.outputs = []

    def write(self, value):
        self.outputs.append(value)

    def add_input(self, value):
        self.inputs.append(value)

    def mamma(self, arvo):
        s
