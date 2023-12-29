import csv
import json

def add_credit_card():
    card_number = input('Enter the card number: ')
    exp_date = input('Enter the expiry date: ')
    name_card = input('Enter the name on the card: ')
    cvv = input('Enter the CVV: ')
    credit_card = {
                "card_number": card_number,
                "expiry_date": exp_date,
                "name_on_card": name_card,
                "cvv": cvv
            }
    return credit_card
        

def edit_user_info(user):
    with open('users.json', 'r') as json_file:
        user_file = json.load(json_file)
    for user_info in user_file:
            if user_info["username"] == user.name:
                while True:
                    prt_str = '1. Address\n2. Phone number\n3. Email\n4. Credit card\n5. Save and exit'
                    choice = input("\nSelect one of the following:\n" + prt_str)
                    if choice == '1':
                        address = input("Enter the new address: ")
                        user_info["address"] = address  
                    elif choice == '2':
                        phone = input("Enter the new phone number: ")
                        user_info["phone"] = phone 
                    elif choice == '3':
                        email = input("Enter the new email: ")
                        user_info["email"] = email 
                    elif choice == '4':
                        if len(user_info["credit_cards"]) == 0:
                            add_card = input('You have no credit cards registered. Would you like to add one? y/n')
                            if add_card.lower() == 'y':
                                credit_card = add_credit_card()
                                user_info["credit_cards"] = [credit_card]
                            elif add_card.lower() == 'n':
                                break
                        else:
                            while True:
                                num_of_cards = 0
                                for i, card in enumerate(user_info["credit_cards"]):
                                    num_of_cards +=1
                                    print('')
                                    print(f"Card {i + 1}:")
                                    print(f"Card number: {card['card_number']}")
                                    print(f"Expiry date: {card['expiry_date']}")
                                    print(f"Name on card: {card['name_on_card']}")
                                    print(f"CVV: {card['cvv']}")
                                    print('')
                                card = input("Enter the number of the credit card you want to edit, a to add a new card, or c to cancel: ")
                                if card.isdigit() and int(card) <= num_of_cards:
                                    prt_str_card = '1. Card number\n2. Expiry date\n3. Name on card\n4. CVV\n'
                                    card_edit = input("What would you like to edit?\n" + prt_str_card)
                                    if card_edit == '1':
                                        card_number = input("Enter your new card number: ")
                                        user_info["credit_cards"][int(card)-1]["card_number"] = card_number
                                        break
                                    elif card_edit == '2':
                                        expiry_date = input("Enter your new expiry date: ")
                                        user_info["credit_cards"][int(card)-1]["expiry_date"] = expiry_date
                                        break
                                    elif card_edit == '3':
                                        name_on_card = input("Enter the new name on the card: ")
                                        user_info["credit_cards"][int(card)-1]["name_on_card"] = name_on_card
                                        break
                                    elif card_edit == '4':
                                        cvv = input("Enter the new CVV: ")
                                        user_info["credit_cards"][int(card)-1]["cvv"] = cvv
                                        break
                                    else:
                                        print("Invalid choice.")
                                elif card == 'c':
                                    break
                                elif card == 'a':
                                    credit_card = add_credit_card()
                                    user_info["credit_cards"].append(credit_card)
                                else:
                                    print("Invalid choice.")
                    elif choice == '5':
                        break
                    else:
                        print("Invalid choice. ")
                with open('users.json', "w") as write_file:
                    json.dump(user_file, write_file,indent=2)


