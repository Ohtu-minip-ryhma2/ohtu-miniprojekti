from app import App
from stub_io import StubIO


class TestApp:

    def test_yksi_tagi(self):
        # Testataan yhden tagin syöttäminen
        io = StubIO(["Python"])
        app = App(io, None, None)

        assert app.kysy_tagit() == ["python"]

    def test_useita_tageja(self):
        # Testataan usean tagin syöttäminen
        io = StubIO(["Python, Testaus"])
        app = App(io, None, None)

        assert app.kysy_tagit() == ["python", "testaus"]

    def test_tyhjät_tagit(self):
        # Testataan tagien ohittaminen
        io = StubIO([""])
        app = App(io, None, None)

        assert app.kysy_tagit() == []

    def test_tagien_valilyonnit(self):
        # Testataan ylimääräisten välilyöntien poistaminen
        io = StubIO([" Python , Testaus "])
        app = App(io, None, None)

        assert app.kysy_tagit() == ["python", "testaus"]

    def test_tyhja_tagi_listassa(self):
        # Testataan tyhjien tagien poistaminen
        io = StubIO(["python,,testaus"])
        app = App(io, None, None)

        assert app.kysy_tagit() == ["python", "testaus"]

    def test_yksi_sivunumero(self):
        # Testataan yksittäinen sivunumero
        io = StubIO(["15"])
        app = App(io, None, None)

        assert app.kysy_sivunumerot() == "15"

    def test_sivuvali(self):
        # Testataan sivuvälin muuttaminen BibTeX-muotoon
        io = StubIO(["10-25"])
        app = App(io, None, None)

        assert app.kysy_sivunumerot() == "10--25"

    def test_bibtex_sivuvali(self):
        # Testataan valmiiksi oikeassa muodossa oleva sivuväli
        io = StubIO(["10--25"])
        app = App(io, None, None)

        assert app.kysy_sivunumerot() == "10--25"

    def test_tyhjät_sivunumerot(self):
        # Testataan sivunumeroiden ohittaminen
        io = StubIO([""])
        app = App(io, None, None)

        assert app.kysy_sivunumerot() == ""

    def test_virheellinen_sivuvali(self):
        # Annetaan ensin virheellinen ja sitten oikea sivuväli
        io = StubIO(["25-10", "10-25"])
        app = App(io, None, None)

        assert app.kysy_sivunumerot() == "10--25"
        assert "Virhe: Anna kelvollinen sivunumero tai sivuväli." in io.get_outputs()

    def test_virheellinen_sivunumero(self):
        # Annetaan ensin tekstiä ja sitten oikea sivunumero
        io = StubIO(["abc", "15"])
        app = App(io, None, None)

        assert app.kysy_sivunumerot() == "15"
        assert "Virhe: Anna kelvollinen sivunumero tai sivuväli." in io.get_outputs()

    def test_vapaaehtoinen_kentta(self):
        # Testataan vapaaehtoisen kentän ohittaminen
        io = StubIO([""])
        app = App(io, None, None)

        assert app.kysy_vapaaehtoinen("Testi: ") == ""

    def test_viite_vapaaehtoisilla_kentilla(self):
        # Testataan viitteen muodostaminen kaikilla tiedoilla
        io = StubIO([
            "Maija Meikäläinen",
            "Testiartikkeli",
            "2026",
            "Testijulkaisu",
            "10-25",
            "Python, Testaus"
        ])

        app = App(io, None, None)
        viite = app.lisaa_viite()

        assert viite == {
            "type": "article",
            "author": "Maija Meikäläinen",
            "title": "Testiartikkeli",
            "year": 2026,
            "publisher": "Testijulkaisu",
            "pages": "10--25",
            "tags": ["python", "testaus"]
        }

    def test_viite_ilman_vapaaehtoisia_kenttia(self):
        # Testataan viitteen muodostaminen vain pakollisilla tiedoilla
        io = StubIO([
            "Maija Meikäläinen",
            "Testiartikkeli",
            "2026",
            "Testijulkaisu",
            "",
            ""
        ])

        app = App(io, None, None)
        viite = app.lisaa_viite()

        assert viite["pages"] == ""
        assert viite["tags"] == []

    def test_pakollinen_kentta(self):
        # Testataan kelvollinen syöte
        io = StubIO(["Maija Meikäläinen"])
        app = App(io, None, None)

        assert app.kysy_pakollinen("Kirjoittaja: ") == "Maija Meikäläinen"

    def test_tyhja_pakollinen_kentta(self):
        # Testataan tyhjän syötteen hylkääminen
        io = StubIO(["", "Maija"])
        app = App(io, None, None)

        assert app.kysy_pakollinen("Kirjoittaja: ") == "Maija"
        assert "Virhe: Kenttä ei voi olla tyhjä." in io.get_outputs()

    def test_pakollinen_kentta_valilyonneilla(self):
        # Testataan pelkkien välilyöntien hylkääminen
        io = StubIO(["   ", "Maija"])
        app = App(io, None, None)

        assert app.kysy_pakollinen("Kirjoittaja: ") == "Maija"
        assert "Virhe: Kenttä ei voi olla tyhjä." in io.get_outputs()

    def test_kelvollinen_vuosi(self):
        # Testataan oikean vuosiluvun hyväksyminen
        io = StubIO(["2026"])
        app = App(io, None, None)

        assert app.kysy_vuosi() == 2026

    def test_virheellinen_vuoden_pituus(self):
        # Testataan liian lyhyt ja liian pitkä vuosiluku
        io = StubIO(["26", "20260", "2026"])
        app = App(io, None, None)

        assert app.kysy_vuosi() == 2026
        assert io.get_outputs().count(
            "Virhe: Vuoden täytyy olla nelinumeroinen luku."
        ) == 2

    def test_vuosi_sisaltaa_kirjaimia(self):
        # Testataan kirjaimia sisältävän vuosiluvun hylkääminen
        io = StubIO(["20ab", "2026"])
        app = App(io, None, None)

        assert app.kysy_vuosi() == 2026
        assert "Virhe: Vuoden täytyy olla nelinumeroinen luku." in io.get_outputs()