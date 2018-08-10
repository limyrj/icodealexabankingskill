#calling the necessary libraries; if you don't have them, install them first!
import json
import requests
import sys
#we define the base url to simplify the code and reduce potential errors.
api_base_url = "https://reqres.in"
#the base function of the code. We define it first to increase its reusability if more functions are to be added to this code.
def register_user():
    userEmail = input("What is your email?:")
    userPassword = input("What is your password?")
    userPasswordConfirm = input("Please reenter your password.")
    #checks if the reentered password matches the original.
    if userPassword == userPasswordConfirm:
        #makes the login info into a dictionary
        loginParams = {"email": userEmail, "password": userPassword}
        #sends the request to the api!
        responseLogin = requests.post("%s/api/register" %(api_base_url), data = loginParams)
        if responseLogin.status_code == 201:
            logintoken = responseLogin.json()
            print("Registration successful, token: %s" %(logintoken["token"]))
            userChoice = input("Proceed with login? [y/n]")
            if userChoice == "y":
                login_user()
            if userChoice == "n":
                sys.exit()
            else:
                #the program is disappointed
                userBuffer = input("You just failed a simple options question")
                sys.exit()
        elif responseLogin.status_code == 400:
            #you didn't enter one of the values!
            loginError = responseLogin.json()
            for data in loginError:
                print(data + " : " + loginError[data])
            register_user()
        else:
            #a random error popped up!
            loginError = responseLogin.json()
            for data in loginError:
                print("An unexpected error occurred: " + data + " : " +loginError[data] + "with error code: " +str(responseLogin.status_code))
            register_user()
    else:
        userBuffer = input("Sorry, the passwords did not match.")
        register_user()
    userBuffer = input("Thanks and goodbye!")
    sys.exit()
def login_user():
    userEmail = input("What is your email?:")
    userPassword = input("What is your password?")
    userPasswordConfirm = input("Please reenter your password.")
    if userPassword == userPasswordConfirm:
        loginParams = {"email": userEmail, "password": userPassword}
        responseLogin = requests.post("%s/api/login" %(api_base_url), data = loginParams)
        if responseLogin.status_code == 200:
            logintoken = responseLogin.json()
            print("Login successful, token: %s" %(logintoken["token"]))
        elif responseLogin.status_code == 400:
            loginError = responseLogin.json()
            for data in loginError:
                print(data + " : " + loginError[data])
            login_user()
        else:
            loginError = responseLogin.json()
            for data in loginError:
                print("An unexpected error occurred: " + data + " : " +loginError[data] + "with error code: " +str(responseLogin.status_code))
            login_user()
    else:
        userBuffer = input("Sorry, the passwords did not match.")
        login_user()
    userBuffer = input("Thanks and goodbye!")
    sys.exit()
def get_user_data(userinputid):
    #calls the api for the user info with the id the user has entered.
    responseReply = requests.get("%s/api/users/%s" %(api_base_url, userinputid))
    #an if loop to see if the user exists; 404 status code = user doesn't exist. 
    if responseReply.status_code == 404:
        print("That user does not exist.")
        userinputid = input("Search again?: (type no to quit)")
        if userinputid == "no":
            sys.exit()
        else:
            get_user_data(userinputid)  
    #formats the JSON reply the api has sent into a dictionary, which the below code parses into a string output with multiple for loops. 
    elif responseReply.status_code == 200:    
        interpretedReply = responseReply.json()
        for data in interpretedReply:
            for objects in interpretedReply[data]:
                print(str(objects)+" : "+ str(interpretedReply[data][objects]))
        userinputid = input("Search again?: (type no to quit)")
        #gives the user the option to quit from the program. Otherwise, the program will continue.
        if userinputid == "no":
            sys.exit()
        get_user_data(userinputid)
    else:
        print("An unexpected error occurred; error code %s" %(str(responseReply.status_code)))
def add_user_data():
    username = input("What is the name of the new user?")
    userJob = input("What is the job of the new user?")
    paramAddUser = {"name": username, "job": userJob}
    responseReply = requests.post("%s/api/users" %(api_base_url), params = paramAddUser)
    if responseReply.status_code == 201:
        print("User successfully added!:")
        userSuccessfullyAdded = responseReply.json()
        for data in userSuccessfullyAdded:
            print(data + " : " + userSuccessfullyAdded[data])
    else:
        print("An unexpected error occured; error code %s" %(str(responseReply.status_code)))
print("Make sure you have the json and requests library to run this code")
userChoice = input("Select a function:\n1. View user (Press 1)\n2. Add user (Press 2)\n3. Register (Press 3)\n4. Login (Press 4)")
if userChoice == "1":
    #grabs the id the user wishes to call
    userinputid = input("Hi what's the id you want:")
    get_user_data(userinputid)
elif userChoice == "2":
    add_user_data()
elif userChoice == "3":
    register_user()
elif userChoice == "4":
    login_user()
else:
    userBuffer = input("You just failed a simple options question")
    sys.exit()