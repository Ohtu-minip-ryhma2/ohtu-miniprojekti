class ConsoleIO:
    """Tehty oma io luokka konsolikäyttöönlittymälle. Tälle kun
   tekee sitten mock-luokan testeille, niin onnistuu asiat helpommin siinä """
    def write(self, value):
        print(value)

    def read(self, prompt):
        return input(prompt)
