import re
from pybtex.database import parse_string

from app import App
from stub_io import StubIO
from tietokanta import Tietokanta
from tulostus import Tulostus


class AppLibrary:
    ROBOT_LIBRARY_SCOPE = "TEST CASE"

    def __init__(self):
        self.io = StubIO()
        # Luodaan tietokanta muistiin, jotta testit eivät vaikuta toisiinsa
        self.tietokanta = Tietokanta(":memory:")
        self.tulostus = Tulostus(self.io)
        self.app = App(self.io, self.tietokanta, self.tulostus)

    def input(self, value):
        self.io.add_input(value)

    def output_should_contain(self, expected):
        output = self.get_output()
        assert expected in output, (
            f"Expected output to contain '{expected}', but it did not. It was: '{output}'"
        )

    def output_should_not_contain(self, unexpected):
        output = self.get_output()
        assert unexpected not in output, (
            f"Expected output to not contain '{unexpected}', but it did. It was: '{output}'"
        )

    def _parse_tags(self, tags):
        if not tags:
            return []
        if isinstance(tags, str):
            return [tag.strip().lower() for tag in tags.split(",") if tag.strip()]
        if isinstance(tags, (list, tuple)):
            return [str(tag).strip().lower() for tag in tags if str(tag).strip()]
        return [str(tags).strip().lower()]

    def _normalize_pages(self, pages):
        pages_str = str(pages).strip()
        if not pages_str:
            return ""
        match = re.fullmatch(r"([0-9]+)\s*[-–]{1,2}\s*([0-9]+)", pages_str)
        if match:
            return f"{match.group(1)}--{match.group(2)}"
        return pages_str

    def create_dict_for_testing_citation(self, author, title, year, publisher, pages="", tags=""):
        citation = {
            "type": "article",
            "author": author,
            "title": title,
            "year": year,
            "publisher": publisher,
            "pages": str(pages).strip(),
            "tags": self._parse_tags(tags),
        }
        self.io.create_dict_for_testing_citation(citation)

    def get_citation_dict(self, number_of_dict: int):
        if number_of_dict is None:
            raise AssertionError("Viitteen numero puuttuu testidictin hakemisesta.")
        return self.io.get_citation_dict(number_of_dict)

    def _check_db_citation(self, expected, db_citation):
        errors = []
        for field, label in [
            ("author", "tekijä"),
            ("title", "otsikko"),
            ("publisher", "julkaisija"),
        ]:
            if db_citation.get(field) != expected[field]:
                errors.append(
                    f"Tietokannan {label} ei täsmää: "
                    f"odotettiin '{expected[field]}', saatiin '{db_citation.get(field)}'."
                )

        if str(db_citation.get("year")) != str(expected["year"]):
            errors.append(
                f"Tietokannan vuosi ei täsmää: "
                f"odotettiin '{expected['year']}', saatiin '{db_citation.get('year')}'."
            )

        expected_pages = self._normalize_pages(expected.get("pages", ""))
        if expected_pages:
            actual_pages = self._normalize_pages(db_citation.get("pages") or "")
            if not actual_pages:
                errors.append(
                    f"Tietokannasta puuttuvat sivunumerot (pages): "
                    f"odotettiin '{expected_pages}', saatiin '{db_citation.get('pages')}'."
                )
            elif actual_pages != expected_pages:
                errors.append(
                    f"Tietokannan sivunumerot eivät täsmää: "
                    f"odotettiin '{expected_pages}', saatiin '{actual_pages}'."
                )

        expected_tags = expected.get("tags", [])
        if expected_tags:
            actual_tags_raw = db_citation.get("tags")
            if not actual_tags_raw:
                errors.append(
                    f"Tietokannasta puuttuvat tagit (tags): "
                    f"odotettiin {expected_tags}, saatiin '{actual_tags_raw}'."
                )
            else:
                actual_tags = self._parse_tags(actual_tags_raw)
                for tag in expected_tags:
                    if tag not in actual_tags:
                        errors.append(
                            f"Tietokannasta puuttuu tagi '{tag}': saatiin {actual_tags}."
                        )

        return errors

    def _get_expected_printed_index(self, citation_index: int) -> int:
        indexed_dicts = list(enumerate(self.io.cit_dicts, start=1))
        sorted_dicts = sorted(
            indexed_dicts,
            key=lambda item: self.tulostus.sukunimi_jarjestys(item[1]),
        )
        return next(
            pos for pos, (idx, _) in enumerate(sorted_dicts, start=1) if idx == citation_index
        )

    def _check_printed_citation(self, expected, printed_index, outputs):
        errors = []
        prefix = f"[{printed_index}] "
        matching_lines = [line for line in outputs if line.startswith(prefix)]
        if not matching_lines:
            return [f"Tulosteesta ei löytynyt riviä tunnisteella '{prefix}'. Tuloste oli: {outputs}"]
        citation_line = matching_lines[-1]

        for field, label in [
            ("author", "tekijä"),
            ("title", "otsikko"),
            ("publisher", "julkaisija"),
        ]:
            if expected[field] not in citation_line:
                errors.append(
                    f"Tulosteesta puuttuu {label} '{expected[field]}': '{citation_line}'."
                )

        if str(expected["year"]) not in citation_line:
            errors.append(f"Tulosteesta puuttuu vuosi '{expected['year']}': '{citation_line}'.")

        expected_pages = self._normalize_pages(expected.get("pages", ""))
        if expected_pages and (
            expected_pages not in citation_line and expected["pages"] not in citation_line
        ):
            errors.append(f"Tulosteesta puuttuvat sivut '{expected_pages}': '{citation_line}'.")

        for tag in expected.get("tags", []):
            if tag.lower() not in citation_line.lower():
                errors.append(f"Tulosteesta puuttuu tagi '{tag}': '{citation_line}'.")

        return errors

    def check_citations(self, citation_index: int):
        expected = self.get_citation_dict(citation_index)
        db_citations = self.tietokanta.hae_viitteet()
        outputs = self.get_output()

        if citation_index < 1 or citation_index > len(db_citations):
            raise AssertionError(
                f"Tietokannasta ei löytynyt viitettä numerolla {citation_index} "
                f"(tietokannassa {len(db_citations)} viitettä)."
            )

        printed_index = self._get_expected_printed_index(citation_index)
        errors = []
        errors.extend(self._check_db_citation(expected, db_citations[citation_index - 1]))
        errors.extend(self._check_printed_citation(expected, printed_index, outputs))

        if errors:
            raise AssertionError("\n".join(errors))

    def get_output(self):
        return self.io.get_outputs()

    def pop_one(self):
        self.io.read("")

    def run_application(self):
        self.app.run()

    def tarkista_bib_tiedosto(self, citation_index: int):
        """
        Tarkistaa pybtex-kirjastolla, että BibTeX-tiedostoon (streamiin) kirjoitettu viite
        vastaa testidictin odotettuja tietoja.
        """
        expected = self.get_citation_dict(citation_index)
        bib_content = self.io.give_stream().getvalue()
        if not bib_content.strip():
            raise AssertionError("BibTeX-tiedosto (stream) on tyhjä.")

        bib_data = parse_string(bib_content, "bibtex")
        entries = list(bib_data.entries.values())
        if citation_index < 1 or citation_index > len(entries):
            raise AssertionError(
                f"BibTeX-tiedostosta ei löytynyt viitettä numerolla {citation_index} "
                f"(tiedostossa {len(entries)} viitettä)."
            )

        entry = entries[citation_index - 1]
        errors = []

        if not entry.persons.get("author"):
            errors.append(
                f"BibTeX-tiedostosta puuttuu tekijä (odotettiin '{expected['author']}')."
            )
        else:
            person = entry.persons["author"][0]
            parsed_author = " ".join(
                person.first_names
                + person.middle_names
                + person.prelast_names
                + person.last_names
                + person.lineage_names
            )
            if parsed_author != expected["author"]:
                errors.append(
                    f"BibTeX-tiedoston tekijä ei täsmää: "
                    f"odotettiin '{expected['author']}', saatiin '{parsed_author}'."
                )

        if entry.fields.get("title") != expected["title"]:
            errors.append(
                f"BibTeX-tiedoston otsikko ei täsmää: "
                f"odotettiin '{expected['title']}', saatiin '{entry.fields.get('title')}'."
            )

        if str(entry.fields.get("year")) != str(expected["year"]):
            errors.append(
                f"BibTeX-tiedoston vuosi ei täsmää: "
                f"odotettiin '{expected['year']}', saatiin '{entry.fields.get('year')}'."
            )

        if entry.fields.get("publisher") != expected["publisher"]:
            errors.append(
                f"BibTeX-tiedoston julkaisija ei täsmää: "
                f"odotettiin '{expected['publisher']}', saatiin '{entry.fields.get('publisher')}'."
            )

        expected_pages = self._normalize_pages(expected.get("pages", ""))
        if expected_pages:
            actual_pages = self._normalize_pages(entry.fields.get("pages") or "")
            if not actual_pages:
                errors.append(
                    f"BibTeX-tiedostosta puuttuu 'pages'-kenttä (odotettiin '{expected_pages}')."
                )
            elif actual_pages != expected_pages:
                errors.append(
                    f"BibTeX-tiedoston sivunumerot eivät täsmää: "
                    f"odotettiin '{expected_pages}', saatiin '{actual_pages}'."
                )

        expected_tags = expected.get("tags", [])
        if expected_tags:
            actual_tags_raw = entry.fields.get("keywords") or entry.fields.get("tags")
            if not actual_tags_raw:
                errors.append(
                    f"BibTeX-tiedostosta puuttuvat tagit ('keywords'/'tags'-kenttä, "
                    f"odotettiin {expected_tags})."
                )
            else:
                actual_tags = self._parse_tags(actual_tags_raw)
                for tag in expected_tags:
                    if tag not in actual_tags:
                        errors.append(
                            f"BibTeX-tiedostosta puuttuu tagi '{tag}': saatiin {actual_tags}."
                        )

        if errors:
            raise AssertionError("\n".join(errors))

