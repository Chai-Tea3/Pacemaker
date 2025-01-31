import user_storage
import hashlib 
from user import User
from parameters import Parameter
from pacingmode import Pacing
HOME = "HOME"
LOGIN = "LOGIN"
REGISTER = "REGISTER"
MAXUSERS = 10

#fetches the current users and places them into a list
_user: list[User] = user_storage.ReadUsers()

#checking whether a new user can be registered
def RegisterCheck(username,password):
    if(username == "" or password == ""):
        message = "invalid username"
    else:
        hashpassword = hashlib.sha256(password.encode())
        print(hashpassword.hexdigest())
        newuser = User(username,hashpassword.hexdigest(),Pacing.InitialUserValues(),Parameter.UserValues())
        if(MaxUserCheck()): #checks if user count is <10
            if(CheckUser(newuser)):
                message = "Username already registered"
            else:
                _user.append(newuser)
                user_storage.WriteUsers(_user)
                message = "Registration successful"
        else:
            message = "maximum amount of users registered" 
    return message

#checking for amount of users 
def MaxUserCheck():
    if (len(_user) < MAXUSERS):
        return True
    else:
        return False

#checks if username and password match a user already created
def LoginCheck(username,password):
    hashpassword = hashlib.sha256(password.encode())
    print(hashpassword.hexdigest())
    newuser = User(username,hashpassword.hexdigest(),Pacing.InitialUserValues(),Parameter.UserValues())
    if(CheckUser(newuser)):
        index = userIndex(newuser.getUsername())
        if(CheckPassword(newuser,index)):
            message = "Login successful"
        else:
            message = "incorrect username or password"
    else:
         message = "incorrect username or password" #messages to be displayed in interface
    return message

    
    
    
#checking if the user exists in the list
def CheckUser(newuser: User):
    founduser = 0
    for user in _user:
        if(newuser.getUsername() == user.getUsername()):
            founduser = 1
            return True
    if(founduser == 0):
        return False
    
#finds the index of the user in the list
def userIndex(username:str):
     for user in _user:
        if(username == user.getUsername()):
            userindex = _user.index(user)
            return userindex

#checks if the password is the same at the given index
def CheckPassword(newuser: User,index):
    user: User = _user[index]
    if(newuser.getPassword() == user.getPassword()):
        return True
    else:
        return False

#updates the paramater values when changed with sliders in interface, write to json file 
def updateParameter(username: str, key,value):
    index = userIndex(username)  
    user: User = _user[index]  
    user.setParameter(value, key)
    _user[index] = user
    user_storage.WriteUsers(_user)  

#returns the specifc value of the parameter at index key
def getParameter(username:str,key):
    _user: list = user_storage.ReadUsers()
    index = userIndex(username)  
    user: User = _user[index]
    return float(user.getParameter(key))

def getParameters(username:str):
    _user: list = user_storage.ReadUsers()
    index = userIndex(username)  
    user: User = _user[index]
    parameter_key = [str(key) for key in user.getParameters()]
    print(parameter_key)
    parameter_dict = user.getParameters()
    send_list = []
    for x in parameter_key:
        if(x == "AS"):
            send_list.append(int(parameter_dict[x]*10))
        elif(x == "AA"):
            send_list.append(int(parameter_dict[x]*10))
        elif(x == "VS"):
            send_list.append(int(parameter_dict[x]*10))
        elif(x == "VA"):
            send_list.append(int(parameter_dict[x]*10))
        else:
            send_list.append(int(parameter_dict[x]))
    print(send_list)
    return list(send_list)    

def updatePacing(username: str, value:str):
    index = userIndex(username)  
    user: User = _user[index]  
    _user[index] = user
    user.setPacing(value)            

def getPacing(username:str):
    _user: list = user_storage.ReadUsers()
    index = userIndex(username)  
    user: User = _user[index]
    return int(user.getPacing())    

    
    





    