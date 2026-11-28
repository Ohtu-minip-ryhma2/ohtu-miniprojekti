from io import StringIO


class StubIO:
    def __init__(self, inputs=None, stream=None):
        self.inputs = inputs if inputs is not None else []
        self.outputs = []
        self.stream = stream if stream is not None else StringIO()
        self.cit_dicts = []  # Lista, johon tallennetaan luodut viitedictit testeihin

    def write(self, value):
        self.outputs.append(value)

    def add_input(self, value):
        self.inputs.append(value)

    def read(self, prompt):
        if len(self.inputs) > 0:
            return self.inputs.pop(0)
        raise Exception("No more inputs available in StubIO.")

    def give_stream(self):
        return self.stream

    def get_outputs(self):
        return self.outputs

    def create_dict_for_testing_citation(self, citation):
        self.cit_dicts.append(citation)

    def get_citation_dict(self, number_of_dict):
        # Palautetaan viitedict sillä numerolla mitä haetaan (1-pohjainen indeksi,
        # jotta se vastaa tulosteen numerointia [1], [2], ...).
        index = int(number_of_dict) - 1
        if index < 0 or index >= len(self.cit_dicts):
            raise IndexError(
                f"Testiviitettä numerolla {number_of_dict} ei löydy (tallennettu {len(self.cit_dicts)} kpl)."
            )
        return self.cit_dicts[index]
