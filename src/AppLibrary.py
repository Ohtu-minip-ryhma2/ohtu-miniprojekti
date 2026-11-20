from app import App
from stub_io import StubIO


class AppLibrary:
    def __init__(self):
        self.io = StubIO()        

    def start_app(self):
        self.app = App(self.io)
        self.app.run()

    def input(self, value):
        self.io.add_input(value)

    def output_should_contain(self, value):
        assert value in self.io.output(), f"Expected output to contain '{value}', but it did not."

    def output_should_not_contain(self, value):
        assert value not in self.io.output(), f"Expected output to not contain '{value}', but it did."