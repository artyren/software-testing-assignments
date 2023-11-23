import csv
from checkout_and_payment import *
import pytest
import shutil 
import os
from unittest.mock import * 

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
  
def test_load_products_from_file_containments(copy_csv_file):
  products = load_products_from_csv("copy_products.csv")
  assert products
  assert products[1].name == "Banana"
  assert products[1].price == 1
  assert products[1].units == 15
  
  
def test_load_products_from_changed_file(copy_csv_file):
  products = load_products_from_csv("copy_products.csv")
  assert products
  assert products[1].name == "Banana"
  assert products[1].price == 1
  assert products[1].units == 15
  
def test_load_non_existing_csv():
  with pytest.raises(FileNotFoundError) as err_str:
    load_products_from_csv("test.csv")
  assert "No such file or directory: 'test.csv'" in str(err_str.value)

def test_load_invalid_csv_key(invalid_products_csv_key):
    with pytest.raises(KeyError) as err_str:
        load_products_from_csv(invalid_products_csv_key)
    assert "Product" in str(err_str.value)

def test_load_valid_mock_csv(mock_csv):
  products = load_products_from_csv(mock_csv)
  assert products 
  
def test_load_change_mock_csv(mock_csv_float_error):
  with pytest.raises(ValueError) as err_str:
        load_products_from_csv(invalid_products_csv_key)
  assert "invalid literal for int() with base 10: '17.77'" in str(err_str.value)
  
def test_load_valid_mock_csv(mock_csv):
  products = load_products_from_csv(mock_csv)
  assert products 
  assert len(products) == 2
  assert products[0].name == "Testproduct"
  assert products[0].price == 29.95
  assert products[0].units == 17
  assert products[1].name == "Csvreader"
  assert products[1].price == 15.00
  assert products[1].units == 17
  
  
def test_load_valid_mock_diff_values_csv(mock_csv):
  products = load_products_from_csv(mock_csv)
  assert products 
  assert len(products) != 1
  assert products[0].name != "testproduct"
  assert products[0].price != 29.90
  assert products[0].units != 1
  assert products[1].name != "csvreader"
  assert products[1].price != 15.10
  assert products[1].units != 16

def test_load_change_mock_csv_val_error(mock_csv_float_error2):
  with pytest.raises(ValueError) as err_str:
        load_products_from_csv(mock_csv_float_error2)
  assert "invalid literal for int() with base 10: '15.05'" in str(err_str.value)