# TrelloCardCreater
Python Script to create boards, lists, and cards to your personal Trello account (This is without using Trello SDK)

#requirements

Application was created on Python 3.9.1 64 bit Interpereter. The program should work with older versions but if not, please update to newest version

To connect to your trello account, you will need your Account Key and Token for varification. The UI will hide your input so that your information is not stolen.
Information on how to generate these credentials can be found here https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/. Keep a record of these
somewhere safe.

If you already have a personal board, card or list, you will need your 8 Character BoardID that can be grabbed from its url, your 8 Character CardID from its url,
or your List name spelled correctly.

#Usage

When you start the application, it will prompt you to paste your key, and then token. If they fail validation it will prompt you again. After that, follow the onscreen
instructons to create your new board, list, and card. If you already have a board or card that you want to post to, you will need the 8 Character boardID found in the url of your 
board. https://trello.com/b/[BoardID]/{name}, your List Name spelled correctly, and your CardID found in the url of your desired card. https://trello.com/c/[cardID]/{name}. The UI
will prompt you for this information. Once you send a comment, you can check your board on Trello to ensure it went through.

#Known Issues

Entering a non existent list name and then entering a correct one after will cause an error, for some reason the app isn't pulling the json information correctly on the second try

Next step is finding a way to grab user board and card by name instead of url

