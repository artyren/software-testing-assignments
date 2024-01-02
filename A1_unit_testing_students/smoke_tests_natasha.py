import pytest
from checkout_and_payment import *
from login import *
from logout import *
from unittest.mock import * 
from products import *
import shutil
import random
import os
from test_check_cart import MockUser, MockProduct, MockShoppingCart

### CSV FILE FIXTURES ###

def get_json(filename):
    with open(filename, "r") as users:
        return json.load(users)

def rollback_json():
    os.remove("users.json")
    os.system('cp users_backup.json users.json')


#tests for new implementation ##############################################################################
#log in by registering and dont add credit cards or anything to cart
def test_smoke_1(capsys):
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    user_exists = False
    for user in data:
        if user["username"] == new_username:
            user_exists = True
    assert user_exists == False
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'n', new_username, 'Hejsan123!', 'all', 'y', 'l' ]):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "You were successfully registered!" in captured.out
    assert "Successfully logged in" in captured.out
    assert "You have been logged out" in captured.out
    data = get_json("users.json")
    assert data[-1]["username"] == new_username
    assert data[-1]["address"] == 'uppsala 123'
    assert data[-1]["phone"] == '1122331122'
    assert data[-1]["email"] == new_username+'@mail.com'
    assert data[-1]["credit_cards"] == []
    rollback_json()


#register new user and add credit card, add apple to cart and check out (no money on card)
def test_smoke_2(capsys):
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    user_exists = False
    for user in data:
        if user["username"] == new_username:
            user_exists = True
    assert user_exists == False
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'y', '111111111111', '12/12', new_username, '123',  new_username, 'Hejsan123!', 'all', 'y', '1', 'c', 'y', 'l', 'y'  ]):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "You were successfully registered!" in captured.out
    assert "Successfully logged in" in captured.out
    assert "You don't have enough money to complete the purchase." in captured.out
    assert "You have been logged out" in captured.out
    data = get_json("users.json")
    assert data[-1]["username"] == new_username
    assert data[-1]["address"] == 'uppsala 123'
    assert data[-1]["phone"] == '1122331122'
    assert data[-1]["email"] == new_username+'@mail.com'
    assert data[-1]["credit_cards"] != []
    rollback_json()



#add new user with new fields, edit all fields of the card and chech its updated correctly, and add a new card
def test_smoke_3():
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'y', '555-555-555-555', '12/12', new_username, '123' ]):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]["credit_cards"][0]['cvv'] == '123'
    with patch('builtins.input', side_effect=[new_username, 'Hejsan123!', 'all', 'y', 'e', '4', '1', '4', '000', '4', '1', '3', 'new name', '4', '1', '2', '13/02', '4', '1', '1', '1234-1234-1234-1234' , '4', 'a', '1111-1111-1111-1111', '11/01', 'name', '111', 'c', '5', 'l'   ]):
        searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]["credit_cards"][0]['cvv'] == '000'
    assert data[-1]["credit_cards"][0]['name_on_card'] == 'new name'
    assert data[-1]["credit_cards"][0]['expiry_date'] == '13/02'
    assert data[-1]["credit_cards"][0]['card_number'] == '1234-1234-1234-1234'
    assert data[-1]["credit_cards"][1]['cvv'] == '111'
    assert data[-1]["credit_cards"][1]['name_on_card'] == 'name'
    assert data[-1]["credit_cards"][1]['expiry_date'] == '11/01'
    assert data[-1]["credit_cards"][1]['card_number'] == '1111-1111-1111-1111'
    rollback_json()


#reg new user , add credit card, change address, email and phone number and check that its correct and log out
def test_smoke_4():
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'n']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    data = get_json("users.json")
    with patch('builtins.input', side_effect=[new_username, 'Hejsan123!', 'all', 'y', 'e', '1', 'new address', '2', '018-000000', '3', 'mail@mail.se', '5', 'l'  ]):
        searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]['address'] == 'new address'
    assert data[-1]['phone'] == '018-000000'
    assert data[-1]['email'] == 'mail@mail.se'
    rollback_json()

#test editing an invalid choice
def test_smoke_5(capsys):
    data = get_json("users.json")
    with patch('builtins.input', side_effect=['Ramanathan', "Notaproblem23*", 'all', 'y', 'e', 'asdnkjsdc', '5', 'l'  ]):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Invalid choice." in captured.out
    rollback_json()


#reg new user and dont add card, edit info and add card and check it was added
def test_smoke_6():
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'n']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]["credit_cards"] == [] 
    with patch('builtins.input', side_effect=[new_username, 'Hejsan123!', 'all', 'y', 'e', '4', 'y', '1111-1111-1111-1111','11/01', 'name', '111', '5', 'l'  ]):
        searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]["credit_cards"][0]['cvv'] == '111'
    assert data[-1]["credit_cards"][0]['name_on_card'] == 'name'
    assert data[-1]["credit_cards"][0]['expiry_date'] == '11/01'
    assert data[-1]["credit_cards"][0]['card_number'] == '1111-1111-1111-1111'
    rollback_json()