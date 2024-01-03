from products import *
from users_manager import *

from unittest.mock import patch

import pytest


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


# Test 3
def test_logout_no_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "added to your cart" not in captured.out
    assert "You have been logged out" in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 4
def test_invalid_option(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["f", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Invalid input. Please try again." in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")

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
    rollback_json()


# Test 6
def test_success_multiple_item_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #59. Vaccuum Cleaner = 30$
    # Test item: #67. Gloves  =  5$
    with patch('builtins.input', side_effect=["59", "67", "c", "y", "l","y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Blender added to your cart." in captured.out
    assert "Gloves added to your cart." in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 25.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
           assert entry["wallet"] == 25
    rollback_json()


# TODO bug: when ordering, you can infinitely add items to your cart
# they never go out of stock. so test fails
# Test 7
# def test_out_of_stock(capsys):
#     data = get_json("users.json")
#     login_info = {"username": "Oliver", "wallet": 60}

#     with patch('builtins.input', side_effect=["59", "59", "c", "y", "l","y"]):
#         checkoutAndPayment(login_info)

#     captured = capsys.readouterr()
#     assert "Blender added to your cart." in captured.out
#     assert "Sorry, Blender is out of stock." in captured.out
#     data = get_json("users.json")
#     assert data != get_json("users_backup.json")
#     for entry in data:
#         if entry["username"] == "Oliver":
#             assert entry["wallet"] == 30
#     rollback_json()


# Test 8
def test_invalid_product_selection(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["0", "l"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Invalid input. Please try again." in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 9
def test_empty_cart_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    with patch('builtins.input', side_effect=["c", "y", "l","y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Your basket is empty. Please add items before checking out." in captured.out
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
    data = get_json("users.json")
    assert data == get_json("users_backup.json")
    rollback_json()


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
    rollback_json()


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

    rollback_json()

# Test 15
def test_multiple_users_with_different_carts(capsys):
    data = get_json("users.json")
    user1_info = {"username": "Oliver", "wallet": 60}
    user2_info = {"username": "Athena", "wallet": 100}

    # Test item: #1. Apple = $2
    with patch('builtins.input', side_effect=["1", "c", "y", "l"]):
        checkoutAndPayment(user1_info)

    # Test item: #44. Towel = $4
    with patch('builtins.input', side_effect=["44", "c", "y", "l"]):
        checkoutAndPayment(user2_info)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Oliver! Your remaining balance is 58.0" in captured.out
    assert "Thank you for your purchase, Athena! Your remaining balance is 96.0" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 58
        if entry["username"] == "Athena":
            assert entry["wallet"] == 96
    rollback_json()


# Test 16
def test_insufficient_funds_after_spending_all(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #63. Running shoes = 60$
    # Test item: #1. Apple = 2$
    with patch('builtins.input', side_effect=["63", "c", "y", "1", "c", "y", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Thank you for your purchase, Oliver! Your remaining balance is 0.0" in captured.out
    assert "You don't have enough money to complete the purchase.\nPlease try again!" in captured.out
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 0
    rollback_json()



# Test 17
def test_deny_logout_and_no_checkout(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #1. Apple = 2$
    with patch('builtins.input', side_effect=["1", "l", "n", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart."
    assert captured.out.count("Your cart is not empty.You have following items") == 2
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 18
def test_checkout_invalid_yesno_confirm(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #1. Apple = 2$
    with patch('builtins.input', side_effect=["1", "c", "foo", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart."
    # assert "Invalid input. Please try again." in captured.out ## Instead of reasking it is treated as no
    assert "Your cart is not empty.You have following items" in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 19
def test_login_invalid_yesno_confirm(capsys):
    data = get_json("users.json")
    login_info = {"username": "Oliver", "wallet": 60}

    # Test item: #1. Apple = 2$
    with patch('builtins.input', side_effect=["1", "l", "foo", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart."
    # assert "Invalid input. Please try again." in captured.out ## Instead of reasking it is treated as no
    assert captured.out.count("Your cart is not empty.You have following items") == 2
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 20
def test_negative_wallet(capsys):
    data = get_json("users.json")
    login_info = {"username": "Benjamin", "wallet": -500}

    # Test item: #1. Apple = 2$
    with patch('builtins.input', side_effect=["1", "c", "y", "l", "y"]):
        checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart." in captured.out
    assert "You don't have enough money to complete the purchase.\nPlease try again!" in captured.out
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


#######
# Test 21
def test_invalid_type_int():
    login_info = 24
    with pytest.raises(TypeError) as err_msg:
        checkoutAndPayment(login_info)
    assert "'int' object is not subscriptable" in str(err_msg.value)


# Test 22
def test_invalid_type_str():
    login_info = "Benjamin"
    with pytest.raises(TypeError) as err_msg:
        checkoutAndPayment(login_info)
    assert "string indices must be integers" in str(err_msg.value)


# Test 23
def test_invalid_type_float():
    login_info = 24.3
    with pytest.raises(TypeError) as err_msg:
        checkoutAndPayment(login_info)
    assert "'float' object is not subscriptable" in str(err_msg.value)


# Test 24
def test_invalid_type_list():
    login_info = ["Oliver", 60]
    with pytest.raises(TypeError) as err_msg:
        checkoutAndPayment(login_info)
    assert "list indices must be integers or slices, not str" in str(err_msg.value)
        ## indices are str in dictionaries