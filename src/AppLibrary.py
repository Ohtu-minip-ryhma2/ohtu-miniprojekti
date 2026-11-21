from app import App
from stub_io import StubIO
from tietokanta import Tietokanta
from tulostus import Tulostus
from pybtex.database import parse_string

class AppLibrary:
    ROBOT_LIBRARY_SCOPE = "TEST CASE"
    def __init__(self):
        self.io = StubIO()
        self.tietokanta = Tietokanta(":memory:") # luodaan tietokanta muistiin, jotta testit eivät vaikuta toisiinsa
        self.tulostus = Tulostus(self.io)
        self.app = App(self.io, self.tietokanta, self.tulostus)

    def input(self, value):
        self.io.add_input(value)

    def output_should_contain(self, expected):
        output = self.get_output()
        assert expected in output, f"Expected output to contain '{expected}', but it did not. It was: '{output}'"

    def output_should_not_contain(self, unexpected):
        output = self.get_output()
        assert unexpected not in output, f"Expected output to not contain '{unexpected}', but it did. It was: '{output}'"

    def get_output(self):
        return self.io.get_outputs()

    def pop_one(self):
        self.io.read("")

    def run_application(self):
        self.app.run()

        """
        Tämä meni hieman monimutkaiseksi, koska tarvitaan lisäpalikoita mitkä tarkistaa BibTex-tiedoston sisällön.
        Käytetään pybtex-kirjastoa, joka osaa parsia BibTeX-tiedostoja. Author homma hieman hankala, koska pybtex parsii authorin listaksi.
        """
    def check_bib_file(self, author, title, year, publisher):
        # Haetaan bib-tiedoston sisältö streamistä
        bib_content = self.io.give_stream().getvalue()
        # Parsitaan bib-tiedosto
        bib_data = parse_string(bib_content, "bibtex")
        # Tarkistetaan, että viite löytyy ja sen tiedot ovat oikein
        #self.io.write(f"Bib-tiedoston sisältö:\n{bib_data}")  # Debug-tulostus
        
        assert len(bib_data.entries) == 1, f"Expected 1 entry in bib file, but found {len(bib_data.entries)}"
        entry = list(bib_data.entries.values())[0]
        person = entry.persons["author"][0]
        parsed_author = " ".join(person.first_names + person.last_names)
        assert parsed_author == author, f"Expected author '{author}', but found '{parsed_author}'"
        assert entry.fields["title"] == title, f"Expected title '{title}', but found '{entry.fields['title']}'"
        assert entry.fields["year"] == year, f"Expected year '{year}', but found '{entry.fields['year']}'"
        assert entry.fields["publisher"] == publisher, f"Expected publisher '{publisher}', but found '{entry.fields['publisher']}'"
        
        