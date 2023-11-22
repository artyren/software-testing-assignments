from checkout_and_payment import *
from products import *
import shutil
import os 
import pytest

@pytest.fixture
def copy_csv_file():
  # Set up: Copy the CSV file
  shutil.copy('products.csv','copy_products.csv')
  yield
  #Remove the copied CSV file
  os.remove('copy_products.csv')
  
#Mock classes for testing
class MockProduct:
    def __init__(self, name, price, units):
        self.name = name
        self.price = float(price)
        self.units = int(units)
    def get_product(self):
        return [self.name, self.price, self.units]

class MockUser:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = float(wallet)

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
    

#Test empty cart
def test_empty_cart_checkout(capsys):
    user = MockUser("Olof", 100.0)
    cart = MockShoppingCart()

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "Your basket is empty. Please add items before checking out." in captured.out

#Test case for insufficient funds
def test_insufficient_funds(capsys):
    user = MockUser("Helga", 50.0)
    cart = MockShoppingCart()
    product = MockProduct("CheapDesktop", 60.0, 1)
    
    cart.add_item(product)

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out
    
def test_successful_checkout(capsys):
    user = MockUser("Robin", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("CheapComputer", 20.0, 2)
    
    cart.add_item(product)

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Robin!" in captured.out
    assert user.wallet == 80.0  
    assert len(cart.items) == 0  


