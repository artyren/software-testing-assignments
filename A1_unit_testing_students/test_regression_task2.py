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


### TEST_LOGIN FUNCTION TESTS ###
# TEST 8
def test_pass_upper():
    assert pass_check("") == False
    assert pass_check("GGGHJ#") == False

# TEST 9
def test_pass_correct():
    assert pass_check("LowRoar12<3") == True
    assert pass_check("HEALTHofficial#") == True
    assert pass_check("%AmericanNonjaWarrior%") == True
    assert pass_check("Wooooohaaaaa#") == True

# TEST 10
def test_pass_arg_int():
    with pytest.raises(TypeError) as e:
        pass_check(1)

# TEST 11
def test_pass_arg_float():
    with pytest.raises(TypeError) as e:
        pass_check(0.1)

#TEST 12
def test_pass_arg_list():
    with pytest.raises(TypeError) as e:
        pass_check(["pass"])

### TEST_LOGOUTFUNCTION TESTS ###
# TEST 8
def test_product_prints_and_stay(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Bike", 1500, 1))
    with patch('builtins.input', return_value="N"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Bike', 1500.0, 1]\n"

# TEST 9
def test_product_prints_and_stay(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Bike", 1500, 1))
    with patch('builtins.input', return_value="N"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Bike', 1500.0, 1]\n"

# TEST 10
def test_product_prints_and_wrong_input(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    with patch('builtins.input', return_value="kjasdlfjbalsd"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n"

# TEST 11
def test_cart_clear(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n"
    assert cart.items == []

# TEST 12
def test_cart_clear(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n"
    assert cart.items == []

### TEST_DISPLAY_CSV_AS_TABLE TESTS ###
#Test 2: check if a selected row is printed correctly
def test_display_csv_as_table_selected_row(copy_csv_file, capsys):
    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    assert "['Apple', '2', '10']" in captured.out


#Test 3: nonexistent file
def test_display_csv_as_table_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table('nonexistent_file.csv')

#Test 7: no argument passed to function
def test_display_csv_as_table_too_many_args(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_csv_as_table('', '', '')


#Test 8: check if last element in the csv file is the last row printed
def test_display_csv_as_table_hej(copy_csv_file, capsys):
    last_row_csv = None
    for row in open("copy_products.csv"): 
        last_row_csv = row
    
    #convert last row in csv file to a list of strings
    last_row_csv_list = last_row_csv.strip().split(',')

    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]

    #convert last printed row to a list of strings
    last_printed_row = eval(non_empty_lines[-1])

    assert last_row_csv_list == last_printed_row
   
#Test 9: check if random index row in the csv file is the same index printed
def test_display_csv_as_table_print_random_index(copy_csv_file, capsys):
    rows_csv  = 0
    for row in open("copy_products.csv"): 
        rows_csv+= 1

    random_number = random.randint(0, rows_csv)

    i = 0
    random_row_csv =  None
    for row in open("copy_products.csv"): 
        if i == random_number:
            random_row_csv = row
        i+= 1
    
    random_row_csv = random_row_csv.strip().split(',')

    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    random_row_printed = eval(non_empty_lines[random_number])

    assert random_row_csv == random_row_printed

### TEST_FILTERED_TABLE TESTS ###
#Test 1: check if the searched item is in the printed result
def test_display_filtered_table_search_in_printed_res(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', "Apple")
    captured = capsys.readouterr()
    assert "Apple" in captured.out

#Test 2: check if the searched item is the only item printed (no other items)
def test_display_filtered_table_only_search_printed(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', "Apple")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]

    assert len(non_empty_lines) - 1 == 1 and "Apple" in captured.out #-1 because the header is also printed

#Test 3: no items are printed if nonexistent item is searched
def test_display_filtered_table_search_nonexistent(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', "nonexistent")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]

    assert len(non_empty_lines) - 1 == 0 #-1 because the header is always printed
    
#Test 8: header column "Product" is changed to something else
def test_display_filtered_table_different_header(copy_csv_file, capsys):
    shutil.copy('copy_products.csv', 'tmp_copy_products.csv')
    with open('tmp_copy_products.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        rows = list(csv_reader)
    header_index = rows[0].index('Product')
    rows[0][header_index] = "Hello"
    with open('tmp_copy_products.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)
    with pytest.raises(ValueError):
        display_filtered_table('tmp_copy_products.csv', "")

#Test 9: check if the header is printed correctly
def test_display_filtered_table_header(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', '')
    captured = capsys.readouterr()
    assert "['Product', 'Price', 'Units']" in captured.out

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
    

### SEARCH_AND_BUY_PRODUCTS TEST FUNCTIONS ###
#Test 1: successful login
def test_search_and_buy_product_login(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456"]):
         with pytest.raises(StopIteration):  
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Successfully logged in" in captured.out


#Test 2: successfully add one item to cart
def test_search_and_buy_product_add_to_cart(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '71', 'c']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Backpack" in captured.out
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y',  "l", 'y']):
        searchAndBuyProduct()

#Test 3: add multiple items to cart
def test_search_and_buy_product_add_multiple_to_cart(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '1', '2', '3', 'c']):
         with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Apple" in captured.out
    assert "Banana" in captured.out
    assert "Orange" in captured.out
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y',  "l", 'y']):
        searchAndBuyProduct()

#Test 4: select item with index out of bounds
def test_search_and_buy_product_index_out_of_bounds(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '1000']):
        with pytest.raises(StopIteration): 
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Invalid input. Please try again" in captured.out


#Test 5: search for specific item
def test_search_and_buy_product_search_specific_product(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'Banana']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Banana" in captured.out


### CHECKOUT_AND_PAYMENT TEST FUNCTIONS ###
def rollback_json():
    os.remove("users.json")
    os.system('cp users_backup.json users.json')


def get_json(path):
    with open(path, "r") as users:
        return json.load(users)


# Test 1
def test_invalid_login_info():
    login_info = {"username": "Benjamin"}
    with pytest.raises(KeyError) as err_msg:
        checkoutAndPayment(login_info)
    assert "'wallet'" in str(err_msg.value)


# Test 2
def test_invalid_wallet_value():
    login_info = {"username": "Benjamin", "wallet": "money"}
    with pytest.raises(ValueError) as err_msg:
        checkoutAndPayment(login_info)
    assert "could not convert string to float: 'money'" in str(err_msg.value)


# Test 3
def test_logout_no_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "added to your cart" not in captured.out
    assert "You have been logged out" in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 4
def test_invalid_option(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["f", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Invalid input. Please try again." in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")

# TEST 8
def test_invalid_product_selection(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["0", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Invalid input. Please try again." in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")

### WALLET OR CARD IMPLEMENTATION TEST FUNCTIONS ###
def test_pay_with_wallet_card_implemented(capsys):
    user = MockUser("Robin", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("CheapComputer", 20.0, 2)
    
    cart.add_item(product)

    with patch("builtins.input", side_effect=["w"]):
        result = checkout(user, cart)
        captured = capsys.readouterr()
        assert "Thank you for your purchase, Robin!" in captured.out
        assert user.wallet == 80.0  
        assert len(cart.items) == 0  
    assert result is None 

def test_pay_with_card(capsys):
    user = MockUser("Robin", 100.0)
    user.add_card("MasterVisa", 120.0)
    cart = MockShoppingCart()
    product = MockProduct("CheapComputer", 20.0, 2)
    
    cart.add_item(product)

    with patch("builtins.input", side_effect=["c", "1"]):
        result = checkout(user, cart)
        captured = capsys.readouterr()
        assert "\nSelect a card:" in captured.out
        assert "Thank you for your purchase, Robin!" in captured.out
        assert user.wallet == 100.0 
        assert user.cards[0]['balance'] == 100.0   
        assert len(cart.items) == 0  
    assert result is None 

def test_pay_with_card_several_cards(capsys):
    user = MockUser("Robin", 100.0)
    user.add_card("MasterVisa", 120.0)
    user.add_card("VisaMaster", 140.0)
    user.add_card("CardElite", 1000.0)
    cart = MockShoppingCart()
    product = MockProduct("CheapComputer", 20.0, 2)
    
    cart.add_item(product)

    with patch("builtins.input", side_effect=["c", "3"]):
        result = checkout(user, cart)
        captured = capsys.readouterr()
        assert "\nSelect a card:" in captured.out
        assert "Thank you for your purchase, Robin!" in captured.out
        assert user.wallet == 100.0  
        assert user.cards[0]['balance'] == 120.0 
        assert user.cards[1]['balance'] == 140.0 
        assert user.cards[2]['balance'] == 980.0    
        assert len(cart.items) == 0  
    assert result is None 
