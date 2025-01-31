import json
from user import User
FILEPATH = "Software-3K04-/storage/user.json"


def WriteJSON(filepath: str,userlist: list)-> None:
    with open(filepath,"w") as f:
        json.dump(userlist,f,indent=1)
    #writes to the json file, dumps the list with an indent so it is easier to read

def WriteUsers(users: list[User])-> None:
    userdictlist = []
    for user in users:
        userdict = {}
        userdict["username"] = user.getUsername()
        userdict["password"] = user.getPassword()
        userdict["pacingmode"] = user.pacing
        userdict["parameters"] = user.getParameters()
        userdictlist.append(userdict)
    WriteJSON(FILEPATH,userdictlist)
    #writes the user values into a dictionary and then into a list, this list is then written into the json file using the previous function
    #used for a user registration, will be used in the future when users can change their parameter values in the DCM
    
def ReadJSON(filepath: str):
    with open(filepath,"r") as f:
        x = json.load(f)
    return x
    #returns the json file so that it can be read

def ReadUsers() -> list[User]:
    users = []
    readlist = ReadJSON(FILEPATH)
    for user in readlist:
        username = user["username"]
        password = user["password"]
        pacing = user["pacingmode"]
        parameters = user["parameters"]
        uservalue = User(username,password,pacing,parameters)
        users.append(uservalue)
    return users 
    #takes read json file and sets the user values equal to values in the file, this is used to get previous user's values when they login

