#calling the necessary libraries; if you don't have them, install them first!
import json
import requests
import sys
#we define the base url to simplify the code and reduce potential errors.
api_base_url = "https://reqres.in"
#the base function of the code. We define it first to increase its reusability if more functions are to be added to this code.
def get_user_data():
    #grabs the id the user wishes to call
    userinputid = input("Hi what's the id you want:")
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
userChoice = input("Select a function:\n1. View user (Press 1)\n2. Add user (Press 2)")
if userChoice == "1":
    get_user_data()
elif userChoice == "2":
    add_user_data()
else:
    userBuffer = input("You just failed a simple options question")
    sys.exit()