*** Settings ***
Library           ../appLibrary.py

*** Keywords ***
Input Mennään Lisäämään
    Input  lisää


Viitteen Tiedot
    [Arguments]    ${author}    ${title}    ${year}    ${journal}