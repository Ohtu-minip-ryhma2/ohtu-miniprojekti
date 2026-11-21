class App:
    def __init__(self, io, tietokanta, tulostus):
        self.io = io
        self.tietokanta = tietokanta
        self.tulostus = tulostus

    # Pääsilmukka, joka kysyy komentoja kunnes käyttäjä lopettaa
    def run(self):
        while True:
            command = self.io.read(
                "Komento (lisää) viite, (tulosta) viiteluettelo tai luo (bib) tiedosto: "
            )
	    # Tyhjä komento lopettaa ohjelman
            if not command:
                break

            if command == "lisää":
                viite = self.lisaa_viite()
                try:
                    self.tietokanta.lisaa_viite(viite)
                    self.io.write("Viitteen tiedot hyväksytty.")
                except Exception as e:
                    self.io.write(f"Virhe lisättäessä viitettä: {e}")

            elif command == "tulosta":
                try:
                    viitteet = self.tietokanta.hae_viitteet()
                    self.tulostus.tulosta_viitteet(viitteet)
                except Exception as e:
                    self.io.write(f"Virhe tulostaessa viitteitä: {e}")

            elif command == "bib":
                nimi = self.kysy_pakollinen("Tiedoston nimi (ilman .bib): ")
                self.tulostus.luo_bib(nimi, self.tietokanta)
            
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
        #journal = self.kysy_pakollinen("Lehti/julkaisu: ")
        publisher = self.kysy_pakollinen("Julkaisija: ")

        viite = {
	    # Kootaan annetut tiedot
        # muutettu että on yhteensopiva tietokanta.py kanssa
        # TODO keskustellaan, mitä kaikkiea pitää olla tässä
            "type": "article",
            "author": author,
            "title": title,
            "year": year,
            "publisher": publisher
        }

    
        # Palautetaan viite
        return viite
