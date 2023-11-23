import pytest
from products import display_filtered_table
import shutil
import os
from io import StringIO
import sys
import csv
import random


@pytest.fixture
def copy_csv_file():
    #copy the CSV file
    shutil.copy('products.csv', 'copy_products.csv')
    yield
    #remove the copied CSV file
    os.remove('copy_products.csv')
    if os.path.isfile('tmp_copy_products.csv'):
        os.remove('tmp_copy_products.csv')


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




    