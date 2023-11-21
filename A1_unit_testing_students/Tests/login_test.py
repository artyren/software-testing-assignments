import ../login.py as login
import mock as m

def test_user_name():
    with mock.patch.object(__builtins__, 'input', lambda: 'some_input'):
        assert login.login() == 'expected_output'