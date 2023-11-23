import pytest
from products import searchAndBuyProduct
import shutil
import os
from io import StringIO
import sys
import csv
from unittest.mock import patch



# @pytest.fixture
# def login():
#     #copy the CSV file
#     shutil.copy('products.csv', 'copy_products.csv')
#     yield
#     #remove the copied CSV file
#     os.remove('copy_products.csv')
#     if os.path.isfile('tmp_copy_products.csv'):
#         os.remove('tmp_copy_products.csv')


# @pytest.fixture
# def fakefunc(mocker):
#     return mocker.patch('products.searchAndBuyProduct')



# #Test 1: successful login
# def test_search_and_buy_product_login(capsys):
#     with pytest.raises(KeyboardInterrupt):   
#         with patch('builtins.input', side_effect=["Luna", "Moonlight#456", KeyboardInterrupt]):
#             searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Successfully logged in" in captured.out

# #Test 2: Failed login
# def test_search_and_buy_product_login2(capsys):
#     with pytest.raises(KeyboardInterrupt):
#         with patch('builtins.input', side_effect=["Wrong", "login",KeyboardInterrupt]):
#             searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Either username or password were incorrect" in captured.out


# #Test 3: successfully add something to cart
# def test_search_and_buy_product_add_to_cart(capsys):
#     with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '71', 'c', KeyboardInterrupt]):
#         with pytest.raises(KeyboardInterrupt):
#             searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Backpack" in captured.out


# #Test 4: select item with index out of bounds
# def test_search_and_buy_product_index_out_of_bounds(capsys):
#     with pytest.raises(KeyboardInterrupt):
#         with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '1000', KeyboardInterrupt]):
#             searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Invalid input. Please try again" in captured.out


# #Test 5: search for specific item
# def test_search_and_buy_product_search_specific_product(capsys):
#     with pytest.raises(KeyboardInterrupt):
#         with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'Banana', KeyboardInterrupt]):
#             searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Banana" in captured.out


# #Test 6: logout
# def test_search_and_buy_product_logout(capsys):
#     with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', 'l']):
#         searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "You have been logged out" in captured.out


# #Test 7: checkout empty cart
# def test_search_and_buy_product_empty_checkout(capsys):
#     with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', 'c', 'y']):
#         searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Your basket is empty. Please add items before checking out." in captured.out


#Test 8: right item was added to cart, choosing 70 chooses item 70 from the print that shows all items
# def test_search_and_buy_product_successful_checkout(capsys):
#     with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '70', ....]):
#         searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Your basket is empty. Please add items before checking out." in captured.out


#Test 9: successful checkout
# def test_search_and_buy_product_successful_checkout(capsys):
#     with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '70', 'c','y']):
#         searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "Thank you for your purchase, Luna! Your remaining balance is 89.5" in captured.out


#Test 10: Insufficient balance
# def test_search_and_buy_product_insufficient_balance(capsys):
#     with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '55', 'c','y']):
#         searchAndBuyProduct()
#     captured = capsys.readouterr()
#     assert "You don't have enough money to complete the purchase. Please try again!" in captured.out
    