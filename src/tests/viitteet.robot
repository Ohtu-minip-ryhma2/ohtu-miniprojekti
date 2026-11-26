*** Settings ***
resource    resource.robot

*** Test Cases ***
Testataan että voidaan mennä lisäämään viite
    Lisätään Viitteen Tiedot    J.K. Rowling    Harry Potter ja viisasten kivi    1997    Otava
    Pois
    Run Application
    Output Should Contain    Lisätään uusi viite
    Output Should Contain    Vapaaehtoiset kentät voi ohittaa painamalla Enteriä.
    Output Should Contain    Viitteen tiedot hyväksytty.

Testataan että lisätty viite tulostuu oikein
    Lisätään Viitteen Tiedot    J.K. Rowling    Harry Potter ja viisasten kivi    1997    Otava
    Input  tulosta
    Pois
    Run Application
    Tarkista Viitteet Ilman Sivuja tai Tageja   J.K. Rowling    Harry Potter ja viisasten kivi    1997    Otava

Testataan että saadaan bib tiedosto
    Lisätään Viitteen Tiedot    J.K. Rowling    Harry Potter ja viisasten kivi    1997    Otava
    Input  bib
    Input  testibib
    Pois
    Run Application
    check_bib_file    J.K. Rowling    Harry Potter ja viisasten kivi    1997    Otava