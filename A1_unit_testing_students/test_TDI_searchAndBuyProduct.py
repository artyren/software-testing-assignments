from login import login
from products import searchAndBuyProduct
from users_manager import rollback_json

from unittest.mock import patch


# Stub for displaying all products
def display_csv_as_table(csv_filename):
    # pass
    print('''['Product', 'Price', 'Units']
             ['Apple', '2', '10']
             ['Banana', '1', '15']
             ['Orange', '1.5', '8']''')


# Stub for displaying filtered products
def display_filtered_table(csv_filename, search):
    # print version:
    header = ['Product', 'Price', 'Units']
    product_data = {
        'apple': ['Apple', '2', '10'],
        'banana': ['Banana', '1', '15'],
        'orange': ['Orange', '1.5', '8']
    }

    print(header)

    search_lower = search.lower()
    if search_lower in product_data:
        print(product_data[search_lower])
    else: pass


# Stub for checkoutAndPayment (ignore since it's continuation of execution and last thing + not login)
def checkoutAndPayment(login_info):
    pass

# ----------- MAIN DRIVER -----------


mockUser = 'Oliver'
mockPass = 'Oliver*123'
mockWallet = '60'

'''
Paths to cover (simplified CFG):
1. login 
    a. success -> go to 2
    b. fail pass -> retry login (go back to 1)
    c. fail user -> create new user
        Y. if Y, creates new username
            - use good password -> go back to 1
            - use insufficient password -> repeat
        N. if N, skip (go back to 1)
2. search + choose Y/N to go to shop
    a. all items
        Y. if Y, checkout - test ends
        N. if N, go back to 2
    b. filtered items (valid or invalid items are indifferent)
        Y. if Y, checkout - test ends
        N. if N, go back to 2
   
   
For fail loops we can do n=10 
'''

# Test 1: login success (1a) + search all (2a) + confirm (Y)
def test_1():
    with patch('builtins.input', side_effect=[mockUser, mockPass, 'all', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        #mock_login.assert_called_once()     # successful login = only called exactly once
        mock_all_prod.assert_called_once_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()


# Test 2: login pass fail once (1b) + search all (2a) + deny once (N)
def test_2():
    with patch('builtins.input', side_effect=['Oliver', 'foo', mockUser, mockPass, 'all', 'n', 'all', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        #assert mock_login.call_count == 2
        assert mock_all_prod.call_count == 2
        mock_all_prod.assert_called_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()


# Test 3: login pass fail 10 times (1b) + search all (2a) + deny 10 times (N)
def test_3():
    with patch('builtins.input', side_effect=['Oliver', 'foo'] * 10 + [mockUser, mockPass]
                                                   + ['all', 'n'] * 10 + ['all', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        #assert mock_login.call_count == 11
        assert mock_all_prod.call_count == 11
        mock_all_prod.assert_called_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()


# Test 4: search filtered (2b) + confirm (Y)
def test_4():
    with patch('builtins.input', side_effect=[mockUser, mockPass, 'apple', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        mock_all_prod.assert_not_called()
        mock_filtered_prod.assert_called_once_with("products.csv", "apple")
        mock_checkout.assert_called()


# Test 5: search filtered (2b) + deny once (N)
def test_5():
    with patch('builtins.input', side_effect=[mockUser, mockPass, 'apple', 'n', 'banana', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        mock_all_prod.assert_not_called()
        #mock_filtered_prod.assert_called_with("products.csv", "apple")
        mock_filtered_prod.assert_called_with("products.csv", "banana")
        assert mock_filtered_prod.call_count == 2
        mock_checkout.assert_called()


# Test 6: search filtered (2b) + deny 10 times (N)
def test_6():
    with patch('builtins.input', side_effect=[mockUser, mockPass] + ['apple', 'n'] * 10 + ['banana', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        mock_all_prod.assert_not_called()
        #mock_filtered_prod.assert_called_with("products.csv", "apple")
        mock_filtered_prod.assert_called_with("products.csv", "banana")
        assert mock_filtered_prod.call_count == 11
        mock_checkout.assert_called()


# Test 7: alternate between searches
def test_7():
    with patch('builtins.input', side_effect=[mockUser, mockPass, 'banana', 'n', 'all', 'y']), \
            patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
            patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
            patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:
        # Run test
        searchAndBuyProduct()

        # Verify calls
        mock_all_prod.assert_called_once_with("products.csv")
        mock_filtered_prod.assert_called_once_with("products.csv", "banana")
        mock_checkout.assert_called()


# At this point the new user registration was discovered, so the tests below cover that part of login
# To simplify on already tested stubs, default: all items and go to shop (Y)

newUser = 'User12345'
goodPass = '8A$88888'
badPass = 'incorrect'

# Test 8: login new user (1c) + confirm + use good password
def test_8():
    with patch('builtins.input', side_effect=[newUser, 'foo', 'y', goodPass,
                                                    newUser, goodPass, 'all', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        #assert mock_login.call_count == 2
        mock_all_prod.assert_called_once_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()

        rollback_json()


# Test 9: login new user (1c) + confirm (Y) + use insufficient password
def test_9():
    with patch('builtins.input', side_effect=[newUser, 'foo', 'y', badPass, goodPass,
                                                    newUser, goodPass, 'all', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        #assert mock_login.call_count == 2
        mock_all_prod.assert_called_once_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()

        rollback_json()


# Test 10: login new user (1c) + confirm (Y) + use insufficient password 10 times
def test_10():
    with patch('builtins.input', side_effect=[newUser, 'foo', 'y'] + [badPass] * 10 + [goodPass,
                                                    newUser, goodPass, 'all', 'y']), \
            patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
            patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
            patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:
        # Run test
        searchAndBuyProduct()

        # Verify calls
        # assert mock_login.call_count == 2
        mock_all_prod.assert_called_once_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()

        rollback_json()


# Test 11: login new user (1c) + deny (N) + success login
def test_11():
    with patch('builtins.input', side_effect=[newUser, 'foo', 'n',
                                                    mockUser, mockPass, 'all', 'y']), \
         patch('products.display_csv_as_table', wraps=display_csv_as_table) as mock_all_prod, \
         patch('products.display_filtered_table', wraps=display_filtered_table) as mock_filtered_prod, \
         patch('products.checkoutAndPayment', wraps=checkoutAndPayment) as mock_checkout:

        # Run test
        searchAndBuyProduct()

        # Verify calls
        #assert mock_login.call_count == 2
        mock_all_prod.assert_called_once_with("products.csv")
        mock_filtered_prod.assert_not_called()
        mock_checkout.assert_called()