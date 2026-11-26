import sys
import re

class App:
    def __init__(self, io, tietokanta, tulostus):
        self.io = io
        self.tietokanta = tietokanta
        self.tulostus = tulostus

    # Pääsilmukka, joka kysyy komentoja kunnes käyttäjä lopettaa
    def run(self):
        while True:
            command = self.io.read(
                "Komento (lisää) viite, (tulosta) viiteluettelo tai luo (bib) tiedosto. (exit) lopettaa: "
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
                try:
                    nimi = self.kysy_pakollinen("Tiedoston nimi (ilman .bib): ")
                    self.tulostus.luo_bib(nimi, self.tietokanta)
                except Exception as e:
                    self.io.write(f"Virhe tulostettaessa bib-tiedostoa: {e}")

            elif command == "exit":
                sys.exit()

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

    def kysy_tagit(self):
        # Kysytään vapaaehtoiset tagit pilkulla eroteltuna
        vastaus = self.kysy_vapaaehtoinen(
            "Tagit (pilkulla eroteltuna): "
        )

        # Poistetaan ylimääräiset välilyönnit ja tyhjät tagit
        tagit = [
            tagi.strip().lower()
            for tagi in vastaus.split(",")
            if tagi.strip()
        ]

        return tagit

    def kysy_vapaaehtoinen(self, kysymys):
        # Kysytään tieto, jonka voi jättää tyhjäksi
        return self.io.read(kysymys).strip()
    
    def kysy_sivunumerot(self):
        # Kysytään vapaaehtoiset sivunumerot
        while True:
            pages = self.kysy_vapaaehtoinen(
                "Sivunumerot (esim. 10-25): "
            )

            if not pages:
                return ""

            if re.fullmatch(r"[0-9]+", pages):
                return pages

            valit = re.fullmatch(
                r"([0-9]+)\s*[-–]{1,2}\s*([0-9]+)", pages
            )

            if valit:
                alku, loppu = valit.groups()

                if int(alku) <= int(loppu):
                    return f"{alku}--{loppu}"

            self.io.write(
                "Virhe: Anna kelvollinen sivunumero tai sivuväli."
            )

    def lisaa_viite(self):
        # Kysytään käyttäjältä pakolliset tiedot viitteeseen
        self.io.write("Lisätään uusi viite")

        author = self.kysy_pakollinen("Kirjoittaja: ")
        title = self.kysy_pakollinen("Otsikko: ")
        year = self.kysy_vuosi()
        publisher = self.kysy_pakollinen("Julkaisija: ")

        # Kysytään vapaaehtoiset tiedot
        self.io.write(
            "Vapaaehtoiset kentät voi ohittaa painamalla Enteriä."
        )

        pages = self.kysy_sivunumerot()
        tags = self.kysy_tagit()

        # Kootaan annetut tiedot
        viite = {
            "type": "article",
            "author": author,
            "title": title,
            "year": year,
            "publisher": publisher,
            "pages": pages,
            "tags": tags
        }

        return viite
