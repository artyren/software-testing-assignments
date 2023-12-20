import pytest
from test_search_and_buy_product import *

# Define a fixture to set up and tear down the regtest fixture for all tests
@pytest.fixture(autouse=True)
def setup_and_teardown_regtest(regtest):
    yield
    regtest.clear()  # Clear regtest data after each test function

# Helper function to save regtest output to a file
def save_output_to_file(regtest, file_name):
    with open(file_name, 'a') as file:  # Use 'a' for append mode
        file.write(f"\n\n{regtest.out}")





# Test 5 in the other test file
def test_regression_search_and_buy_product_search_specific_product(regtest):
    test_search_and_buy_product_search_specific_product(regtest)
    save_output_to_file(regtest, 'output_regression.txt')

# Test 6 in the other test file
def test_regression_search_and_buy_product_logout(regtest):
    test_search_and_buy_product_logout(regtest)
    save_output_to_file(regtest, 'output_regression.txt')

# Test 7 in the other test file
def test_regression_search_and_buy_product_empty_checkout(regtest):
    test_search_and_buy_product_empty_checkout(regtest)
    save_output_to_file(regtest, 'output_regression.txt')

# Test 8 in the other test file
def test_regression_search_and_buy_product_correct_item(regtest):
    test_search_and_buy_product_correct_item(regtest)
    save_output_to_file(regtest, 'output_regression.txt')

# Test 9 in the other test file
def test_regression_search_and_buy_product_successful_checkout(regtest):
    test_search_and_buy_product_successful_checkout(regtest)
    save_output_to_file(regtest, 'output_regression.txt')

# # Test 10 in the other test file
# def test_regression_search_and_buy_product_insufficient_balance(regtest):
#     test_search_and_buy_product_insufficient_balance(regtest)
#     save_output_to_file(regtest, 'output_regression.txt')

# # Repeat the same pattern for other test functions...
