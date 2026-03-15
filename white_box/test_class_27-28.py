# -*- coding: utf-8 -*-

"""
White-box unit testing examples.
"""
import unittest
from unittest.mock import patch

from class_exercises import BankAccount, BankingSystem, Product, ShoppingCart

from book_store import Book, BookStore


class TestBankAccount(unittest.TestCase):
    # 27---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.BankAccount = BankAccount(10, 10)
        self.assertEqual(self.BankAccount.account_number, 10)
        self.assertEqual(self.BankAccount.balance, 10)

    @patch("builtins.print")
    def test_view_account(self, mock_print):
        """
        Check view account function
        """
        self.BankAccount.view_account()
        # Revisando el mensaje exactamente
        mock_print.assert_called_once_with(
            f"The account {self.BankAccount.account_number} has a balance of {self.BankAccount.balance}"
        )
        """
        Forma alternativa, revisando que contenga los valores que imprime el print
        mensaje = mock_print.call_args.args[0]
        self.assertIn(str(self.BankAccount.account_number), mensaje)
        self.assertIn(str(self.BankAccount.balance), mensaje)
        """


class TestBankSystem(unittest.TestCase):
    # 27---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.BankSystem = BankingSystem()
        self.assertEqual(self.BankSystem.users, {"user123": "pass123"})
        self.assertEqual(self.BankSystem.logged_in_users, set())

    @patch("builtins.print")
    def test_authenticate_first_time(self, mock_print):
        """
        Check authentication
        """
        user = "user123"
        contra = "pass123"
        s = set()
        s.add(user)
        self.assertEqual(self.BankSystem.authenticate(user, contra), True)
        mock_print.assert_called_once_with(f"User {user} authenticated successfully.")
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_authenticate_second_time(self, mock_print):
        """
        Check authentication
        """
        user = "user123"
        contra = "pass123"
        s = set()
        s.add(user)
        self.BankSystem.authenticate(user, contra)
        self.assertEqual(self.BankSystem.authenticate(user, contra), False)
        mock_print.assert_called_with("User already logged in.")
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_authenticate_with_wrong_user(self, mock_print):
        """
        Check authentication
        """
        user = "user124"
        contra = "pass123"
        s = set()
        self.assertEqual(self.BankSystem.authenticate(user, contra), False)
        mock_print.assert_called_once_with("Authentication failed.")
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_authenticate_with_wrong_password(self, mock_print):
        """
        Check authentication
        """
        user = "user123"
        contra = "pass124"
        s = set()
        self.assertEqual(self.BankSystem.authenticate(user, contra), False)
        mock_print.assert_called_once_with("Authentication failed.")
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_transfer_money_with_sender_not_authenticated(self, mock_print):
        """
        Check authentication
        """
        user = "user123"
        receiver = "user456"
        s = set()
        self.assertEqual(
            self.BankSystem.transfer_money(user, receiver, 1000, "regular"), False
        )
        mock_print.assert_called_once_with("Sender not authenticated.")
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_transfer_money_regular_transaction(self, mock_print):
        """
        Check authentication
        """
        sender = "user123"
        contra = "pass123"
        s = set()
        s.add(sender)
        self.BankSystem.authenticate(sender, contra)
        receiver = "user456"
        amount = 1
        transaction_type = "regular"
        self.assertEqual(
            self.BankSystem.transfer_money(sender, receiver, amount, transaction_type),
            True,
        )
        mock_print.assert_called_with(
            f"Money transfer of ${amount} ({transaction_type} transfer)"
            + f" from {sender} to {receiver} processed successfully."
        )
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_transfer_money_express_transaction(self, mock_print):
        """
        Check authentication
        """
        sender = "user123"
        contra = "pass123"
        s = set()
        s.add(sender)
        self.BankSystem.authenticate(sender, contra)
        receiver = "user456"
        amount = 1
        transaction_type = "express"
        self.assertEqual(
            self.BankSystem.transfer_money(sender, receiver, amount, transaction_type),
            True,
        )
        mock_print.assert_called_with(
            f"Money transfer of ${amount} ({transaction_type} transfer)"
            + f" from {sender} to {receiver} processed successfully."
        )
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_transfer_money_scheduled_transaction(self, mock_print):
        """
        Check authentication
        """
        sender = "user123"
        contra = "pass123"
        s = set()
        s.add(sender)
        self.BankSystem.authenticate(sender, contra)
        receiver = "user456"
        amount = 1
        transaction_type = "scheduled"
        self.assertEqual(
            self.BankSystem.transfer_money(sender, receiver, amount, transaction_type),
            True,
        )
        mock_print.assert_called_with(
            f"Money transfer of ${amount} ({transaction_type} transfer)"
            + f" from {sender} to {receiver} processed successfully."
        )
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_transfer_money_with_wrong_transaction_type(self, mock_print):
        """
        Check authentication
        """
        sender = "user123"
        contra = "pass123"
        s = set()
        s.add(sender)
        self.BankSystem.authenticate(sender, contra)
        receiver = "user456"
        amount = 1
        transaction_type = "Error"
        self.assertEqual(
            self.BankSystem.transfer_money(sender, receiver, amount, transaction_type),
            False,
        )
        mock_print.assert_called_with("Invalid transaction type.")
        self.assertEqual(self.BankSystem.logged_in_users, s)

    @patch("builtins.print")
    def test_transfer_without_enough_founds(self, mock_print):
        """
        Check authentication
        """
        sender = "user123"
        contra = "pass123"
        s = set()
        s.add(sender)
        self.BankSystem.authenticate(sender, contra)
        receiver = "user456"
        amount = 1000
        transaction_type = "regular"
        self.assertEqual(
            self.BankSystem.transfer_money(sender, receiver, amount, transaction_type),
            False,
        )
        mock_print.assert_called_with("Insufficient funds.")
        self.assertEqual(self.BankSystem.logged_in_users, s)


class TestProduct(unittest.TestCase):
    # 28---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beginning of each test.
        """
        self.product = Product("Apple", 10)
        self.assertEqual(self.product.name, "Apple")
        self.assertEqual(self.product.price, 10)

    @patch("builtins.print")
    def test_view_product(self, mock_print):
        """
        Check view_product function
        """
        msg = self.product.view_product()
        expected_msg = (
            f"The product {self.product.name} has a price of {self.product.price}"
        )
        mock_print.assert_called_once_with(expected_msg)
        self.assertEqual(msg, expected_msg)


class TestShoppingCart(unittest.TestCase):
    # 28---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beginning of each test.
        """
        self.cart = ShoppingCart()
        self.product = Product("Apple", 10)
        self.assertEqual(self.cart.items, [])

    def test_add_product_first_time(self):
        """
        Check adding a new product
        """
        self.cart.add_product(self.product, 1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]["product"], self.product)
        self.assertEqual(self.cart.items[0]["quantity"], 1)

    def test_add_product_existing(self):
        """
        Check adding an existing product increases quantity
        """
        self.cart.add_product(self.product, 1)
        self.cart.add_product(self.product, 2)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]["quantity"], 3)

    def test_remove_product_partial(self):
        """
        Check removing part of the quantity
        """
        self.cart.add_product(self.product, 3)
        self.cart.remove_product(self.product, 1)
        self.assertEqual(self.cart.items[0]["quantity"], 2)

    def test_remove_product_all(self):
        """
        Check removing all product quantity
        """
        self.cart.add_product(self.product, 2)
        self.cart.remove_product(self.product, 2)
        self.assertEqual(self.cart.items, [])

    @patch("builtins.print")
    def test_view_cart(self, mock_print):
        """
        Check view_cart function
        """
        self.cart.add_product(self.product, 2)
        self.cart.view_cart()
        mock_print.assert_called_once_with(
            f"2 x {self.product.name} - ${self.product.price * 2}"
        )

    @patch("builtins.print")
    def test_checkout(self, mock_print):
        """
        Check checkout function
        """
        self.cart.add_product(self.product, 2)
        self.cart.checkout()
        total = self.product.price * 2
        mock_print.assert_any_call(f"Total: ${total}")
        mock_print.assert_any_call("Checkout completed. Thank you for shopping!")

    def test_remove_product_not_in_cart(self):
        """
        Removing a product that does not exist
        """
        self.cart.remove_product(self.product, 1)
        self.assertEqual(self.cart.items, [])


class TestBook(unittest.TestCase):
    # 29---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beginning of each function.
        """
        self.book = Book("Clean Code", "Robert Martin", 50.0, 10)
        self.assertEqual(self.book.title, "Clean Code")
        self.assertEqual(self.book.author, "Robert Martin")
        self.assertEqual(self.book.price, 50.0)
        self.assertEqual(self.book.quantity, 10)

    @patch("builtins.print")
    def test_display(self, mock_print):
        """
        Check display function
        """
        self.book.display()

        mock_print.assert_any_call(f"Title: {self.book.title}")
        mock_print.assert_any_call(f"Author: {self.book.author}")
        mock_print.assert_any_call(f"Price: ${self.book.price}")
        mock_print.assert_any_call(f"Quantity: {self.book.quantity}")


class TestBookStore(unittest.TestCase):
    # 29---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beginning of each function.
        """
        self.store = BookStore()
        self.book = Book("Clean Code", "Robert Martin", 50.0, 10)

        self.assertEqual(self.store.books, [])

    @patch("builtins.print")
    def test_add_book(self, mock_print):
        """
        Check add_book function
        """
        self.store.add_book(self.book)

        self.assertEqual(len(self.store.books), 1)
        self.assertEqual(self.store.books[0], self.book)

        mock_print.assert_called_once_with(
            f"Book '{self.book.title}' added to the store."
        )

    @patch("builtins.print")
    def test_display_books_empty(self, mock_print):
        """
        Check display_books when store is empty
        """
        self.store.display_books()

        mock_print.assert_called_once_with("No books in the store.")

    @patch("builtins.print")
    def test_display_books_with_books(self, mock_print):
        """
        Check display_books when store has books
        """
        self.store.add_book(self.book)

        with patch.object(Book, "display") as mock_display:
            self.store.display_books()

            mock_print.assert_any_call("Books available in the store:")
            mock_display.assert_called_once()

    @patch("builtins.print")
    def test_search_book_not_found(self, mock_print):
        """
        Check search_book when book is not found
        """
        self.store.search_book("Python")

        mock_print.assert_called_once_with("No book found with title 'Python'.")

    @patch("builtins.print")
    def test_search_book_found(self, mock_print):
        """
        Check search_book when book exists
        """
        self.store.add_book(self.book)

        with patch.object(Book, "display") as mock_display:
            self.store.search_book("Clean Code")

            mock_print.assert_any_call("Found 1 book(s) with title 'Clean Code':")
            mock_display.assert_called_once()

    @patch("builtins.print")
    def test_search_book_case_insensitive(self, mock_print):
        """
        Check search_book ignoring case
        """
        self.store.add_book(self.book)

        with patch.object(Book, "display") as mock_display:
            self.store.search_book("clean code")

            mock_print.assert_any_call("Found 1 book(s) with title 'clean code':")
            mock_display.assert_called_once()


def test_search_multiple_books(self):
    """
    Search when multiple books match the title
    """
    b1 = Book("Clean Code", "Robert Martin", 50, 5)
    b2 = Book("Clean Code", "Someone Else", 40, 3)

    self.store.add_book(b1)
    self.store.add_book(b2)

    with patch("builtins.print") as mock_print:
        with patch.object(Book, "display") as mock_display:
            self.store.search_book("Clean Code")

            mock_print.assert_any_call("Found 2 book(s) with title 'Clean Code':")
            self.assertEqual(mock_display.call_count, 2)
