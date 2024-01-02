from login import *
from logout import *
from checkout_and_payment import *
from products import display_filtered_table
from products import display_csv_as_table
import pytest
from unittest.mock import patch
from checkout_and_payment import Product, ShoppingCart
import shutil
import os
import csv
from unittest.mock import * 
from products import *
import random


#----------------- LOGIN -------------------------
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
    
def test_convo_route1(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["N", "N", "N"]):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Have a nice day!\n"
    assert json_file == get_json("users_original.json")

def test_convo_route2(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["Phoenix", "wrong"]):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Either username or password were incorrect\n"
    assert json_file == get_json("users_original.json")

def test_pass_length():
    assert pass_check("G#") == False
    assert pass_check("GGGHJ#") == False

def test_pass_symbol():
    assert pass_check("kajsnDkdjWankjDdn") == False
    assert pass_check("GGGHJasdadadad") == False

def test_pass_upper():
    assert pass_check("") == False
    assert pass_check("GGGHJ#") == False


##-----------------LOGOUT-------------------------
def test_cart_empty():
    cart = ShoppingCart()
    assert logout(cart) == True

def test_cart_int_input():
    with pytest.raises(Exception) as e:
        logout(1)

def test_cart_wrong_input():
    with pytest.raises(Exception) as e:
        logout((ShoppingCart(), ShoppingCart()))

def test_product_prints_and_exit(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Eggs", 15, 4))
    cart.add_item(Product("Chips", 30, 1))
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Eggs', 15.0, 4]\n['Chips', 30.0, 1]\n"

def test_product_prints_and_stay(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Bike", 1500, 1))
    with patch('builtins.input', return_value="N"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Bike', 1500.0, 1]\n"


##------------------CSV_DISPLAY-----------------

@pytest.fixture
def copy_csv_file():
    #copy the CSV file
    shutil.copy('products.csv', 'copy_products.csv')
    yield
    #remove the copied CSV file
    os.remove('copy_products.csv')
    if os.path.isfile('tmp_copy_products.csv'):
        os.remove('tmp_copy_products.csv')

#Test 1: check if the header is printed correctly
def test_display_csv_as_table_header(copy_csv_file, capsys):
    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    assert "['Product', 'Price', 'Units']" in captured.out

#Test 2: check if a selected row is printed correctly
def test_display_csv_as_table_selected_row(copy_csv_file, capsys):
    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    assert "['Apple', '2', '10']" in captured.out


#Test 3: nonexistent file
def test_display_csv_as_table_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table('nonexistent_file.csv')


#Test 6: no argument passed to function
def test_display_csv_as_table_no_arg(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_csv_as_table()

#Test 10: check if number of newlines in print equals number of lines in csv file
# i.e check that each row in the csv file is printed on a new line
def test_display_csv_as_table_number_of_newlines(copy_csv_file, capsys):
    rows_csv  = 0
    for row in open("copy_products.csv"): 
        rows_csv+= 1

    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    newline_count = captured.out.count('\n')

    assert rows_csv == newline_count



#-------------------------FILTERED----------------------
#Test 1: check if the searched item is in the printed result
def test_display_filtered_table_search_in_printed_res(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', "Apple")
    captured = capsys.readouterr()
    assert "Apple" in captured.out

#Test 3: no items are printed if nonexistent item is searched
def test_display_filtered_table_search_nonexistent(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', "nonexistent")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]

    assert len(non_empty_lines) - 1 == 0 #-1 because the header is always printed

#Test 4: no argument passed to function
def test_display_filtered_table_no_arg(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_filtered_table()

#Test 5: too many arguments passed to function
def test_display_filtered_table_too_many_args(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_filtered_table('', '', '')

#Test 10: check if randomly picked item is printed 
def test_display_filtered_table_random_item(copy_csv_file, capsys):
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
    random_item = random_row_csv[0]
    
    display_filtered_table('copy_products.csv', random_item)
    captured = capsys.readouterr()
    assert random_item in captured.out




#----------------------LOAD_PRODUCTS---------------------

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

def test_load_products_from_empty_file(tmp_path):
    csv_file_path = tmp_path / "empty_test_products.csv"
    open(csv_file_path, 'w').close()

    products = load_products_from_csv(csv_file_path)
    assert not products
    
def test_load_products_from_file(copy_csv_file):
    products = load_products_from_csv("copy_products.csv")
    assert products

def test_load_invalid_csv_key(invalid_products_csv_key):
    with pytest.raises(KeyError) as err_str:
        load_products_from_csv(invalid_products_csv_key)
    assert "Product" in str(err_str.value)
  
def test_load_change_mock_csv(mock_csv_float_error):
    with pytest.raises(ValueError) as err_str:
            load_products_from_csv(invalid_products_csv_key)
    assert "invalid literal for int() with base 10: '17.77'" in str(err_str.value)
  

def test_load_change_mock_csv_val_error(mock_csv_float_error2):
    with pytest.raises(ValueError) as err_str:
            load_products_from_csv(mock_csv_float_error2)
    assert "invalid literal for int() with base 10: '15.05'" in str(err_str.value)
#-------------------------CHECK_CART----------------------
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

def test_check_cart_with_unvalid_user_yes(): 
    user = "Helga",
    cart = MockShoppingCart()
    product1 = MockProduct("Computer", 50.0, 2)
    product2 = MockProduct("Laptop", 20.0, 3)
    product3 = MockProduct("Desktop", 60.0, 3)
    cart.add_item(product1)
    cart.add_item(product2)
    cart.add_item(product3)
    
    with patch("builtins.input", side_effect=["y"]):
        with pytest.raises(AttributeError) as err_str:
            check_cart(user, cart)
        assert "'tuple' object has no attribute 'wallet'" in str(err_str.value)
    
def test_check_cart_with_unvalid_cart(): 
    user = MockUser("Helga", 500.0)
    cart = "cart"
    
    with patch("builtins.input", side_effect=["y"]):
        with pytest.raises(AttributeError) as err_str:
            check_cart(user, cart)
        assert "'str' object has no attribute 'retrieve_item'" in str(err_str.value)

def test_check_cart_with_many_items(capsys): 
    user = MockUser("Helga", 10000000.0)
    cart = MockShoppingCart()
    product1 = MockProduct("Computer", 50.0, 50)
    product2 = MockProduct("Laptop", 20.0, 50)
    product3 = MockProduct("Desktop", 60.0, 50)
    count = 45
    while count>0:
        cart.add_item(product1)
        cart.add_item(product2)
        cart.add_item(product3)
        count = count - 1
    
    with patch("builtins.input", side_effect=["y"]):
        check_cart_result = check_cart(user, cart)
        captured = capsys.readouterr()
        assert "Thank you for your purchase, Helga!" in captured.out
        assert user.wallet == 9994150.0
        assert len(cart.items) == 0  
    assert check_cart_result is None  

#-----------------------------CHECKOUT_CART----------------

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
    
def test_successful_checkout_same_product_twice(capsys):
    user = MockUser("Robin", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("Computer", 20.0, 3)
    
    cart.add_item(product)
    cart.add_item(product)

    checkout(user, cart)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Robin!" in captured.out
    assert user.wallet == 60.0  
    assert len(cart.items) == 0  

def test_checkout_all_instances_of_product():
    user = MockUser("Robin", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("Computer", 20.0, 3)
    
    cart.add_item(product)
    cart.add_item(product)
    cart.add_item(product)

    with pytest.raises(ValueError) as err_str:
        checkout(user, cart)
    assert "list.remove(x): x not in list" in str(err_str.value)
    

def test_checkout_cart_invalid():
    user = MockUser("Robin", 100.0)
    cart = "cart"
    
    with pytest.raises(AttributeError) as err_str:
       checkout(user, cart)
    assert "'str' object has no attribute 'items'" in str(err_str.value)


#-------------------SEARCH_AND_BUY--------------------
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

#Test 6: logout
def test_search_and_buy_product_logout(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', 'l']):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "You have been logged out" in captured.out


#Test 7: checkout empty cart
def test_search_and_buy_product_empty_checkout(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', 'c', 'y']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Your basket is empty. Please add items before checking out." in captured.out

# Test 10: Insufficient balance
def test_search_and_buy_product_insufficient_balance(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '54', 'c','y']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase.\nPlease try again!" in captured.out
    
#---------------------CHECKOUT_AND_PAYMENT-----------------
def rollback_json():
    os.remove("users.json")
    os.system('cp users_backup.json users.json')


def get_json(path):
    with open(path, "r") as users:
        return json.load(users)



# Test 5
def test_success_one_item_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #59. Blender = 30$
    with patch('builtins.input', side_effect=["59", "c", "y", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Blender added to your cart." in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 30.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 30
    reset_json()


# Test 6
def test_success_multiple_item_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #59. Vaccuum Cleaner = 30$
    # Test item: #67. Gloves  =  5$
    with patch('builtins.input', side_effect=["59", "67", "c", "y", "l","y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Vaccuum Cleaner added to your cart." in captured.out
    assert "Gloves added to your cart." in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 25.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
           assert entry["wallet"] == 25
    reset_json()

# Test 12
def test_cancel_logout_forgotten_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #58. Blender = 30$
    with patch('builtins.input', side_effect=["59", "l", "n", "c", "y", "l","y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    print(captured.out)
    assert "Blender added to your cart." in captured.out
    assert "Your cart is not empty.You have following items" in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 30.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 30
    reset_json()


# Test 13
def test_insufficient_funds(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #52. Laptop = 800$
    with patch('builtins.input', side_effect=["52", "c", "y", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Laptop added to your cart." in captured.out
    assert "You don't have enough money to complete the purchase.\nPlease try again!" in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 14
def test_wallet_update(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #1. Apple = 2$
    # First checkout
    with patch('builtins.input', side_effect=["1", "c", "y", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Oliver! Your remaining balance is 58.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 58
            login_info["wallet"] = entry["wallet"] # modify stub with updated wallet

    # Second checkout
    with patch('builtins.input', side_effect=["1", "c", "y", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Oliver! Your remaining balance is 56.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 56

    reset_json()

#-------------------------REMOVE_ITEM---------------------------------

def test_remove_item(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}
    pre_products = load_products_from_csv("products.csv") 

    with patch('builtins.input', side_effect=["52", "r", "2", "r", "f", "r", "1", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Laptop added to your cart." in captured.out
    assert "Choice out of range" in captured.out
    assert "Choice is not a numeric one." in captured.out
    assert "Laptop has been removed." in captured.out
    post_products = load_products_from_csv("products.csv")
    assert pre_products[51].units == post_products[51].units 
    data = get_json("users.json")
    assert data == get_json("users_backup.json")

def test_remove_item_no_items(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}
    pre_products = load_products_from_csv("products.csv")

    with patch('builtins.input', side_effect=["r", "2", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Choice out of range" in captured.out
    post_products = load_products_from_csv("products.csv")
    for i in range(len(post_products)):
        assert pre_products[i].units == post_products[i].units 
    data = get_json("users.json")
    assert data == get_json("users_backup.json")

def test_remove_item_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}
    pre_products = load_products_from_csv("products.csv")

    with patch('builtins.input', side_effect=["51", "51", "r", "2", "c", "y", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Phone Charger added to your cart." in captured.out
    assert "Phone Charger has been removed." in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 55" in captured.out
    post_products = load_products_from_csv("products.csv")
    assert pre_products[50].units != post_products[50].units
    assert pre_products[50].units == 3
    backup_p = load_products_from_csv("products_backup.csv")
    with open('products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in backup_p:
            writer.writerow([backup_p.name, backup_p.price, backup_p.units])

    reset_json()
    data = get_json("users.json")
    assert data == get_json("users_backup.json")