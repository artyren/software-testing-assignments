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
  
@pytest.fixture
def invalid_products_csv_key(tmp_path):
  csv_path = tmp_path / "invalid_products_key.csv"
  with open(csv_path, 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile)
      csv_writer.writerow(["InvalidHeader1", "InvalidHeader2", "InvalidHeader3"])
      csv_writer.writerow(["Product1", "10.99", "5"])
  return csv_path

@pytest.fixture
def mock_csv(mocker):
  return mocker.patch('builtins.open', new_callable=mock_open,
    read_data='Product,Price,Units\n"Testproduct",29.95,17\n"Csvreader",15.00,17')
  
@pytest.fixture
def mock_csv_float_error(mocker):
  return mocker.patch('builtins.open', new_callable=mock_open,
    read_data='Product,Price,Units\n"Testproduct",29.95,17.77\n"Csvreader",15.00,17')
  
@pytest.fixture
def mock_csv_float_error2(mocker):
  return mocker.patch('builtins.open', new_callable=mock_open,
    read_data='Product,Price,Units\n"Testproduct",29.95,17\n"Csvreader",15.00,15.05')

  
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


### TODO: TEST_LOGIN FUNCTION TESTS ###

### TODO: TEST_LOGOUTFUNCTION TESTS ###

### TODO: TEST_DISPLAY_CSV_AS_TABLE TESTS ###

### TODO: TEST_FILTERED_TABLE TESTS ###

### LOAD_PRODUCTS_FROM_CSV FUNCTION TESTS ###
## Test 1 ##
def test_load_products_from_empty_file(tmp_path):
  csv_file_path = tmp_path / "empty_test_products.csv"
  open(csv_file_path, 'w').close()

  products = load_products_from_csv(csv_file_path)
  assert not products

## Test 2 ##
def test_load_products_from_file(copy_csv_file):
  products = load_products_from_csv("copy_products.csv")
  assert products

## Test 3 ##
def test_load_products_from_file_containments(copy_csv_file):
  products = load_products_from_csv("copy_products.csv")
  assert products
  assert products[1].name == "Banana"
  assert products[1].price == 1
  assert products[1].units == 15
  
## Test 4 ##
def test_load_products_from_changed_file(copy_csv_file):
  products = load_products_from_csv("copy_products.csv")
  assert products
  assert products[1].name == "Banana"
  assert products[1].price == 1
  assert products[1].units == 15

## Test 5 ##
def test_load_non_existing_csv():
  with pytest.raises(FileNotFoundError) as err_str:
    load_products_from_csv("test.csv")
  assert "No such file or directory: 'test.csv'" in str(err_str.value)

### CHECK_CART FUNCTION TESTS ###

## TEST 1 ##
def test_check_cart_with_items():
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("Computer", 50.0, 2)
    cart.add_item(product)

    with patch("builtins.input", side_effect=["y"]):
        check_cart_result = check_cart(user, cart)
    assert check_cart_result is None  

## TEST 2 ##
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

## TEST 3 ##
def test_check_cart_without_items():
    user = MockUser("Olga", 100.0)
    cart = MockShoppingCart()

    with patch("builtins.input", side_effect=["n"]):
        check_cart_result = check_cart(user, cart)
    assert check_cart_result is False

## TEST 4 ##
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

## TEST 5 ##
def test_check_cart_with_no_items(capsys): 
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()

    with patch("builtins.input", side_effect=["y"]):
        check_cart(user, cart)
        captured = capsys.readouterr()
        assert "Your basket is empty. Please add items before checking out." in captured.out
        
### CHECKOUT TEST FUNCTIONS #####
## Test 1 ##
#Test empty cart
def test_empty_cart_checkout(capsys):
    user = MockUser("Olof", 100.0)
    cart = MockShoppingCart()

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "Your basket is empty. Please add items before checking out." in captured.out

## Test 2 ##
#Test case for insufficient funds
def test_insufficient_funds(capsys):
    user = MockUser("Helga", 50.0)
    cart = MockShoppingCart()
    product = MockProduct("CheapDesktop", 60.0, 1)
    
    cart.add_item(product)

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out

## Test 3 ##
def test_insufficient_funds_several_products(capsys):
    user = MockUser("Helga", 50.0)
    cart = MockShoppingCart()
    product1 = MockProduct("Computer", 20.0, 3)
    product2 = MockProduct("Desktop", 60.0, 3)
    
    cart.add_item(product1)
    cart.add_item(product2)

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out

## Test 4 ##
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

## Test 5 ##
def test_successful_checkout_several_products(capsys):
    user = MockUser("Robin", 100.0)
    cart = MockShoppingCart()
    product1 = MockProduct("Computer", 20.0, 3)
    product2 = MockProduct("Desktop", 60.0, 3)
    
    cart.add_item(product1)
    cart.add_item(product2)

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Robin!" in captured.out
    assert user.wallet == 20.0  
    assert len(cart.items) == 0  
    

### TODO: SEARCH_AND_BUY_PRODUCTS TEST FUNCTIONS ###

### TODO: CHECKOUT_AND_PAYMENT TEST FUNCTIONS ###

### WALLET OR CARD IMPLEMENTATION TEST FUNCTIONS ###
def test_pay_with_wallet_card_implemented():
    return 0

def test_pay_with_card():
    return 0

def test_pay_with_card_several_cards():
    return 0