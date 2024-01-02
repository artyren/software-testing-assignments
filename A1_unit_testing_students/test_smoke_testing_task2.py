import pytest
from checkout_and_payment_card_impl import *
from login import *
from logout import *
from unittest.mock import patch
from products import *
import shutil
import random
import os

### CSV FILE FIXTURES ###

@pytest.fixture
def copy_csv_file():
  # Set up: Copy the CSV file
  shutil.copy('products.csv','copy_products.csv')
  yield
  #Remove the copied CSV file
  os.remove('copy_products.csv')
  if os.path.isfile('tmp_copy_products.csv'):
      os.remove('tmp_copy_products.csv')
  
@pytest.fixture
def invalid_products_csv_key(tmp_path):
  csv_path = tmp_path / "invalid_products_key.csv"
  with open(csv_path, 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile)
      csv_writer.writerow(["InvalidHeader1", "InvalidHeader2", "InvalidHeader3"])
      csv_writer.writerow(["Product1", "10.99", "5"])
  return csv_path
### LOGIN FUNCTION FIXTURES ### 
def reset_json():
    with open('users.json', "r+") as test_file:
        json_test = json.load(test_file)
        with open('users_original.json', "r") as orig_file:
            json_orig = json.load(orig_file)
            json_test = json_orig
        test_file.seek(0)
        json.dump(json_test, test_file, indent=10)
        test_file.truncate()

def get_json(filename):
    with open(filename, "r") as users:
        return json.load(users)
  
# Mock classes for testing
class MockUser:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = float(wallet)
        self.cards = []
    
    # method to add a card to the user's list of cards 
    def add_card(self, card_name, card_balance):
        card = {"name": card_name, "balance": float(card_balance)}
        self.cards.append(card)
        
    # Method to retrieve the list of user's cards
    def get_cards(self):
        return self.cards

class MockProduct:
    def __init__(self, name, price, units):
        self.name = name
        self.price = float(price)
        self.units = int(units)
      #A method to get product details as a list
    def get_product(self):
        return [self.name, self.price, self.units]

class MockShoppingCart:
    def __init__(self):
        self.items = []
    # Method to add a product to the cart
    def add_item(self, product):
        self.items.append(product)
        
    # Method to remove a product from the cart
    def remove_item(self, product):
        self.items.remove(product)

    # Method to retrieve the items in the cart
    def retrieve_item(self):
        return self.items

    # Method to clear all items from the cart
    def clear_items(self):
        self.items = []

    # Method to calculate the total price of items in the cart
    def get_total_price(self):
        return sum(item.price for item in self.items)
    
    
def rollback_json():
    os.remove("users.json")
    os.system('cp users_backup.json users.json')


# TEST 1: LOGIN INVALID THEN LOGIN VALID USER END PROGRAM #
def test_login_invalid(capsys):
    json_file = get_json("users.json")
    route_strings = ["Sofia", "hey", "OASd", "N","Samantha","SecurePass123/^","all","y","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Answer in wrong format, try again\nHave a nice day!\n" in captured.out
    assert json_file == get_json("users_original.json")
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 2: LOGIN VALID SEARCH FOR SPECIFIC PRODUCT#
def test_login_valid_directly_search_product_logout(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","blender","y","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "['Product', 'Price', 'Units']\n['Blender', '30', '1']" in captured.out
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 3: LOGIN VALID CHECK CART W/ NOTHING IN IT 
def test_login_valid_no_shop_check_cart_logout(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","all","n","all","y","c", "y","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "Your basket is empty. Please add items before checking out.\n" in captured.out
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 4: LOGIN VALID BUY PRODUCT
def test_login_valid_shop_item_check_cart_pay_by_wallet_logout(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","all","y","71","c","y","w","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "Backpack added to your cart." in captured.out
    assert "['Backpack', 15.0, 1]" in captured.out
    assert "Thank you for your purchase, Samantha! Your remaining balance is 135.0" in captured.out 
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 5: LOGIN VALID BUY SEVERAL PRODUCTS
def test_login_valid_shop_several_items_check_cart_pay_by_wallet_logout(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","all","y","69","50","c","y","w","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "Notebook added to your cart." in captured.out
    assert "Batteries added to your cart." in  captured.out 
    assert "['Notebook', 2.0, 5]" in captured.out
    assert "['Batteries', 3.0, 6]" in captured.out
    assert "Thank you for your purchase, Samantha! Your remaining balance is 145.0" in captured.out 
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 6: LOGIN VALID CARD PAYMENT INVALID
def test_login_valid_shop_check_cart_pay_by_card_invalid(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","all","y","69","c","y","c","c","y","w","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "Notebook added to your cart." in captured.out
    assert "You don't have any cards on file." in captured.out 
    assert "Thank you for your purchase, Samantha! Your remaining balance is 148.0" in captured.out 
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 7: LOGIN VALID LOGOUT WITHOUT BUYING
def test_login_valid_shop_logout_without_buying(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","all","y","69","l","y"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "Notebook added to your cart." in captured.out
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 8: 
def test_login_invalid_checkout_logout(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","all","y","c","y","w","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 9: SEARCH INVALID PRODUCT
def test_login_search_invalid_product_logout(capsys):
    json_file = get_json("users.json")
    route_strings = ["Samantha","SecurePass123/^","hej","y","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert json_file == get_json("users_original.json")
    assert "Successfully logged in\n" in captured.out
    assert "['Product', 'Price', 'Units']" in captured.out 
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()
    
# TEST 10: REGISTER USER
def test_login_register_new_user(capsys):
    json_file = get_json("users.json")
    route_strings = ["Sofia","Slayslay!","y", "Slayslay!","Sofia","Slayslay!","all","y","l"]
    with patch('builtins.input', side_effect=route_strings):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Successfully logged in\n" in captured.out
    assert "You have been logged out" in captured.out
    assert json_file == get_json("users_original.json")
    rollback_json()