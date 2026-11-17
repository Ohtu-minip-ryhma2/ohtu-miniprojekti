class App:
    def __init__(self, io):
        self.io = io

    def run(self):
        while True:
            command = self.io.read("Komento (lisää) viite tai (tulosta) viiteluettelo: ")

            if not command:
                break

            if command == "lisää":
                self.io.write("Ei lisää mitään")

            elif command == "tulosta":
                self.io.write("Ei tulosta mitään")
