from pymongo import MongoClient
from datetime import datetime
import os
from cryptography.fernet import Fernet
from colorama import Fore, Back, Style
import time

CONNECTION_STRING = "" #Add MongoDB database link


def clr():
    os.system('cls')


def write_key():
    key = Fernet.generate_key() 
    with open("key.key", "wb") as key_file: 
        key_file.write(key) 


def load_key():
    return open("key.key", "rb").read() 


def insertAccount(key):
    f = Fernet(key)

    site = ""
    while site == "":
        site = str(input("SITE: "))

    clr()
    email = ""
    while email == "":
        email = str(input("EMAIL: "))

        if email:
            email = f.encrypt(email.encode())

    clr()
    username = str(input("USERNAME: "))
    if username:
        username = f.encrypt(username.encode())
    else:
        username = f.encrypt('NaN'.encode())
        
    clr()
    password = str(input("PASSWORD: "))
    if password:
        password = f.encrypt(password.encode())
    else:
        password = f.encrypt('NaN'.encode())
    

    clr()
    twofa = str(input("2FA: "))
    if twofa:
        twofa = f.encrypt(twofa.encode())
    else:
        twofa = f.encrypt('NaN'.encode())
    

    clr()
    twofa_app = str(input("2FA APP: "))
    if twofa_app:
        twofa_app = f.encrypt(twofa_app.encode())
    else:
        twofa_app = f.encrypt('NaN'.encode())

    clr()
    data_registo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    last_seen = data_registo
    last_update = data_registo
    
    try:
        with MongoClient(CONNECTION_STRING) as client:

            db = client.password_manager
            collection = db.accounts

            new_document = {
                "site": site,
                "email": email,
                "username": username,
                "password": password,
                "twofa":twofa,
                "twofa_app": twofa_app,
                "data_registo": data_registo,
                "last_seen": data_registo,
                "last_update": data_registo
            }    
            
            result = collection.insert_one(new_document)

            print(Fore.GREEN + "\nSUCCESS: Account registed: " + Style.RESET_ALL, result.inserted_id)
            time.sleep(1)
        

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)


def listAccounts():
    i = 1
    try:
        with MongoClient(CONNECTION_STRING) as client:
            db = client.password_manager
            collection = db.accounts

            projection = {
                "site": 1,
                "data_registo": 1,
                "last_seen": 1,
                "last_update": 1
            }

            result = collection.find({}, projection)

            print(Fore.RED + Back.WHITE + "{:<20} | {:<30} | {:<30} | {:<30}".format("SITE", "REGISTRATION DATE", "LAST TIME OPENED", "LAST UPDATE"))

            for document in result:
                print(Fore.GREEN + Back.BLACK + "{:<20} | {:<30} | {:<30} | {:<30}\n".format(document.get("site"), document.get("data_registo"), document.get("last_seen"), document.get("last_update")))

            print(Fore.RED + Back.WHITE + "{:<20} | {:<30} | {:<30} | {:<30} {}".format("SITE", "REGISTRATION DATE", "LAST TIME OPENED", "LAST UPDATE", ""+ Style.RESET_ALL))

            
    except Exception as e:
        i = 0
        print(f"Error: {e}")
        time.sleep(1)

    return i



def viewAccount(key):

    if listAccounts():

        print("\nWrite account website field.")
        while True:

            site = input("SITE: ")
                
            check = str(input("Are you sure you want to see this account? (y/n) "))

            if check == "y" or check == "Y":
                f = Fernet(key)
                try:
                    with MongoClient(CONNECTION_STRING) as client:
                        db = client.password_manager
                        collection = db.accounts

                        result = collection.find_one({"site": site})

                        if result:
                            print(Fore.RED + Back.WHITE + "{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30}".format("SITE", "EMAIL", "USERNAME", "PASSWORD", "2FA", "2FA APP", "REGISTARTION DATE", "LAST TIME OPENED", "LAST UPDATE"))

                            id = result.get("_id")
                            email = result.get("email")
                            username = result.get("username")
                            password = result.get("password")
                            twofa = result.get("twofa")
                            twofa_app = result.get("twofa_app")

                            print(Fore.GREEN + Back.BLACK + "{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format(result.get("site"), f.decrypt(email).decode(), f.decrypt(username).decode(), f.decrypt(password).decode(), f.decrypt(twofa).decode(), f.decrypt(twofa_app).decode(), result.get("data_registo"), result.get("last_seen"), result.get("last_update")))

                            print(Fore.RED + Back.WHITE + "{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} {}".format("SITE", "EMAIL", "USERNAME", "PASSWORD", "2FA", "2FA APP", "REGISTARTION DATE", "LAST TIME OPENED", "LAST UPDATE",  ""+ Style.RESET_ALL))
                            
                            
                            mommentDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            
                            filter = { "_id": id }
                            update = { "$set": { 'last_seen': mommentDate } }
                            
                            collection.update_one(filter, update)
                            
                        else:
                            print(Fore.RED + "\nERROR: No account found that corresponds:" + Style.RESET_ALL, site)

                        
                except Exception as e:
                    print(f"ERROR: {e}")

                break
            else:
                break
    
    else:
        print(Fore.RED + "ERROR: Registers list is empty." + Style.RESET_ALL)         
          

    
def deleteAccount():

    if listAccounts():

        print("Write account website field.\n")
        while True:

            site = input("SITE: ")
                
            check = str(input("Are you sure you want to delete this account? (y/n) "))

            if check == "y" or check == "Y":
                try:
                    with MongoClient(CONNECTION_STRING) as client:
                        db = client.password_manager
                        collection = db.accounts

                        result = collection.find_one({"site": site})

                        if result:
                            collection.delete_one({"_id":result.get("_id")})
                            print(Fore.GREEN + "\nSUCCESS: Account deleted: " + Style.RESET_ALL, site)
                            time.sleep(1)
                            
                        else:
                            print(Fore.RED + "\nERROR: No account found that corresponds:" + Style.RESET_ALL, site)
                            time.sleep(1)
                        
                except Exception as e:
                    print(f"ERROR: {e}")
                    time.sleep(1)
                break
            else:
                break
    
    else:
        print(Fore.RED + "ERROR: Registers list is empty." + Style.RESET_ALL)    
    
    
        
def updateAccount(key):
    
    if listAccounts():
        print("Write account website field.\n")
        while True:

            site = input("SITE: ")
            
            check = str(input("Are you sure you want to update this account? (y/n) "))

            if check == "y" or check == "Y":

                try:
                    with MongoClient(CONNECTION_STRING) as client:
                        db = client.password_manager
                        collection = db.accounts

                        result = collection.find_one({"site": site})

                        if result:
                            f = Fernet(key)
                            
                            id = result.get("_id")
                            email = result.get("email")
                            username = result.get("username")
                            password = result.get("password")
                            twofa = result.get("twofa")
                            twofa_app = result.get("twofa_app")
                            
                            clr()
                            print("\nActual site name: {}\n".format(result.get("site")))
                            up_site = str(input("Update site name? (y/n) "))
                            if up_site == "y" or up_site == "Y":
                                site = str(input("New Site name: "))
                            
                            
                            clr()
                            print("\nActual email: {}\n".format(f.decrypt(email).decode()))
                            up_email = str(input("Update email? (y/n) "))
                            if up_email == "y" or up_email == "Y":
                                email = str(input("New email: "))
                                email = f.encrypt(email.encode())
                             
                                
                            clr()
                            print("\nActual username: {}\n".format(f.decrypt(username).decode()))
                            up_username = str(input("Update username? (y/n) "))
                            if up_username == "y" or up_username == "Y":
                                username = str(input("New username: "))
                                username = f.encrypt(username.encode()) 
                                
                                
                            clr()
                            print("\nActual password: {}\n".format(f.decrypt(password).decode()))
                            up_password = str(input("Update password? (y/n) "))
                            if up_password == "y" or up_password == "Y":
                                i = 0
                                while i == 0:
                                    password = str(input("New Password: "))
                                    confirm_password = str(input("Confirm Password: "))

                                    if password == confirm_password:
                                        password = f.encrypt(password.encode())
                                        i = 1
                                    else:
                                        print(Fore.RED + "\nERROR: Password not confirmed" + Style.RESET_ALL)
                                        
                                        
                            clr()
                            print("\nActual Two Factor Authenticator: {}\n".format(f.decrypt(twofa).decode()))
                            up_twofa = str(input("Update Two Factor Authenticator? (y/n) "))
                            if up_twofa == "y" or up_twofa == "Y":
                                twofa = str(input("New Two Factor Authenticator: "))
                                twofa = f.encrypt(twofa.encode())            
                            
                            
                            clr()
                            print("\nActual Two Factor Authenticator App: {}\n".format(f.decrypt(twofa_app).decode()))
                            up_twofa_app = str(input("Update Two Factor Authenticator App? (y/n) "))
                            if up_twofa_app == "y" or up_twofa_app == "Y":
                                twofa_app = str(input("New Two Factor Authenticator App: "))
                                twofa_app = f.encrypt(twofa_app.encode())
                                
                                
                            last_update = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            
                            filter = { "_id": id } 
                                                       
                            update = {
                                "$set": {
                                    'site': site,
                                    'email': email,
                                    'username': username,
                                    'password': password,
                                    'twofa': twofa,
                                    'twofa_app': twofa_app,
                                    'last_update': last_update
                                }
                            }
                            
                            result_update = collection.update_one(filter, update)

                            if result_update.modified_count > 0:
                                print(Fore.GREEN + "\nSUCCESS: Account updated: " + Style.RESET_ALL, site)
                                time.sleep(1)
                            else:
                                 print(Fore.RED + "ERROR: No account was updated" + Style.RESET_ALL)
                                 time.sleep(1)
                                
                            
                            
                        else:
                            print(Fore.RED + "\nERROR: No account found that corresponds:" + Style.RESET_ALL, site)
                            time.sleep(1)

                        
                except Exception as e:
                    print(f"ERROR: {e}")
                    time.sleep(1)
            break
    else:
        print(Fore.RED + "ERROR: Registers list is empty." + Style.RESET_ALL)
        time.sleep(1)           
                