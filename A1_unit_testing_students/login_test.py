from login import *
import pytest
from unittest.mock import patch

def reset_json():
    with open('users.json', "r+") as test_file:
        json_test = json.load(test_file)
        with open('users_original.json', "r") as orig_file:
            json_orig = json.load(orig_file)
            json_test = json_orig
        test_file.seek(0)
        json.dump(json_test, test_file, indent=10)
        test_file.truncate()

def get_json(filename):
    with open(filename, "r") as users:
        return json.load(users)

def test_convo_route1(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["N", "N", "N"]):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Have a nice day!\n"
    assert json_file == get_json("users_original.json")

def test_convo_route2(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["Phoenix", "wrong"]):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Either username or password were incorrect\n"
    assert json_file == get_json("users_original.json")

def test_convo_route3(capsys):
    json_file = get_json("users.json")
    with patch('builtins.input', side_effect=["Phoenix", "Firebir&^d987"]):
        assert login() == {"username": "Phoenix", "wallet": 120 }
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Successfully logged in\n"
    assert json_file == get_json("users_original.json")

def test_convo_route4():
    route_strings = ["Fox", "fake", "Y", "T#st", "Testing#"]
    with patch('builtins.input', side_effect=route_strings):
        assert login() == None
    json_file = get_json("users.json")
    assert json_file != get_json("users_original.json")
    assert json_file[-1]["username"] == "Fox"
    assert json_file[-1]["password"] == "Testing#"
    assert json_file[-1]["wallet"] == 0
    reset_json()

def test_convo_route5(capsys):
    json_file = get_json("users.json")
    route_strings = ["Fox", "fake", "OASd", "N",]
    with patch('builtins.input', side_effect=route_strings):
        assert login() == None
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Answer in wrong format, try again\nHave a nice day!\n"
    assert json_file == get_json("users_original.json")

def test_pass_length():
    assert pass_check("") == False
    assert pass_check("GGGHJ#") == False

def test_pass_symbol():
    assert pass_check("kajsnDkdjWankjDdn") == False
    assert pass_check("GGGHJasdadadad") == False

def test_pass_upper():
    assert pass_check("") == False
    assert pass_check("GGGHJ#") == False

def test_pass_correct():
    assert pass_check("LowRoar12<3") == True
    assert pass_check("HEALTHofficial#") == True
    assert pass_check("%AmericanNonjaWarrior%") == True
    assert pass_check("Wooooohaaaaa#") == True

def test_pass_arg():
    with pytest.raises(TypeError) as e:
        pass_check(1)
    with pytest.raises(TypeError) as e:
        pass_check(0.1)
    with pytest.raises(TypeError) as e:
        pass_check(["pass"])