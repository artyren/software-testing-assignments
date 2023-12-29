import json
from user import add_credit_card
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
                
                
                address = input('Enter your address: ')
                phone = input('Enter your phone number: ')
                email = input('Enter your email: ')
                while True:
                    add_card = input('Do you want to add a credit card? y/n')
                    if add_card.lower() == 'y':
                        credit_card = add_credit_card()
                        break
                    elif add_card.lower() == 'n':
                        break
                    else:
                        ('Invalid choice.')
                data.append({"username": username, 
                             "password": new_pass, 
                             "wallet": 0,
                             "address": address,
                             "phone": phone,
                             "email": email,
                             "credit_cards": [credit_card] if add_card.lower() == 'y' else []})
                

                file.seek(0)
                json.dump(data, file, indent=2)
                file.truncate()
                print('You were successfully registered!\n')
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