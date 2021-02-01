#Program requires these three packages to function
import getpass
import requests
import json


def start():
    user_key = ""
    user_token = ""
    url = "https://api.trello.com/1/search"

    hello = """
    ****************************************
    *                                      *
    *           Trello Post API            *
    *                                      *
    ****************************************\n"""
    print(hello)

    #Loops for user Key and Token generated from Trello. If the Key and Token are invalid or can resolve,
    #prompt user to enter their credentials again. 
    while True:
        #!!!Input is hidden from screen for user security
        user_key = getpass.getpass(prompt="Please paste your Trello Key and press enter (Display hidden for security): ")
        user_token = getpass.getpass(prompt="Please paste your Trello Token and press enter (Display hidden for security): ")

        headers = {"Accept": "application/json"}
        query = {'key': user_key,'token': user_token,'query': '{query}'}
        respones = requests.request("GET",url,headers=headers,params=query)

        #Loops until we get a valid connection. Response returns 404 or 400 usually if we can't
        #connect, but we really only care about 200. Uses Key/Token to send a search query
        if respones.status_code == 200:
            print("""\n
            *****************************************************
            *               Key and Token Validated             *
            *****************************************************\n""")
            break
        else:
            print("""\n
            *****************************************************
            * Key and Token cannot resolve, please try again... *
            *****************************************************\n""")

    return user_key, user_token


def user_board(key, token):
    answer = None
    post_url = "https://api.trello.com/1/boards/"
    #Driver for UI, checks to see if boardID provided by user is valid, or if no board,
    # allows user to create one 
    while answer not in ("Y","N"):
        answer = input("Do you already have a board? (Y or N): ") 
        if answer == "Y":
            while True:
                board_id = input("Please enter your Board's 8 Character ID Number [https://trello.com/b/[8 Char ID]/name]: ")
                url_resolve = "https://api.trello.com/1/boards/"+ board_id + "/lists"
                query = {"key": key, "token": token}
                response = requests.request("GET",url_resolve,params=query)
                if response.status_code == 200:
                    print("""\n
                    *****************************************************
                    *               Url Successfully Resolved           *
                    *****************************************************\n""")
                    break         
                else:
                    print("""\n
                    *****************************************************
                    *               Cannot find board                   *
                    *****************************************************\n""")          
        elif answer == "N":
            board_name = input("Creating Board, please enter board name: ")
            query = {"name": board_name, "key": key, "token": token}
            response = requests.request("POST", post_url, params=query)
            board_id = response.json()["shortUrl"].split("/")[-1].strip()

    return board_id


def user_list(key, token, board_id):
    answer = None
    found = None
    url = "https://api.trello.com/1/boards/"+ board_id + "/lists"
    #Same driver functionality as previous, allows user to find list or create a new list
    while answer not in ("Y","N"):
        answer = input("Do you already have a List? (Y or N): ") 
        if answer == "Y":
            while True:
                #For some reason, ListIDs are handled differently and are not exposed in the url.
                #Need to generate Json based off of your list name and search through it for ID
                list_name = input("Please enter your list name exactly how it appears: ")
                query = {"key": key, "token": token}
                response = requests.request("GET",url,params=query)
                list_json = response.json()
                for key in list_json:
                    if key["name"] == list_name:
                        list_id = key["id"]
                        print("""\n
                        *****************************************************
                        *                    List Found                     *
                        *****************************************************\n""") 
                        found = True
                        break
                if found == True:
                    break
                else:
                    list_json = None
                    key = None
                    print("""\n
                    *****************************************************
                    *               Cannot find list                    *
                    *****************************************************\n""")
        elif answer == "N":
            list_name = input("Creating List, Please enter the name of your List: ")
            url = f"https://api.trello.com/1/boards/" + board_id + "/lists"
            querystring = {"name": list_name, "key": key, "token": token}
            response = requests.request("POST", url, params=querystring)
            list_id = response.json()["id"]

    return list_id   


def user_card(key,token,list_id):
    answer = None
    #Once we get here we use all prior generated info to create a card and post to it, or 
    #post to an already existing card
    while answer not in ("Y", "N"):
        answer = input("Do you already have a Card? (Y or N): ") 
        if answer == "Y":
            card_id = input("Please enter your 8 Char CardID https://trello.com/c/[8 Char ID]/name: ")
            url = "https://api.trello.com/1/cards/"+ card_id + "/actions/comments?"
            text = input("Please enter your comment: ")
            q = {"key": key, "token": token, "text":text}
            requests.request("POST", url, params=q)
            print("""\n
            *****************************************************
            *               Comment Submitted!                  *
            *****************************************************\n""")
        elif answer == "N":
            card_name = input("Please name your card: ")
            url = f"https://api.trello.com/1/cards"
            querystring = {"name": card_name, "idList": list_id, "key": key, "token": token}
            response = requests.request("POST", url, params=querystring)
            card_id = response.json()["id"]
            url = "https://api.trello.com/1/cards/"+ card_id + "/actions/comments?"

            text = input("Please enter your comment: ")
            q = {"key": key, "token": token, "text":text}
            requests.request("POST", url, params=q)
            print("""\n
            *****************************************************
            *               Comment Submitted!                  *
            *****************************************************\n""")


#main driver
def main():
    user_key, user_token = start()
    board = user_board(user_key, user_token)
    list_ = user_list(user_key,user_token,board)
    user_card(user_key,user_token,list_)

if __name__ == "__main__":
    main()