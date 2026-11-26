*** Settings ***
Library           ../AppLibrary.py

*** Keywords ***
Tulosta Viitteet
    Input  tulosta

Pois
    Input  ${EMPTY}

Lisätään Viitteen Tiedot
    [Arguments]    ${author}    ${title}    ${year}    ${publisher}  ${pages}=${EMPTY}  ${tags}=${EMPTY}
    Input  lisää
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Input  ${pages}
    input  ${tags}

Tarkista Viitteet Ilman Sivuja tai Tageja
    [Arguments]    ${author}    ${title}    ${year}    ${publisher}  ${pages}=${EMPTY}  ${tags}=${EMPTY}
    Output Should Contain   [1] ${author}. ${title} ${publisher}, ${year}.
