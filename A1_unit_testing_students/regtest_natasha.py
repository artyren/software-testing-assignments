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
def copy_users_file():
  # Set up: Copy the CSV file
  shutil.copy('users.json','copy_users.csv')
  yield
  #Remove the copied CSV file
  os.remove('copy_users.csv')


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
  

### help funcitons/fixtures ### 
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

def rollback_json():
    os.remove("users.json")
    os.system('cp users_backup.json users.json')

### login_test ##########################################################################################
# Test 1
def test_convo_route1(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["N", "N", "N"]):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Have a nice day!\n"
    assert json_file == get_json("users_original.json")

# Test 2
def test_convo_route2(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["Phoenix", "wrong"]):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Either username or password were incorrect\n"
    assert json_file == get_json("users_original.json")

# Test 3
def test_convo_route3(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["Phoenix", "Firebir&^d987"]):
        assert login() == {"username": "Phoenix", "wallet": 120 }
    captured = capsys.readouterr()
    assert captured.out == "Successfully logged in\n"
    assert json_file == get_json("users_original.json")

# Test 4
def test_convo_route4():
    route_strings = ["Fox", "fake", "Y", "T#st", "Testing#"]
    with patch('builtins.input', side_effect=route_strings):
        assert login() == None
    json_file = get_json("users.json")
    assert json_file != get_json("users_original.json")
    assert json_file[-1]["username"] == "Fox"
    assert json_file[-1]["password"] == "Testing#"
    assert json_file[-1]["wallet"] == 0
    reset_json()

# Test 5
def test_convo_route5(capsys):
    json_file = get_json("users.json")
    route_strings = ["Fox", "fake", "OASd", "N",]
    with patch('builtins.input', side_effect=route_strings):
        assert login() == None
    captured = capsys.readouterr()
    assert captured.out == "Answer in wrong format, try again\nHave a nice day!\n"
    assert json_file == get_json("users_original.json")






### logout_test ##########################################################################################
# Test 1
def test_cart_empty():
    cart = ShoppingCart()
    assert logout(cart) == True

# Test 2
def test_cart_string_input():
    with pytest.raises(Exception) as e:
        logout("cart")

# Test 3
def test_cart_int_input():
    with pytest.raises(Exception) as e:
        logout(1)

# Test 4
def test_cart_float_input():
    with pytest.raises(Exception) as e:
        logout(0.1)

# Test 5
def test_cart_list_input():
    with pytest.raises(Exception) as e:
        logout([ShoppingCart()])




##  test_display_csv_as_table #########################################################################################
#Test 1: check if the header is printed correctly
def test_display_csv_as_table_header(copy_csv_file, capsys):
    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    assert "['Product', 'Price', 'Units']" in captured.out


#Test 4: empty csv file
def test_display_csv_as_table_with_empty_csv_file(copy_csv_file):
    shutil.copy('copy_products.csv', 'tmp_copy_products.csv')
    open('tmp_copy_products.csv', 'w').close()
    with pytest.raises(StopIteration):
        display_csv_as_table('tmp_copy_products.csv')


#Test 5: check if the number of rows printed is equal to the number of rows in the csv file
def test_display_csv_as_table_length(copy_csv_file, capsys):
    #count how many rows there are in csv file
    rows_csv  = 0
    for row in open("copy_products.csv"): 
        rows_csv+= 1
    #count how many rows are printed 
    display_csv_as_table('copy_products.csv')
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    rows_printed = len(non_empty_lines)
    #check if the number of rows in the csv file equals the number of rows printed
    assert rows_printed == rows_csv

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





## test_display_filtered_table #######################################################################################
#Test 4: no argument passed to function
def test_display_filtered_table_no_arg(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_filtered_table()

#Test 5: too many arguments passed to function
def test_display_filtered_table_too_many_args(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_filtered_table('', '', '')


#Test 6: empty csv file
def test_display_filtered_table_with_empty_csv_file(copy_csv_file):
    shutil.copy('copy_products.csv', 'tmp_copy_products.csv')
    open('tmp_copy_products.csv', 'w').close()
    with pytest.raises(StopIteration):
        display_filtered_table('tmp_copy_products.csv', "")


#Test 7: no items are printed if empty string is searched
def test_display_filtered_table_search_empty_string(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', "")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    assert len(non_empty_lines) - 1 == 0 #-1 because the header is always printed


#Test 9: check if the header is printed correctly
def test_display_filtered_table_header(copy_csv_file, capsys):
    display_filtered_table('copy_products.csv', '')
    captured = capsys.readouterr()
    assert "['Product', 'Price', 'Units']" in captured.out



## test_load_products_from_csv #######################################################################################
# Test 6
def test_load_invalid_csv_key(invalid_products_csv_key):
    with pytest.raises(KeyError) as err_str:
        load_products_from_csv(invalid_products_csv_key)
    assert "Product" in str(err_str.value)

# Test 7
def test_load_valid_mock_csv(mock_csv):
  products = load_products_from_csv(mock_csv)
  assert products 
  
# Test 8
def test_load_change_mock_csv(mock_csv_float_error):
  with pytest.raises(ValueError) as err_str:
        load_products_from_csv(invalid_products_csv_key)
  assert "invalid literal for int() with base 10: '17.77'" in str(err_str.value)
  
# Test 9
def test_load_valid_mock_csv2(mock_csv):
  products = load_products_from_csv(mock_csv)
  assert products 
  assert len(products) == 2
  assert products[0].name == "Testproduct"
  assert products[0].price == 29.95
  assert products[0].units == 17
  assert products[1].name == "Csvreader"
  assert products[1].price == 15.00
  assert products[1].units == 17
  

def test_load_products_from_changed_file(copy_csv_file):
  products = load_products_from_csv("copy_products.csv")
  assert products
  assert products[1].name == "Banana"
  assert products[1].price == 1
  assert products[1].units == 15
  

## test_check_cart #######################################################################################
#Test 6 
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
    
#Test 7
def test_check_cart_with_unvalid_cart(): 
    user = MockUser("Helga", 500.0)
    cart = "cart"
    with patch("builtins.input", side_effect=["y"]):
        with pytest.raises(AttributeError) as err_str:
            check_cart(user, cart)
        assert "'str' object has no attribute 'retrieve_item'" in str(err_str.value)

#Test 8
def test_check_cart_with_other_than_yes_no():
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("Computer", 50.0, 2)
    cart.add_item(product)
    with patch("builtins.input", side_effect=["hej"]):
        check_cart_result = check_cart(user, cart)
    assert check_cart_result is False       

#Test 9
def test_check_cart_with_other_than_yes_no_no_items():
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()
    with patch("builtins.input", side_effect=["no"]):
        check_cart_result = check_cart(user, cart)
    assert check_cart_result is False
    

def test_check_cart_with_no_items(capsys): 
    user = MockUser("Helga", 100.0)
    cart = MockShoppingCart()

    with patch("builtins.input", side_effect=["y"]):
        check_cart(user, cart)
        captured = capsys.readouterr()
        assert "Your basket is empty. Please add items before checking out." in captured.out


## test_checkout #######################################################################################
# Test 6
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

# Test 7
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
    
# Test 8
def test_checkout_user_invalid():
    user = "Robin"
    cart = MockShoppingCart()
    product = MockProduct("Computer", 20.0, 3)
    cart.add_item(product)
    with pytest.raises(AttributeError) as err_str:
        checkout(user, cart)
    assert "'str' object has no attribute 'wallet'" in str(err_str.value)
    
# Test 9
def test_checkout_product_invalid():
    user = MockUser("Robin", 100.0)
    cart = MockShoppingCart()
    product = MockProduct("Computer", 20.0, 1.5)
    cart.add_item(product)
    cart.add_item(product)
    with pytest.raises(ValueError) as err_str:
       checkout(user, cart)
    assert "list.remove(x): x not in list" in str(err_str.value)
    

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
    

## test_search_and_buy_product #######################################################################################
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


#Test 8: right item was added to cart, choosing item 70 from the print chooses item 70 from the csv file
def test_search_and_buy_product_correct_item(copy_csv_file, capsys):
    row_55_csv = None
    i = 0
    for row in open("copy_products.csv"): 
        if i == 55:
            row_55_csv = row
        i+=1
    product_at_row_55 = row_55_csv.strip().split(',')[0]
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '55']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    lines = captured.out.split('\n')
    relevant_line = None
    for line in lines:
        if 'added to your cart' in line:
            relevant_line = line
    assert relevant_line == f"{product_at_row_55} added to your cart."
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y',  "l", 'y']):
        searchAndBuyProduct()


#Test 9: successful checkout
def test_search_and_buy_product_successful_checkout(capsys, copy_users_file):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '54', 'c','y', 'l']):
        # with pytest.raises(StopIteration):
        searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Thank you for your purchase, Luna! Your remaining balance is 60.0" in captured.out

#Test 5: search for specific item
def test_search_and_buy_product_search_specific_product(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'Banana']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Banana" in captured.out


## test_checkoutAndPayment #######################################################################################

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


# Test 9
def test_empty_cart_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}
    with patch('builtins.input', side_effect=["c", "y", "l","y"]):
        checkoutAndPayment(login_info)
    captured = capsys.readouterr()
    assert "Your basket is empty. Please add items before checking out." in captured.out
    rollback_json()
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 10
def test_logout_with_leftover_cart(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}
    with patch('builtins.input', side_effect=["59", "l", "y"]):
        checkoutAndPayment(login_info)
    captured = capsys.readouterr()
    assert "Your cart is not empty.You have following items" in captured.out
    rollback_json()
    data = get_json("users.json")
    assert data == get_json("users_backup.json")

# Test 11
def test_deny_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}
    with patch('builtins.input', side_effect=["59", "c", "n", "l", "y"]):
        checkoutAndPayment(login_info)
    captured = capsys.readouterr()
    assert "Your cart is not empty.You have following items" in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")
    rollback_json()

#tests for new implementation ##############################################################################
#test adding a user that does not exist and check that all new fields are correct (no credit card)
def test_new_implementation_1(capsys):
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    user_exists = False
    for user in data:
        if user["username"] == new_username:
            user_exists = True
    assert user_exists == False
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'n']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "You were successfully registered!" in captured.out
    data = get_json("users.json")
    assert data[-1]["username"] == new_username
    assert data[-1]["address"] == 'uppsala 123'
    assert data[-1]["phone"] == '1122331122'
    assert data[-1]["email"] == new_username+'@mail.com'
    assert data[-1]["credit_cards"] == []
    rollback_json()


#test adding a user that does not exist and check that all new fields are correct (with credit card)
def test_new_implementation_2():
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'y', '555-555-555-555', '12/12', new_username, '123' ]):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    data = get_json("users.json")
    assert len(data[-1]["credit_cards"]) != 0
    assert data[-1]["credit_cards"][0]['card_number'] == '555-555-555-555'
    assert data[-1]["credit_cards"][0]['expiry_date'] == '12/12'
    assert data[-1]["credit_cards"][0]['name_on_card'] == new_username
    assert data[-1]["credit_cards"][0]['cvv'] == '123'
    rollback_json()

#add new user with new fields, edit cvv of card and check that it is updated correctly
def test_new_implementation_3():
    data = get_json("users.json")
    new_username = "NewUser" + str(len(data)+1)
    with patch('builtins.input', side_effect=[new_username, "", 'y', 'Hejsan123!', 'uppsala 123', '1122331122', new_username+'@mail.com', 'y', '555-555-555-555', '12/12', new_username, '123' ]):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]["credit_cards"][0]['cvv'] == '123'
    with patch('builtins.input', side_effect=[new_username, 'Hejsan123!', 'all', 'y', 'e', '4', '1', '4', '000', '5'  ]):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    data = get_json("users.json")
    assert data[-1]["credit_cards"][0]['cvv'] == '000'
    rollback_json()
