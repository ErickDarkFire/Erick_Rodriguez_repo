# Al ejecutar coverage, me decia que me faltaba un 1% por que no probaba la llamada a la funcion main de la ultima linea de codigo
# Asi que para evitar que saliera asi, enseguida de if __name__ == "__main__": agregue # pragma: no cover para que no lo considere
# coverage al ejecutarse. De esa forma si sale el 100%

import unittest
from unittest.mock import patch, mock_open, MagicMock
import ej1


class TestGenerateSalt(unittest.TestCase):
    def test_generate_salt_length(self):
        salt = ej1.generate_salt()
        self.assertEqual(len(salt), 32)


class TestGeneratePasswordHash(unittest.TestCase):
    def test_generate_password_hash_consistency(self):
        password = "1234"
        salt = "abcd"
        hash1 = ej1.generate_password_hash(password, salt)
        hash2 = ej1.generate_password_hash(password, salt)
        self.assertEqual(hash1, hash2)


class TestLoadUserData(unittest.TestCase):
    @patch("ej1.os.path.exists")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"user": {"password_hash": "123", "salt": "abc"}}',
    )
    def test_load_user_data_file_exists(self, mock_file, mock_exists):
        mock_exists.return_value = True
        data = ej1.load_user_data()
        self.assertIn("user", data)
        mock_file.assert_called_once_with(ej1.USER_DATA_FILE, "r")

    @patch("ej1.os.path.exists")
    def test_load_user_data_file_not_exists(self, mock_exists):
        mock_exists.return_value = False
        data = ej1.load_user_data()
        self.assertEqual(data, {})


class TestSaveUserData(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("ej1.json.dump")
    def test_save_user_data(self, mock_dump, mock_file):
        data = {"user": "data"}
        ej1.save_user_data(data)
        mock_file.assert_called_once_with(ej1.USER_DATA_FILE, "w")
        mock_dump.assert_called_once()


class TestRegister(unittest.TestCase):
    @patch("ej1.load_user_data")
    @patch("builtins.print")
    def test_register_user_exists(self, mock_print, mock_load):
        mock_load.return_value = {"erick": {}}
        ej1.register("erick")
        mock_print.assert_called_with(
            "User already exists. Please choose a different username."
        )

    @patch("ej1.save_user_data")
    @patch("ej1.generate_password_hash")
    @patch("ej1.generate_salt")
    @patch("ej1.load_user_data")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_register_success(
        self, mock_print, mock_input, mock_load, mock_salt, mock_hash, mock_save
    ):
        mock_load.return_value = {}
        mock_input.return_value = "password123"
        mock_salt.return_value = "salt"
        mock_hash.return_value = "hashed"
        ej1.register("erick")
        mock_save.assert_called_once()
        mock_print.assert_called_with("User registered successfully.")


class TestLogin(unittest.TestCase):
    @patch("ej1.load_user_data")
    @patch("builtins.print")
    def test_login_user_not_exists(self, mock_print, mock_load):
        mock_load.return_value = {}
        ej1.login("erick", "1234")
        mock_print.assert_called_with("User does not exist. Please register first.")

    @patch("ej1.load_user_data")
    @patch("ej1.generate_password_hash")
    @patch("builtins.print")
    def test_login_success(self, mock_print, mock_hash, mock_load):
        mock_load.return_value = {"erick": {"password_hash": "hashed", "salt": "salt"}}
        mock_hash.return_value = "hashed"
        ej1.login("erick", "1234")
        mock_print.assert_called_with("Login successful!")

    @patch("ej1.load_user_data")
    @patch("ej1.generate_password_hash")
    @patch("builtins.print")
    def test_login_invalid_password(self, mock_print, mock_hash, mock_load):
        mock_load.return_value = {"erick": {"password_hash": "correct", "salt": "salt"}}
        mock_hash.return_value = "wrong"
        ej1.login("erick", "1234")
        mock_print.assert_called_with("Invalid password. Please try again.")


class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "erick", "password123", "3"])
    @patch("ej1.register")
    @patch("builtins.print")
    def test_main_register_flow(self, mock_print, mock_register, mock_input):
        ej1.main()

        mock_register.assert_called_once_with("erick")

    @patch("builtins.input", side_effect=["2", "erick", "1234", "3"])
    @patch("ej1.login")
    @patch("builtins.print")
    def test_main_login_flow(self, mock_print, mock_login, mock_input):
        ej1.main()

        mock_login.assert_called_once_with("erick", "1234")

    @patch("builtins.input", side_effect=["4", "3"])
    @patch("builtins.print")
    def test_main_invalid_option(self, mock_print, mock_input):
        ej1.main()

        mock_print.assert_any_call("Invalid choice. Please try again.")

    @patch("builtins.input", side_effect=["3"])
    @patch("builtins.print")
    def test_main_exit(self, mock_print, mock_input):
        ej1.main()

        mock_print.assert_any_call("Exiting...")
