*** Settings ***
Library    ../AppLibrary.py

*** Keywords ***
Tulosta Viitteet
    Input    tulosta

Kirjoita Komentoriville
    [Arguments]    ${text}
    Input    ${text}

Pois Komentoriviltä
    Input    ${EMPTY}

Tulostuksessa Pitäisi Olla
    [Arguments]    ${text}
    Output Should Contain    ${text}

Käynnistä Ohjelma
    Run Application

Tulostuksessa Ei Pitäisi Olla
    [Arguments]    ${text}
    Output Should Not Contain    ${text}

Lisätään Viitteen Tiedot
    [Arguments]    ${author}    ${title}    ${year}    ${publisher}    ${pages}=${EMPTY}    ${tags}=${EMPTY}
    Input    ${author}
    Input    ${title}
    Input    ${year}
    Input    ${publisher}
    Input    ${pages}
    Input    ${tags}
    Create Dict For Testing Citation    ${author}    ${title}    ${year}    ${publisher}    ${pages}    ${tags}

Tarkista Viitteet
    [Arguments]    ${citation_index}
    Check Citations    ${citation_index}
