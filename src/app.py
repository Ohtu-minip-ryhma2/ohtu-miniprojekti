class App:
    def __init__(self, io):
        self.io = io
    # Pääsilmukka, joka kysyy komentoja kunnes käyttäjä lopettaa
    def run(self):
        while True:
            command = self.io.read(
                "Komento (lisää) viite tai (tulosta) viiteluettelo: "
            )
	    # Tyhjä komento lopettaa ohjelman
            if not command:
                break

            if command == "lisää":
                self.lisaa_viite()

            elif command == "tulosta":
                self.io.write("Ei tulosta mitään")

            else:
                self.io.write("Tuntematon komento")

    def kysy_pakollinen(self, kysymys):
        # Kysytään tietoja kunnes tulee kelvollinen syöte
        while True:
            vastaus = self.io.read(kysymys).strip()

            if vastaus:
                return vastaus

            self.io.write("Virhe: Kenttä ei voi olla tyhjä.")

    def kysy_vuosi(self):
        # Kysytään vuosilukua, kunnes oikea muoto
        while True:
            vuosi = self.io.read("Vuosi: ").strip()

            if len(vuosi) == 4 and vuosi.isascii() and vuosi.isdigit():
                return int(vuosi)

            self.io.write(
                "Virhe: Vuoden täytyy olla nelinumeroinen luku."
            )

    def lisaa_viite(self):
        # Kysytään käyttäjältä pakolliset tiedot viitteeseen
        self.io.write("Lisätään uusi artikkeliviite")

        author = self.kysy_pakollinen("Kirjoittaja: ")
        title = self.kysy_pakollinen("Otsikko: ")
        year = self.kysy_vuosi()
        journal = self.kysy_pakollinen("Lehti/julkaisu: ")

        viite = {
	    # Kootaan annetut tiedot
            "type": "article",
            "author": author,
            "title": title,
            "year": year,
            "journal": journal
        }

        self.io.write("Viitteen tiedot hyväksytty.")

        # Palautetaan viite
        return viite
