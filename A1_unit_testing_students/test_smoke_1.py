from products import *
from checkout_and_payment import load_products_from_csv
import json
import shutil
from unittest.mock import patch

def reset_json():
    shutil.copyfile("users_backup.json", "users.json")

def reset_csv():
    shutil.copyfile("products_backup.csv", "products.csv")

def get_json(filename):
    with open(filename, "r") as users:
        return json.load(users)

def test_path_wrong_login_add(capsys):
    choices = []
    choices.append("Tester")
    choices.append("123456")
    choices.append("Y")
    choices.append("Testing123#")
    choices.append("Tester")
    choices.append("Testing123#")
    choices.append("all")
    choices.append("Y")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    user_json = get_json("users.json")
    assert {'password': "Testing123#", 'username': "Tester", 'wallet': 0} in user_json
    assert "You have been logged out" in captured.out
    reset_json()
    

#SHOULD FAIL. Program does not accurately update wallet.
def test_add_item_and_checkout(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("Y")
    choices.append("3")
    choices.append("c")
    choices.append("Y")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    user_json = get_json("users.json")
    reset_json()
    products = load_products_from_csv("products.csv")
    reset_csv()
    assert {'password': "Oliver*123", 'username': "Oliver", 'wallet': 58.5} in user_json
    assert "Orange added to your cart" in captured.out
    assert products[2].name == "Orange"
    assert products[2].units == 7

def test_add_item_then_remove(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("Y")
    choices.append("3")
    choices.append("r")
    choices.append("1")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    user_json = get_json("users.json")
    reset_json()
    products = load_products_from_csv("products.csv")
    reset_csv()
    assert {'password': "Oliver*123", 'username': "Oliver", 'wallet': 60} in user_json
    assert "Orange added to your cart" in captured.out
    assert "Orange has been removed." in captured.out
    assert products[2].name == "Orange"
    assert products[2].units == 8

def test_remove_item_wrong_input(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("Y")
    choices.append("3")
    choices.append("r")
    choices.append("2")
    choices.append("r")
    choices.append("asd")
    choices.append("r")
    choices.append("1")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    user_json = get_json("users.json")
    reset_json()
    products = load_products_from_csv("products.csv")
    reset_csv()
    assert {'password': "Oliver*123", 'username': "Oliver", 'wallet': 60} in user_json
    assert "Orange added to your cart" in captured.out
    assert "Choice out of range." in captured.out
    assert "Choice is not a numeric one" in captured.out
    assert "Orange has been removed." in captured.out
    assert products[2].name == "Orange"
    assert products[2].units == 8

def test_login_logout(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("123124")
    choices.append("Tester")
    choices.append("1231415")
    choices.append("123123")
    choices.append("n")
    choices.append("Tester")
    choices.append("1231415")
    choices.append("y")
    choices.append("Testing123#")
    choices.append("Tester")
    choices.append("Testing123#")
    choices.append("all")
    choices.append("y")
    choices.append("3")
    choices.append("l")
    choices.append("y")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    user_json = get_json("users.json")
    reset_json()
    assert {'password': "Testing123#", 'username': "Tester", 'wallet': 0} in user_json
    assert "Either username or password were incorrect" in captured.out
    assert "Have a nice day!" in captured.out
    assert "Answer in wrong format, try again" in captured.out
    assert "Your cart is not empty.You have following items" in captured.out

#SHOULD FAIL. Still removes money for the two wares even though only one in stock
def test_out_of_stock(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("y")
    choices.append("6")
    choices.append("6")
    choices.append("c")
    choices.append("y")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    user_json = get_json("users.json")
    reset_json()
    products = load_products_from_csv("products.csv")
    reset_csv()
    assert {'password': "Oliver*123", 'username': "Oliver", 'wallet': 50} in user_json
    assert "Watermelon added to your cart." in captured.out
    assert "Sorry, Watermelon is out of stock." in captured.out
    assert products[5].name != "Watermelon" 

def test_invalid_input_store(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("y")
    choices.append("1231414")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    reset_json()
    assert "Invalid input. Please try again." in captured.out

def test_checkout_and_logout(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("y")
    choices.append("3")
    choices.append("c")
    choices.append("n")
    choices.append("l")
    choices.append("y")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    reset_csv()
    reset_json()
    assert "Your cart is not empty.You have following items" in captured.out

def test_too_little_money(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("y")
    choices.append("60")
    choices.append("c")
    choices.append("y")
    choices.append("l")
    choices.append("y")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    reset_csv()
    reset_json()
    assert "You don't have enough money to complete the purchase" in captured.out
    assert "Please try again!" in captured.out

#Fails as wallet not updated correctly

def test_too_little_money_remove(capsys):
    choices = []
    choices.append("Oliver")
    choices.append("Oliver*123")
    choices.append("all")
    choices.append("y")
    choices.append("60")
    choices.append("3")
    choices.append("c")
    choices.append("y")
    choices.append("r")
    choices.append("1")
    choices.append("c")
    choices.append("y")
    choices.append("l")

    with patch('builtins.input', side_effect=choices):
        searchAndBuyProduct()

    captured = capsys.readouterr()
    products = load_products_from_csv("products.csv")
    reset_csv()
    users = get_json("users.json")
    reset_json()
    assert "You don't have enough money to complete the purchase" in captured.out
    assert "Please try again!" in captured.out
    assert {'password': "Oliver*123", 'username': "Oliver", 'wallet': 58.5} in users
    assert products[59].name == "Vacuum Cleaner"
    assert products[2].units == 7