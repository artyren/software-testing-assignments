import sys
import csv
from checkout_and_payment import *
import pytest
from io import StringIO


def test_load_products_from_empty_file(tmp_path):
    # Create an empty CSV file for testing
    csv_file_path = tmp_path / "empty_test_products.csv"
    open(csv_file_path, 'w').close()

    # Test the function with an empty CSV file
    products = load_products_from_csv(csv_file_path)

    # Check if the list of products is empty
    assert not products

