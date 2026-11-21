*** Settings ***
Library           ../AppLibrary.py

*** Keywords ***
Tulosta Viitteet
    Input  tulosta

Pois
    Input  ${EMPTY}

Lisätään Viitteen Tiedot
    [Arguments]    ${author}    ${title}    ${year}    ${publisher}
    Input  lisää
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}

Tarkista Viitteet
    [Arguments]    ${author}    ${title}    ${year}    ${publisher}
    Output Should Contain   Kirjoittajat: ${author}
    Output Should Contain   Otsikko: ${title}
    Output Should Contain   Vuosi: ${year}
    Output Should Contain   Julkaisu: ${publisher} 