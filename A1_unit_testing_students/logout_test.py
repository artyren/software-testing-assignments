from logout import *
import pytest
from unittest.mock import patch
from checkout_and_payment import Product, ShoppingCart

#Cart needs to be tested so correct message is sent if it isnt true
    #All types
#Needs to check that correct event happens when empty
#Needs to check that correct products get printed

#Product(namn, pris, enheter)
#Shoppingcart(Lista av produkter)

def test_cart_empty():
    cart = ShoppingCart()
    assert logout(cart) == True

def test_cart_string_input():
    with pytest.raises(Exception) as e:
        logout("cart")

def test_cart_int_input():
    with pytest.raises(Exception) as e:
        logout(1)
def test_cart_float_input():
    with pytest.raises(Exception) as e:
        logout(0.1)
def test_cart_list_input():
    with pytest.raises(Exception) as e:
        logout([ShoppingCart()])

def test_cart_wrong_input():
    with pytest.raises(Exception) as e:
        logout((ShoppingCart(), ShoppingCart()))

def test_product_prints_and_exit(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Eggs", 15, 4))
    cart.add_item(Product("Chips", 30, 1))
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Eggs', 15.0, 4]\n['Chips', 30.0, 1]\n"

def test_product_prints_and_stay(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Bike", 1500, 1))
    with patch('builtins.input', return_value="N"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Bike', 1500.0, 1]\n"

def test_product_prints_and_stay(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    cart.add_item(Product("Bike", 1500, 1))
    with patch('builtins.input', return_value="N"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n['Bike', 1500.0, 1]\n"

def test_product_prints_and_wrong_input(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    with patch('builtins.input', return_value="kjasdlfjbalsd"):
        assert logout(cart) == False
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n"

def test_cart_clear(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n"
    assert cart.items == []

def test_cart_clear(capsys):
    cart = ShoppingCart()
    cart.add_item(Product("Milk", 10, 2))
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True
    captured = capsys.readouterr()
    assert captured.out == "Your cart is not empty.You have following items\n['Milk', 10.0, 2]\n"
    assert cart.items == []
