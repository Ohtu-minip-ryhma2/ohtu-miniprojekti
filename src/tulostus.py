from pathlib import Path
import re
import unicodedata

class Tulostus:
    def __init__(self, Io):
        self.io = Io
        
    def tulosta_viitteet(viitteet):
        """Tulostaa viitteet terminaaliin.

        Jokainen viite tulostetaan kenttä kerrallaan omille riveilleen ja
        viitteiden väliin jätetaan tyhjä rivi. Esimerkki tuloste:

        Kirjoittajat: Matti Meikalainen, Aku Ankka
        Otsikko: Ankkalinnan asuntojen hintojen muutos välilla 1960-2000
        Vuosi: 2010
        Julkaisu: Ankkalinnan Tiede

        Args:
            viitteet: Lista sanakirjoja, jossa avaimina "author", "title" "year" "publisher"
            TO DO: yhdistetään SQL kantaan, tässä kömpelösti tehty tynkä alkuun.
        """

        for viite in viitteet:
            print(f"Kirjoittajat: {viite['author']}")
            print(f"Otsikko: {viite['title']}")
            print(f"Vuosi: {viite['year']}")
            print(f"Julkaisu: {viite['publisher']}")
            print()


        def luo_bib(tiedosto_nimi, tietokanta):
            """Tekee viitteistä .bib tiedoston

            Ei luo tiedostoa, jos tietokannassa ei ole yhtään viitettä.
            Varoittaa ja lopettaa toiminnan jos samanniminen tiedosto on jo olemassa.
            Laittaa terminaaliin viestin, jos kaikki onnistui.

            Args:
                tiedosto_nimi: Halutun .bib tiedoston nimi, ilman .bib päätettä.
                tietokanta: Tietokanta, josta haetaan.
            """

            viitteet = tietokanta.hae_viitteet()

            if not viitteet:
                print("Viitteitä ei löydy.")
                return

            polku = Path(f"{tiedosto_nimi}.bib")
            if polku.exists():
                print(f"Tiedosto {tiedosto_nimi}.bib on jo olemassa. Valitse muu nimi.")
                return

            kaytetyt_avaimet = set()
            Bibtex_viitteet = []

            for viite in viitteet:
                avain = luo_bib_avain(viite, kaytetyt_avaimet)
                kaytetyt_avaimet.add(avain)
                Bibtex_viitteet.append(muotoile_bib_viite(viite, avain))

            with open(polku, "w", encoding="utf-8") as tiedosto:
                tiedosto.write("\n".join(Bibtex_viitteet))

            print (f"Viitteet tallennettu tiedostoon {polku}")


        def luo_bib_avain(viite, kaytetyt_avaimet):
            """Luo viitteelle uniikin avaimen, käyttäen viitteen ensimmäisen nimen 3:a
            ensimmäistä kirjainta + vuosilukua. Jos vuosiluku on jo käytössä, laitetaan
            perään _2, _3 jne. Nimestä poistetaan ääkköset ja muut ei-kirjaimet.

            Esim. Matti Virtasen 1993 tehty lähde olisi "Mat1993".
            Toinen lähde samalta vuodelta olisi "Mat1993_2".

            Args:
                viite: Viite sanakirjana.
                kaytetyt_avaimet: Kaikki avaimet, jotka on jo käytetty.

            Returns:
                uniikki avain.
            """
            ensimmainen_nimi = viite["author"].split()[0]

            ensimmainen_nimi = unicodedata.normalize("NKFD", ensimmainen_nimi).encode("ascii", "ignore").decode()
            ensimmainen_nimi = re.sub(r"[^A-Za-Z]", "", ensimmainen_nimi)

            pohja = f"{ensimmainen_nimi[:3].capitalize()}{viite['year']}"
            avain = pohja
            numero = 2

            while avain in kaytetyt_avaimet:
                avain = f"{pohja}_{numero}"
                numero += 1

            return avain


        def muotoile_bib_viite(viite, avain):
            """ Muotoilee viitteen BibTeX-muotoiseksi.

            Args:
                viite: Viite sanakirjaan.
                avain: Viitteen uniikki avain.

            Returns:
                BibTeX muotoinen merkkijono.
            """
            return (
                f"@book{{{avain},\n"
                f"  author     = {{{viite['author']}}},\n"
                f"  title      = {{{viite['title']}}},\n"
                f"  year       = {viite['year']},\n"
                f"  publisher  = {{{viite['publisher']}}},\n"
                f"}}\n"
            )