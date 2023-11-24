import json

#Login as a user
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")
    #Look for user in database
    with open('users.json', "r+") as file:
        data = json.load(file)
        for entry in data:
            if entry["username"] == username and entry["password"] == password:
                print("Successfully logged in")
                return {"username": entry["username"], "wallet": entry["wallet"] }
            elif entry["username"] == username:
                print("Either username or password were incorrect")
                return None
        while True:
            answer = input("Username not found, would you like to register? (Y/N)")
            if answer == "Y" or answer == "y":
                new_pass = ""
                while not pass_check(new_pass):
                    new_pass = input("Password needs to: \nBe at least 8 characters\nHave a special character\nHave at least one upper case character\nEnter new password:")
                data.append({"username": username, "password": new_pass, "wallet": 0 })
                file.seek(0)
                json.dump(data, file, indent=10)
                file.truncate()
                return None
            elif answer == "N" or answer == "n":
                print("Have a nice day!")
                return None
            else:
                print("Answer in wrong format, try again")

#Checks if the password passes the requirements
def pass_check(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("Password sent is not a string")
    symbols = set(r"""`~!@#$%^&*()_-+={[}}|\:;"'<,>.?/""")
    case_OK = False
    symbol_OK = False
    if len(password) < 8:
        return False
    for char in password:
        if char in symbols:
            symbol_OK = True
        if char.isupper():
            case_OK = True
            
    return case_OK and symbol_OK