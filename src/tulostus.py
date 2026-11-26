from pathlib import Path
import re
import unicodedata

class Tulostus:
    def __init__(self, Io):
        self.io = Io
        self.stream = self.io.give_stream()
        
    def tulosta_viitteet(self, viitteet):
        """Tulostaa viitteet terminaaliin.

        Viitteet tulostetaan samalla tyylillä kuin mallissa. Numeroidussa listassa, viitteiden
        välillä tyhjä rivi. Lopussa [] sisällä tägit Esimerkki tulosteesta:

        [1] Matti Meikäläinen and Aku Ankka. Astronomian uusi suosio. Ankkalinnan tiede, 55-60, 2020 [Astronomia]

        Args:
            viitteet: Lista sanakirjoja, jossa avaimina "author", "title" "year" "publisher"
        """
        if not viitteet:
            self.io.write("Viitteitä ei löydy")
            return

        self.io.write("")
        jarjestetyt_viitteet = self.jarjesta_viitteet(viitteet)

        for numero, viite in enumerate(jarjestetyt_viitteet, start=1):
            listanumero = f"[{numero}] "
            teksti = listanumero + self.muotoile_tulostettava_viite(viite)
            self.io.write(teksti)
            self.io.write("")

    def muotoile_tulostettava_viite(self, viite):
         """Muotoilee viitteen tekstiksi, järjestys: Kirjoittajat, otsikko, julkaisija, sivut, vuosi, [tagit]
         TO DO: Katsotaan miten tietokannassa tallennetaan tagit
         """
         kirjoittajat = self.muotoile_kirjoittajat(viite['author'])

         otsikko = viite['title']

         loppuosat = [viite['publisher']]
         if viite.get('pages'):
              loppuosat.append(viite['pages'])
         loppuosat.append(str(viite['year']))
         if viite.get('tags'):
              loppuosat.append(f"[{viite['tags']}]")

         return f"{kirjoittajat}. {otsikko} {', '.join(loppuosat)}."


    def muotoile_kirjoittajat(self, kirjoittajat):
         """Muotoilee kirjoittajat muotoon "Etunimi1 Sukunimi1, Etunimi2 Sukunimi2, ... and Etunimin Sukunimin"
         TO DO: Katsotaan miten tietokannasta tulee nämä.
         """
         return kirjoittajat

    def sukunimi_jarjestys(self, viite):
         """Palauttaa jarjesta_viitteed sortedissä käytettävän verrokin.

         Args:
            viite: Viite jota tutkitaan

        Returns:
            verrokki
         """

         ensimmainen_kirjoittaja = viite["author"].split(",")[0].strip()
         osat = ensimmainen_kirjoittaja.split()
         sukunimi = osat[-1]
         etunimet = " ".join(osat[:-1])

         return (sukunimi.casefold(), etunimet.casefold(), viite["title"].casefold())

    def jarjesta_viitteet(self, viitteet):
         """Järjestää viitteet aakkosjärjestykseen ensin ensimmäisen kirjoittajan sukunimen, sitten etunimen,
         sitten viitteen otsikon mukaan. Isoilla ja pienillä kirjaimilla ei ole merkitystä.

         Args:
            viitteet: Lista sanakirjoja.

         Returns:
            Uusi, järjestetty lista.
         """
         return sorted(viitteet, key=self.sukunimi_jarjestys)


    def luo_bib(self, tiedosto_nimi, tietokanta):
            """Tekee viitteistä .bib tiedoston

            Ei luo tiedostoa, jos tietokannassa ei ole yhtään viitettä.
            Varoittaa ja lopettaa toiminnan jos samanniminen tiedosto on jo olemassa.
            Laittaa terminaaliin viestin, jos kaikki onnistui.

            Args:
                tiedosto_nimi: Halutun .bib tiedoston nimi, ilman .bib päätettä.
                tietokanta: Tietokanta, josta haetaan.
                stream: Jos annettu, kirjoitetaan bib-tiedosto streamiin, ei tiedostoon.
                testejä varten.
            """

            viitteet = tietokanta.hae_viitteet()

            if not viitteet:
                self.io.write("Viitteitä ei löydy.")
                return

            polku = Path(f"{tiedosto_nimi}.bib")
            if polku.exists():
                self.io.write(f"Tiedosto {polku} on jo olemassa. Valitse muu nimi.")
                return

            kaytetyt_avaimet = set()
            Bibtex_viitteet = []

            for viite in viitteet:
                avain = self.luo_bib_avain(viite, kaytetyt_avaimet)
                kaytetyt_avaimet.add(avain)
                Bibtex_viitteet.append(self.muotoile_bib_viite(viite, avain))

            sisalto = "\n".join(Bibtex_viitteet)

            # Jos stream on annettu, kirjoitetaan bib-tiedosto streamiin, muuten tiedostoon.
            if self.stream is not None:
                self.stream.write(sisalto)
            else:
                with open(polku, "w", encoding="utf-8") as tiedosto:
                    tiedosto.write(sisalto)

            self.io.write(f"Viitteet tallennettu tiedostoon {polku}")


    def luo_bib_avain(self, viite, kaytetyt_avaimet):
            """Luo viitteelle uniikin avaimen, käyttäen viitteen ensimmäisen nimen 3:a
            ensimmäistä kirjainta + vuosilukua. Jos avain on jo käytössä, laitetaan
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

            ensimmainen_nimi = unicodedata.normalize("NFKD", ensimmainen_nimi).encode("ascii", "ignore").decode()
            ensimmainen_nimi = re.sub(r"[^A-Za-z]", "", ensimmainen_nimi)

            pohja = f"{ensimmainen_nimi[:3].capitalize()}{viite['year']}"
            avain = pohja
            numero = 2

            while avain in kaytetyt_avaimet:
                avain = f"{pohja}_{numero}"
                numero += 1

            return avain


    def muotoile_bib_viite(self, viite, avain):
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