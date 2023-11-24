import pytest
from products import display_csv_as_table
import shutil
import os
from io import StringIO
import sys
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


#Test 6: no argument passed to function
def test_display_csv_as_table_no_arg(copy_csv_file, capsys):
    with pytest.raises(TypeError):
        display_csv_as_table()


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

