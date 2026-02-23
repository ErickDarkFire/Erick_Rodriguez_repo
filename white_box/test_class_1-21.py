# -*- coding: utf-8 -*-

"""
White-box unit testing examples.
"""
import unittest

"""
Notes:

python -m unittest discover

from white_box.class_exercises import divide

import divide

import class_exercises.divide

The unittest module can be used from the command line to run tests from modules, classes or even individual test methods:

python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method
You can pass in a list with any combination of module names, and fully qualified class or method names.


Test modules can be specified by file path as well:

python -m unittest tests/test_something.py

python -m unittest discover -s project_directory -p "*_test.py"
python -m unittest discover project_directory "*_test.py"

"""

from class_exercises import (
    check_number_status,
    validate_password,
    calculate_total_discount,
    calculate_order_total,
    calculate_items_shipping_cost,
    validate_login,
)
from class_exercises import (
    verify_age,
    categorize_product,
    validate_email,
    celsius_to_fahrenheit,
    validate_credit_card,
    validate_date,
    check_flight_eligibility,
    validate_url,
)

# from class_exercises import calculate_quantity_discount, check_file_size, check_loan_eligibility, calculate_shipping_cost, grade_quiz, authenticate_user, get_weather_advisory

"""
White-box unittest class.
"""


class TestCheckNumberStatus(unittest.TestCase):
    # 1---------------------------------------------------------------
    def test_check_number_status_with_zero(self):
        """
        Checks if a number is zero.
        """
        self.assertEqual(check_number_status(0), "Zero")

    def test_check_number_status_with_positive_number(self):
        """
        Checks if a number is positive.
        """
        self.assertEqual(check_number_status(1), "Positive")

    def test_check_number_status_with_negative_number(self):
        """
        Checks if a number is negative.
        """
        self.assertEqual(check_number_status(-1), "Negative")


class TestValidatePassword(unittest.TestCase):
    # 2---------------------------------------------------------------
    def test_validate_password(self):
        """
        Checks if a password is valid
        """
        self.assertTrue(validate_password("Erick1019!"))

    def test_validate_password_with_length_less_than_8(self):
        """
        Checks if a password is long enough.
        """
        self.assertFalse(validate_password("erick123"))

    def test_validate_password_without_uppercase(self):
        """
        Checks if a password have at less a uppercase char.
        """
        self.assertFalse(validate_password("erick19!"))

    def test_validate_password_without_lowercase(self):
        """
        Checks if a password have at less a lowercase char.
        """
        self.assertFalse(validate_password("ERICK19!"))

    def test_validate_password_without_digit(self):
        """
        Checks if a password have at less a digit.
        """
        self.assertFalse(validate_password("erickrod!"))

    def test_validate_password_without_special_char(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019"))

    def test_validate_password_with_special_character_1(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019!"))

    def test_validate_password_with_special_character_2(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019@"))

    def test_validate_password_with_special_character_3(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019#"))

    def test_validate_password_with_special_character_4(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019$"))

    def test_validate_password_with_special_character_5(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019%"))

    def test_validate_password_with_special_character_6(self):
        """
        Checks if a password have at less a special char.
        """
        self.assertFalse(validate_password("erick1019&"))


class TestCalculateTotalDiscount(unittest.TestCase):
    # 3---------------------------------------------------------------
    def test_calculate_total_discount_with_total_amount_less_than_100(self):
        """
        Calculates the discount for a customer's purchase based on the total amount.
        if the total amount is less than 100
        """
        self.assertEqual(calculate_total_discount(99), 0)

    def test_calculate_total_discount_with_total_amount_less_than_501(self):
        """
        Calculates the discount for a customer's purchase based on the total amount.
        if the total amount is less than 501
        """
        self.assertEqual(calculate_total_discount(500), 0.1 * 500)

    def test_calculate_total_discount_with_total_amount_more_than_500(self):
        """
        Calculates the discount for a customer's purchase based on the total amount.
        if the total amount is more than 500
        """
        self.assertEqual(calculate_total_discount(501), 0.2 * 501)


class TestCalculateOrderTotal(unittest.TestCase):
    # 4---------------------------------------------------------------
    def test_calculate_order_total_no1(self):
        """
        Calculate order total with 5 pieces of 1 different item
        """
        dic = [{"quantity": 5, "price": 10}]
        self.assertEqual(calculate_order_total(dic), 5 * 10)

    def test_calculate_order_total_no2(self):
        """
        Calculate order total with 10 pieces of 1 different item
        """
        dic = [{"quantity": 10, "price": 10}]
        self.assertEqual(calculate_order_total(dic), 0.95 * 10 * 10)

    def test_calculate_order_total_no3(self):
        """
        Calculate order total with more than 10 pieces of 1 different item
        """
        dic = [{"quantity": 11, "price": 10}]
        self.assertEqual(calculate_order_total(dic), 0.9 * 11 * 10)

    def test_calculate_order_total_no4(self):
        """
        Calculate order total with 5 pieces of 2 different items
        """
        dic = [{"quantity": 5, "price": 10}, {"quantity": 5, "price": 10}]
        self.assertEqual(calculate_order_total(dic), (5 * 10) + (5 * 10))

    def test_calculate_order_total_no5(self):
        """
        Calculate order total with 10 pieces of 2 different items
        """
        dic = [{"quantity": 10, "price": 10}, {"quantity": 10, "price": 10}]
        self.assertEqual(
            calculate_order_total(dic), (0.95 * 10 * 10) + (0.95 * 10 * 10)
        )

    def test_calculate_order_total_no6(self):
        """
        Calculate order total with more than 10 pieces of 2 different items
        """
        dic = [{"quantity": 11, "price": 10}, {"quantity": 12, "price": 10}]
        self.assertEqual(calculate_order_total(dic), (0.9 * 11 * 10) + (0.9 * 12 * 10))

    def test_calculate_order_total_no7(self):
        """
        Calculate order total with 5 pieces of 1 item and 10 pieces of 1 item
        """
        dic = [{"quantity": 5, "price": 10}, {"quantity": 10, "price": 10}]
        self.assertEqual(calculate_order_total(dic), (5 * 10) + (0.95 * 10 * 10))

    def test_calculate_order_total_no8(self):
        """
        Calculate order total with 10 pieces of 1 item and more than 10 pieces of 1 item
        """
        dic = [{"quantity": 10, "price": 10}, {"quantity": 11, "price": 10}]
        self.assertEqual(calculate_order_total(dic), (0.95 * 10 * 10) + (0.9 * 11 * 10))

    def test_calculate_order_total_no9(self):
        """
        Calculate order total with 5 pieces of 1 item and more than 10 pieces of 1 item
        """
        dic = [{"quantity": 5, "price": 10}, {"quantity": 11, "price": 10}]
        self.assertEqual(calculate_order_total(dic), (5 * 10) + (0.9 * 11 * 10))


class TestCalculateItemsShippingCost(unittest.TestCase):
    # 5---------------------------------------------------------------
    def test_calculate_items_shipping_cost_no1(self):
        """
        Calculate items shipping cost with standard method and 1 item with weight 5
        """
        order = [{"weight": 5}]
        sm = "standard"
        res = 10
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no2(self):
        """
        Calculate items shipping cost with standard method and 1 item with weight 10
        """
        order = [{"weight": 10}]
        sm = "standard"
        res = 15
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no3(self):
        """
        Calculate items shipping cost with standard method and 1 item with weight greater than 10
        """
        order = [{"weight": 11}]
        sm = "standard"
        res = 20
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no4(self):
        """
        Calculate items shipping cost with express method and 1 item with weight 5
        """
        order = [{"weight": 5}]
        sm = "express"
        res = 20
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no5(self):
        """
        Calculate items shipping cost with express method and 1 item with weight 10
        """
        order = [{"weight": 10}]
        sm = "express"
        res = 30
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no6(self):
        """
        Calculate items shipping cost with express method and 1 item with weight greater than 10
        """
        order = [{"weight": 11}]
        sm = "express"
        res = 40
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no7(self):
        """
        Calculate items shipping cost with another shipping method
        """
        order = [{"weight": 5}]
        sm = "hola"

        with self.assertRaises(ValueError):
            calculate_items_shipping_cost(order, sm)

    def test_calculate_items_shipping_cost_no8(self):
        """
        Calculate items shipping cost with standard method and multiple items that sums 5
        """
        order = [{"weight": 2}, {"weight": 3}]
        sm = "standard"
        res = 10
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no9(self):
        """
        Calculate items shipping cost with standard method and multiple items that sums 10
        """
        order = [{"weight": 5}, {"weight": 2}, {"weight": 3}]
        sm = "standard"
        res = 15
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no10(self):
        """
        Calculate items shipping cost with standard method and multiple items that sums more than 10
        """
        order = [{"weight": 5}, {"weight": 5}, {"weight": 3}]
        sm = "standard"
        res = 20
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no11(self):
        """
        Calculate items shipping cost with express method and multiple items that sums 5
        """
        order = [{"weight": 2}, {"weight": 3}]
        sm = "express"
        res = 20
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no12(self):
        """
        Calculate items shipping cost with express method and multiple items that sums 10
        """
        order = [{"weight": 5}, {"weight": 2}, {"weight": 3}]
        sm = "express"
        res = 30
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)

    def test_calculate_items_shipping_cost_no13(self):
        """
        Calculate items shipping cost with express method and multiple items that sums more than 10
        """
        order = [{"weight": 5}, {"weight": 5}, {"weight": 3}]
        sm = "express"
        res = 40
        self.assertEqual(calculate_items_shipping_cost(order, sm), res)


class TestValidateLogin(unittest.TestCase):
    # 6---------------------------------------------------------------
    def test_validate_login_with_max_length(self):
        """
        Validate user credentials with max length in username and password
        """
        username = "erickrodriguezgomez1"
        ps = "hay15caracteres"
        self.assertEqual(validate_login(username, ps), "Login Successful")

    def test_validate_login_with_min_length(self):
        """
        Validate user credentials with min length in username and password
        """
        username = "erick"
        ps = "characte"
        self.assertEqual(validate_login(username, ps), "Login Successful")

    def test_validate_login_without_enough_length_in_username(self):
        """
        Validate user credentials without enough length in username
        """
        username = "eric"
        ps = "characte"
        self.assertEqual(validate_login(username, ps), "Login Failed")

    def test_validate_login_without_enough_length_in_password(self):
        """
        Validate user credentials without enough length in password
        """
        username = "erick"
        ps = "charac"
        self.assertEqual(validate_login(username, ps), "Login Failed")


class TestVerifyAge(unittest.TestCase):
    # 7---------------------------------------------------------------
    def test_verify_age_eligible(self):
        """
        Validate an eligible age
        """
        self.assertEqual(verify_age(22), "Eligible")

    def test_verify_age_too_young(self):
        """
        Validate an lower limit
        """
        self.assertEqual(verify_age(17), "Not Eligible")

    def test_verify_age_too_old(self):
        """
        Validate an upper limit
        """
        self.assertEqual(verify_age(66), "Not Eligible")


class TestCategorizeProduct(unittest.TestCase):
    # 8---------------------------------------------------------------
    def test_categorize_product_with_price_less_than_10(self):
        """
        Determinate a product with price less than 10
        """
        self.assertEqual(categorize_product(9), "Category D")

    def test_categorize_product_with_price_less_than_51(self):
        """
        Determinate a product with price more than 10 and less than 51
        """
        self.assertEqual(categorize_product(50), "Category A")

    def test_categorize_product_with_price_less_than_101(self):
        """
        Determinate a product with price more than 50 and less than 101
        """
        self.assertEqual(categorize_product(100), "Category B")

    def test_categorize_product_with_price_less_than_201(self):
        """
        Determinate a product with price more than 100 and less than 201
        """
        self.assertEqual(categorize_product(200), "Category C")

    def test_categorize_product_with_price_greater_than_200(self):
        """
        Determinate a product with price more than 200
        """
        self.assertEqual(categorize_product(201), "Category D")


class TestValidateEmail(unittest.TestCase):
    # 9---------------------------------------------------------------
    def test_validate_email(self):
        """
        Validate a valid email
        """
        self.assertEqual(validate_email("erick@gmail.com"), "Valid Email")

    def test_validate_email_without_enough_length(self):
        """
        Validate a email without enough length
        """
        self.assertEqual(validate_email("e@e."), "Invalid Email")

    def test_validate_email_without_arroba(self):
        """
        Validate a email without arroba
        """
        self.assertEqual(validate_email("erickgmail.com"), "Invalid Email")

    def test_validate_email_without_dot(self):
        """
        Validate a email without dot
        """
        self.assertEqual(validate_email("erick@gmailcom"), "Invalid Email")


class TestCelsiusToFahrenheit(unittest.TestCase):
    # 10---------------------------------------------------------------
    def test_celsius_to_fahrenheit(self):
        """
        Try to convert a temperature lower than -100 celsius
        """
        self.assertEqual(celsius_to_fahrenheit(-101), "Invalid Temperature")

    def test_celsius_to_fahrenheit(self):
        """
        Try to convert a temperature between -100 and 100 (inclusive) celsius
        """
        self.assertEqual(celsius_to_fahrenheit(0), 32)

    def test_celsius_to_fahrenheit(self):
        """
        Try to convert a temperature greater than 100 celsius
        """
        self.assertEqual(celsius_to_fahrenheit(101), "Invalid Temperature")


class TestValidateCreditCard(unittest.TestCase):
    # 10---------------------------------------------------------------
    def test_validate_credit_card_without_enough_length(self):
        """
        Validate a credit card number without enough length
        """
        self.assertEqual(validate_credit_card("012345678901234"), "Valid Card")

    def test_validate_credit_card_without_enough_length(self):
        """
        Validate a credit card number without enough length
        """
        self.assertEqual(validate_credit_card("0123456789"), "Invalid Card")

    def test_validate_credit_card_with_more_length(self):
        """
        Validate a credit card number with more length
        """
        self.assertEqual(validate_credit_card("01234567890123456789"), "Invalid Card")

    def test_validate_credit_card_with_chars(self):
        """
        Validate a credit card number with a chars
        """
        self.assertEqual(validate_credit_card("abcdefghijklmno"), "Invalid Card")
