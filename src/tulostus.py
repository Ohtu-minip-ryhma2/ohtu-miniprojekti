

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