from checkout_and_payment import *
from users_manager import *
import pytest, os
from unittest.mock import patch


# Simplified version of original checkoutAndPayment() for Bottom-Up Integration
def bui_checkoutAndPayment(login_info):
    # Create/retrieve a user using login information
    user = User(login_info["username"], login_info["wallet"])

    print("User:" + user.name + ", " + str(user.wallet)) # for assertion

    # Product list would originally get displayed here

    while True:
        # Grab input for product selection in numbers
        choice = input()

        if choice == 'c':
            # Check the cart and proceed to checkout if requested
            check = check_cart(user, cart)

            print("Check:" + str(check)) # for assertion

            if check is False:
                continue

        elif choice == 'l':
            # Logout the user
            ask_logout = logout(cart)

            print("Logout:" + str(ask_logout)) # for assertion

            if ask_logout is True:
                # Update wallet info in users file
                update_wallet(user)
                #print("You have been logged out")

                # we can check with file data
                break

            else:
                continue

        elif choice.isdigit() and 1 <= int(choice) <= len(products):
            # Add the selected product to the cart
            selected_product = products[int(choice) - 1]
            if selected_product.units > 0:
                cart.add_item(selected_product)
                print(f"{selected_product.name} added to your cart.")

            else:
                print(f"Sorry, {selected_product.name} is out of stock.")
        else:
            print("\nInvalid input. Please try again.")


# ----------- MAIN DRIVER -----------

login_info = {"username": "Oliver", "wallet": 60}
products = load_products_from_csv("products.csv")
cart = ShoppingCart()

# To check for the returns of functions and how they interact, we can print their results
# and assert how they should interact, since we can't check for their calls as they are
# not mocked as stubs unlike Top-Down Interaction.


# Test 1: Successful one item checkout
def test_1(capsys):
    with patch('builtins.input', side_effect=["1", "c", "y", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()

    assert "User:" + login_info["username"] + ", " + str(login_info["wallet"]) in captured.out
    assert "Check:" + str(None) in captured.out
    assert "Logout:" + str(True) in captured.out
    assert "Apple added to your cart." in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 58.0" in captured.out

    # Checking that update function has changed file
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 58
    rollback_json()


# Test 2: Invalid product selection
def test_2(capsys):
    with patch('builtins.input', side_effect=["0", "l"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    # since User always has same login_info, checking for assertion here is now redundant
    assert "Check:" not in captured.out #we don't checkout
    assert "Logout:" + str(True) in captured.out
    assert "Invalid input. Please try again." in captured.out
    assert "added to your cart" not in captured.out

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 3: Failed checkout due to empty cart
def test_3(capsys):
    with patch('builtins.input', side_effect=["c", "y", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Check:" + str(None) in captured.out
    assert "Logout:" + str(True) in captured.out
    assert "added to your cart" not in captured.out
    assert "Your basket is empty. Please add items before checking out." in captured.out # from check_cart()

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 4: Deny checkout
def test_4(capsys):
    with patch('builtins.input', side_effect=["1", "c", "n", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Check:" + str(False) in captured.out # denying checkout makes False
    assert "Logout:" + str(True) in captured.out
    assert "Apple added to your cart" in captured.out
    assert "Your cart is not empty.You have following items" in captured.out # from check_cart()

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 5: Logout with leftovers in cart
def test_5(capsys):
    with patch('builtins.input', side_effect=["1", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Check:" not in captured.out
    assert "Logout:" + str(True) in captured.out
    assert "Apple added to your cart" in captured.out
    assert "Your cart is not empty.You have following items" in captured.out

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 6: Failed checkout due to insufficient funds in user's wallet
def test_6(capsys):
    # Test item: #52. Laptop = 800$
    with patch('builtins.input', side_effect=["52", "c", "y", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Laptop added to your cart." in captured.out
    assert "Check:" + str(None) in captured.out
    assert "You don't have enough money to complete the purchase.\nPlease try again!" in captured.out
    assert "Logout:" + str(True) in captured.out

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 7: Cancel logout due to a forgotten checkout
def test_7(capsys):
    with patch('builtins.input', side_effect=["1", "l", "n", "c", "y", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart." in captured.out
    assert "Logout:" + str(False) in captured.out # cancel logout
    assert "Check:" + str(None) in captured.out

    assert "Your cart is not empty.You have following items" in captured.out
    assert "Thank you for your purchase, Oliver! Your remaining balance is 58.0" in captured.out
    assert "Logout:" + str(True) in captured.out # confirm logout later

    # Checking that update function has changed file
    data = get_json("users.json")
    assert data != get_json("users_backup.json")
    for entry in data:
        if entry["username"] == "Oliver":
            assert entry["wallet"] == 58
    rollback_json()


# Test 8: Deny logout and no checkout
def test_8(capsys):
    with patch('builtins.input', side_effect=["1", "l", "n", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart." in captured.out
    assert "Logout:" + str(False) in captured.out # cancel logout
    assert "Logout:" + str(True) in captured.out # confirm logout later
    assert "Check:" not in captured.out

    assert captured.out.count("Your cart is not empty.You have following items") == 2

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 9: just logout
def test_9(capsys):
    with patch('builtins.input', side_effect=["l"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "added to your cart" not in captured.out
    assert "Check:" not in captured.out
    assert "Logout:" + str(True) in captured.out

    # Checking that update function has not changed file
    data = get_json("users.json")
    assert data == get_json("users_backup.json")


# Test 10: Invalid yes/no confirm
# In the case of this software, the devs decided that anything other than "Y" is No, so it doesn't
# matter if you write "N"
def test_10(capsys):
    with patch('builtins.input', side_effect=["1", "l", "i", "l", "y"]):
        bui_checkoutAndPayment(login_info)

    captured = capsys.readouterr()
    assert "Apple added to your cart."
    assert "Check:" not in captured.out
    assert "Logout:" + str(False) in captured.out # invalid translates to No
    assert "Logout:" + str(True) in captured.out #confirm logout later
    assert captured.out.count("Your cart is not empty.You have following items") == 2
    data = get_json("users.json")
    assert data == get_json("users_backup.json")