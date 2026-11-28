*** Settings ***
Resource    resource.robot

# Testirungot määritelty tämän tiedoston lopussa, josta voi katso mitä kirjatietoja ne tarkemmin ovat
# Testit kutsuvat aluksi runkoa ja tekevät sen jälkeen varsinaisen testattavan toiminnon.

*** Test Cases ***
1 viite: lisääminen onnistuu
    Lisää Harry Potter Viitenro 1
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tulostuksessa Pitäisi Olla    Lisätään uusi viite
    Tulostuksessa Pitäisi Olla    Vapaaehtoiset kentät voi ohittaa painamalla Enteriä.
    Tulostuksessa Pitäisi Olla    Viitteen tiedot hyväksytty.

1 viite: tulostus ilman sivuja ja tageja
    Lisää Harry Potter Viitenro 1
    Tulosta Viitteet
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Viitteet    1

1 viite: tulostus kun sivuja lisätään
    Lisää Harry Potter Viitenro 1    pages=12-24
    Tulosta Viitteet
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Viitteet    1

1 viite: tulostus kun tageja lisätään
    Lisää Harry Potter Viitenro 1    tags=Best
    Tulosta Viitteet
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Viitteet    1

1 viite: bib-tiedosto ilman sivuja tai tageja
    Lisää Harry Potter Viitenro 1
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1

1 viite: bib-tiedosto kun lisätään tageja
    Lisää Harry Potter Viitenro 1    tags=Best
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1

1 viite: bib-tiedosto kun lisätään sivuja
    Lisää Harry Potter Viitenro 1    pages=12-24
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1

1 viite: bib-tiedosto kun lisätään sivuja ja tageja
    Lisää Harry Potter Viitenro 1    pages=12-24    tags=Best
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1

3 viitettä: tulostus ilman sivuja ja tageja
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3
    Tulosta Viitteet
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Viitteet    1
    Tarkista Viitteet    2
    Tarkista Viitteet    3


3 viitettä: tulostus kun sivuja lisätään
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3    pages=12-24
    Tulosta Viitteet
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Viitteet    1
    Tarkista Viitteet    2
    Tarkista Viitteet    3

3 viitettä: tulostus kun tageja lisätään
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3    tags=Best
    Tulosta Viitteet
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Viitteet    1
    Tarkista Viitteet    2
    Tarkista Viitteet    3

3 viitettä: bib-tiedosto ilman sivuja tai tageja
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1
    Tarkista Bib Tiedosto    2
    Tarkista Bib Tiedosto    3

3 viitettä: bib-tiedosto kun lisätään tageja
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3    tags=Best
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1
    Tarkista Bib Tiedosto    2
    Tarkista Bib Tiedosto    3

3 viitettä: bib-tiedosto kun lisätään sivuja
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3    pages=12-24
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1
    Tarkista Bib Tiedosto    2
    Tarkista Bib Tiedosto    3


3 viitettä: bib-tiedosto kun lisätään sivuja ja tageja
    Lisää Harry Potter Viitenro 1
    Lisää Leviathan Wakes Viitenro 2
    Lisää Bat Eater Viitenro 3    12-24    Best
    Luo Bib Tiedosto
    Pois Komentoriviltä
    Käynnistä Ohjelma
    Tarkista Bib Tiedosto    1
    Tarkista Bib Tiedosto    2
    Tarkista Bib Tiedosto    3


*** Keywords ***
Lisää Harry Potter Viitenro 1
    [Arguments]    ${pages}=${EMPTY}    ${tags}=${EMPTY}
    Kirjoita Komentoriville    lisää
    Lisätään Viitteen Tiedot    J.K. Rowling    Harry Potter ja viisasten kivi    1997    Otava    ${pages}    ${tags}

Lisää Leviathan Wakes Viitenro 2
    [Arguments]    ${pages}=${EMPTY}    ${tags}=${EMPTY}
    Kirjoita Komentoriville    lisää
    Lisätään Viitteen Tiedot    James S.A. Coresy    Leviathan Wakes    2011    Orbit Books    ${pages}    ${tags}

Lisää Bat Eater Viitenro 3
    [Arguments]    ${pages}=${EMPTY}    ${tags}=${EMPTY}
    Kirjoita Komentoriville    lisää
    Lisätään Viitteen Tiedot    Kyle Lee Baker    Bat Eater and Other Names for Cora Zeng    2025    MIRA    ${pages}    ${tags}

Luo Bib Tiedosto
    [Arguments]    ${nimi}=testibib
    Kirjoita Komentoriville    bib
    Kirjoita Komentoriville    ${nimi}