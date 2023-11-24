import pytest
from products import searchAndBuyProduct
import shutil
import os
from io import StringIO
import sys
import csv
from unittest.mock import patch
from login import login


@pytest.fixture
def copy_csv_file():
    #copy the CSV file
    shutil.copy('products.csv', 'copy_products.csv')
    yield
    #remove the copied CSV file
    os.remove('copy_products.csv')



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
def test_search_and_buy_product_successful_checkout(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '54', 'c','y']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Thank you for your purchase, Luna! Your remaining balance is 60.0" in captured.out


# Test 10: Insufficient balance
def test_search_and_buy_product_insufficient_balance(capsys):
    with patch('builtins.input', side_effect=["Luna", "Moonlight#456", 'all', 'y', '54', 'c','y']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase.\nPlease try again!" in captured.out
    