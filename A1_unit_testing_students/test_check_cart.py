import pytest
from checkout_and_payment import *
from unittest.mock import patch
from products import *
import shutil
import os

@pytest.fixture
def copy_csv_file():
  # Set up: Copy the CSV file
  shutil.copy('products.csv','copy_products.csv')
  yield
  #Remove the copied CSV file
  os.remove('copy_products.csv')
  
# Mock classes for testing
class MockUser:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = float(wallet)

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

def test_check_cart_with_items():
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("Computer", 50.0, 2)
    cart.add_item(product)

    with patch("builtins.input", side_effect=["y"]):
        check_cart_result = check_cart(user, cart)
    assert check_cart_result is None  
    
def test_check_cart_with_multiple_items(capsys): 
    user = MockUser("Helga", 600.0)
    cart = MockShoppingCart()
    product1 = MockProduct("Computer", 50.0, 2)
    product2 = MockProduct("Laptop", 20.0, 3)
    product3 = MockProduct("Desktop", 60.0, 3)
    cart.add_item(product1)
    cart.add_item(product2)
    cart.add_item(product3)
    
    with patch("builtins.input", side_effect=["y"]):
        check_cart_result = check_cart(user, cart)
        captured = capsys.readouterr()
        assert "Thank you for your purchase, Helga!" in captured.out
        assert user.wallet == 470.0  
        assert len(cart.items) == 0  
    assert check_cart_result is None  

def test_check_cart_without_items():
    user = MockUser("Olga", 100.0)
    cart = MockShoppingCart()

    with patch("builtins.input", side_effect=["n"]):
        check_cart_result = check_cart(user, cart)
    assert check_cart_result is False

def test_check_cart_with_insufficient_funds(capsys): 
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()
    product1 = MockProduct("Computer", 50.0, 2)
    product2 = MockProduct("Laptop", 20.0, 3)
    product3 = MockProduct("Desktop", 60.0, 3)
    cart.add_item(product1)
    cart.add_item(product2)
    cart.add_item(product3)
    
    with patch("builtins.input", side_effect=["y"]):
        check_cart_result = check_cart(user, cart)
        captured = capsys.readouterr()
        assert "You don't have enough money to complete the purchase." in captured.out
    assert check_cart_result is None  
    
def test_check_cart_with_no_items(capsys): 
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()

    with patch("builtins.input", side_effect=["y"]):
        check_cart(user, cart)
        captured = capsys.readouterr()
        assert "Your basket is empty. Please add items before checking out." in captured.out
        
