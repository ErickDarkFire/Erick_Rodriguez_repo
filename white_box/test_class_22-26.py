# -*- coding: utf-8 -*-

"""
White-box unit testing examples.
"""
import unittest

from class_exercises import (
    VendingMachine,
    TrafficLight,
    UserAuthentication,
    DocumentEditingSystem,
    ElevatorSystem,
)

"""
White-box unittest class 22 to 26

Notes:
    # @classmethod
    # def setUpClass(cls):
    #    return

    def setUp(self):
        self.vending_machine = VendingMachine()
        self.assertEqual(self.vending_machine.state, "Ready")

    # def tearDown(self):
    #    return

    # @classmethod
    # def tearDownClass(cls):
    #    return
"""


class TestVendingMachine(unittest.TestCase):
    # 22---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.vending_machine = VendingMachine()
        self.assertEqual(self.vending_machine.state, "Ready")

    def test_init(self):
        """
        Checks init
        """
        self.assertEqual(self.vending_machine.state, "Ready")

    def test_insert_coin(self):
        """
        Checks insert coin
        """
        self.assertEqual(
            self.vending_machine.insert_coin(), "Coin Inserted. Select your drink."
        )
        self.assertEqual(self.vending_machine.state, "Dispensing")

    def test_insert_2_coins(self):
        """
        Checks insert 2 coins in a row
        """
        self.vending_machine.insert_coin()
        self.assertEqual(
            self.vending_machine.insert_coin(), "Invalid operation in current state."
        )
        self.assertEqual(self.vending_machine.state, "Dispensing")

    def test_select_drink(self):
        """
        Checks select drink
        """
        self.vending_machine.insert_coin()
        self.assertEqual(
            self.vending_machine.select_drink(), "Drink Dispensed. Thank you!"
        )
        self.assertEqual(self.vending_machine.state, "Ready")

    def test_select_drink_without_insert_coin(self):
        """
        Checks select drink while there is no coin inserted
        """
        self.assertEqual(
            self.vending_machine.select_drink(), "Invalid operation in current state."
        )
        self.assertEqual(self.vending_machine.state, "Ready")


class TestTrafficLight(unittest.TestCase):
    # 23---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.traffic_light = TrafficLight()
        self.assertEqual(self.traffic_light.state, "Red")

    def test_init(self):
        """
        Checks init function
        """
        self.assertEqual(self.traffic_light.state, "Red")

    def test_get_current_state_red(self):
        """
        Checks if the current state is red
        """
        self.assertEqual(
            self.traffic_light.get_current_state(), self.traffic_light.state
        )
        self.assertEqual(self.traffic_light.state, "Red")

    def test_get_current_state_green(self):
        """
        Checks if the current state is green
        """
        self.traffic_light.change_state()
        self.assertEqual(
            self.traffic_light.get_current_state(), self.traffic_light.state
        )
        self.assertEqual(self.traffic_light.state, "Green")

    def test_get_current_state_yellow(self):
        """
        Checks if the current state is yellow
        """
        self.traffic_light.change_state()
        self.traffic_light.change_state()
        self.assertEqual(
            self.traffic_light.get_current_state(), self.traffic_light.state
        )
        self.assertEqual(self.traffic_light.state, "Yellow")

    def test_change_state_to_red(self):
        """
        Checks the traffic light can change from red to red again
        """
        self.traffic_light.change_state()
        self.traffic_light.change_state()
        self.traffic_light.change_state()
        self.assertEqual(self.traffic_light.state, "Red")

    def test_change_state_to_yellow(self):
        """
        Checks the traffic light can change from red to yellow
        """
        self.traffic_light.change_state()
        self.traffic_light.change_state()
        self.assertEqual(self.traffic_light.state, "Yellow")

    def test_change_state_to_green(self):
        """
        Checks the traffic light can change from red to green
        """
        self.traffic_light.change_state()
        self.assertEqual(self.traffic_light.state, "Green")


class TestUserAuthentication(unittest.TestCase):
    # 24---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.user_authentication = UserAuthentication()
        self.assertEqual(self.user_authentication.state, "Logged Out")

    def test_init(self):
        """
        Checks init function
        """
        self.assertEqual(self.user_authentication.state, "Logged Out")

    def test_login(self):
        """
        Checks login
        """
        self.assertEqual(self.user_authentication.login(), "Login successful")
        self.assertEqual(self.user_authentication.state, "Logged In")

    def test_login_twice(self):
        """
        Checks login two times in a row
        """
        self.user_authentication.login()
        self.assertEqual(
            self.user_authentication.login(), "Invalid operation in current state"
        )
        self.assertEqual(self.user_authentication.state, "Logged In")

    def test_logout(self):
        """
        Checks logout
        """
        self.user_authentication.login()
        self.assertEqual(self.user_authentication.logout(), "Logout successful")
        self.assertEqual(self.user_authentication.state, "Logged Out")

    def test_logout_without_login(self):
        """
        Checks logout without login
        """
        self.assertEqual(
            self.user_authentication.logout(), "Invalid operation in current state"
        )
        self.assertEqual(self.user_authentication.state, "Logged Out")


class TestDocumentEditingSystem(unittest.TestCase):
    # 25---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.document_editing_system = DocumentEditingSystem()
        self.assertEqual(self.document_editing_system.state, "Editing")

    def test_init(self):
        """
        Checks init function
        """
        self.assertEqual(self.document_editing_system.state, "Editing")

    def test_save_document(self):
        """
        Checks login
        """
        self.assertEqual(
            self.document_editing_system.save_document(), "Document saved successfully"
        )
        self.assertEqual(self.document_editing_system.state, "Saved")

    def test_save_document_twice(self):
        """
        Checks save document two times in a row
        """
        self.document_editing_system.save_document()
        self.assertEqual(
            self.document_editing_system.save_document(),
            "Invalid operation in current state",
        )
        self.assertEqual(self.document_editing_system.state, "Saved")

    def test_edit_document(self):
        """
        Checks edit document
        """
        self.document_editing_system.save_document()
        self.assertEqual(
            self.document_editing_system.edit_document(), "Editing resumed"
        )
        self.assertEqual(self.document_editing_system.state, "Editing")

    def test_logout_without_login(self):
        """
        Checks logout without login
        """
        self.assertEqual(
            self.document_editing_system.edit_document(),
            "Invalid operation in current state",
        )
        self.assertEqual(self.document_editing_system.state, "Editing")


class TestElevatorSystem(unittest.TestCase):
    # 26---------------------------------------------------------------
    def setUp(self):
        """
        Function that runs at the beggining of each function.
        """
        self.elevator_system = ElevatorSystem()
        self.assertEqual(self.elevator_system.state, "Idle")

    def test_init(self):
        """
        Checks init function
        """
        self.assertEqual(self.elevator_system.state, "Idle")

    def test_move_up(self):
        """
        Checks move up function
        """
        self.assertEqual(self.elevator_system.move_up(), "Elevator moving up")
        self.assertEqual(self.elevator_system.state, "Moving Up")

    def test_move_up_twice(self):
        """
        Checks move up function two times in a row
        """
        self.elevator_system.move_up()
        self.assertEqual(
            self.elevator_system.move_up(), "Invalid operation in current state"
        )
        self.assertEqual(self.elevator_system.state, "Moving Up")

    def test_move_down(self):
        """
        Checks move down function
        """
        self.assertEqual(self.elevator_system.move_down(), "Elevator moving down")
        self.assertEqual(self.elevator_system.state, "Moving Down")

    def test_move_down_twice(self):
        """
        Checks move down function two times in a row
        """
        self.elevator_system.move_down()
        self.assertEqual(
            self.elevator_system.move_up(), "Invalid operation in current state"
        )
        self.assertEqual(self.elevator_system.state, "Moving Down")

    def test_move_up_and_then_move_down(self):
        """
        Checks move up and then move down
        """
        self.elevator_system.move_up()
        self.assertEqual(
            self.elevator_system.move_down(), "Invalid operation in current state"
        )
        self.assertEqual(self.elevator_system.state, "Moving Up")

    def test_move_down_and_then_move_up(self):
        """
        Checks move down and then move up
        """
        self.elevator_system.move_down()
        self.assertEqual(
            self.elevator_system.move_up(), "Invalid operation in current state"
        )
        self.assertEqual(self.elevator_system.state, "Moving Down")

    def test_stop_on_idle(self):
        """
        Checks just stop function
        """
        self.assertEqual(
            self.elevator_system.stop(), "Invalid operation in current state"
        )
        self.assertEqual(self.elevator_system.state, "Idle")

    def test_stop_after_move_up(self):
        """
        Checks stop after move up
        """
        self.elevator_system.move_up()
        self.assertEqual(self.elevator_system.stop(), "Elevator stopped")
        self.assertEqual(self.elevator_system.state, "Idle")

    def test_stop_after_move_down(self):
        """
        Checks stop after move down
        """
        self.elevator_system.move_down()
        self.assertEqual(self.elevator_system.stop(), "Elevator stopped")
        self.assertEqual(self.elevator_system.state, "Idle")

    def test_stop_after_each_movement(self):
        """
        Checks stop after move up
        """
        self.elevator_system.move_up()
        self.elevator_system.stop()
        self.elevator_system.move_down()
        self.assertEqual(self.elevator_system.stop(), "Elevator stopped")
        self.assertEqual(self.elevator_system.state, "Idle")
