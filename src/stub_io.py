from io import StringIO

class StubIO:
    def __init__(self, inputs=None, stream=None):
        self.inputs = inputs or []
        self.outputs = []
        self.stream = stream if stream is not None else StringIO()

    def write(self, value):
        self.outputs.append(value)

    def add_input(self, value):
        self.inputs.append(value)

    def read(self, prompt):
        if len(self.inputs) > 0:
            return self.inputs.pop(0)
        else:
            raise Exception("No more inputs available in StubIO.")

    def give_stream(self):
        return self.stream

    def get_outputs(self):
        return self.outputs 
