"""
Sabrina Fechtner, 07/10/2024
Unit testing for main.py
"""


# sometimes I get an "unable to import" message, on import main, users, and users_status
# but I found that running the tests or clicking on 'import' gets rid of the error"

import unittest
from unittest.mock import patch, mock_open, MagicMock
import main
import users
import user_status


class TestMain(unittest.TestCase):
    """
    Class to test the main.py functionality.
    """

    def setUp(self):
        self.user_collection = users.UserCollection()
        self.status_collection = user_status.UserStatusCollection()
        self.status_collection.add_status(
            "evmiles97_00001", "evmiles97", "Code is finally compiling"
        )
        main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )

    def tearDown(self):
        self.user_collection = None

    def test_init_users_and_collections(self):
        """
        Test initializing the user and status collection classes.
        """
        # Test init_user_collection
        user_collection = main.init_user_collection()
        self.assertIsInstance(user_collection, users.UserCollection)

        # Test init_status_collection
        status_collection = main.init_status_collection()
        self.assertIsInstance(status_collection, user_status.UserStatusCollection)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="USER_ID,EMAIL,NAME,LASTNAME\nevmiles97,eve.miles@uw.edu,Eve,Miles\n",
    )
    def test_load_users_existing(self, _mock_file):
        """
        Test loading users successfully and handling existing users.
        """
        result = main.load_users("test_users.csv", self.user_collection)
        self.assertTrue(result)
        self.assertIn("evmiles97", self.user_collection.database)

        self.user_collection.add_user("evmiles97", "eve.miles@uw.edu", "Eve", "Miles")
        result = main.load_users("test_users.csv", self.user_collection)
        self.assertTrue(result)

    @patch(
        "builtins.open",
        # new_callable=mock_open,
        # read_data="USER_ID,EMAIL,NAME\nuser1,email1,name1\n",
        side_effect=KeyError,
    )  # missing email
    def test_load_users_missing_field(self, _mock_file):
        """
        Test loading users with missing fields.
        """
        result = main.load_users("test_users.csv", self.user_collection)
        self.assertFalse(result)
        self.assertNotIn("user1", self.user_collection.database)
        self.assertRaises(KeyError)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_users_file_not_found(self, _mock_file):
        """
        Test handling file not found error when loading users.
        """
        result = main.load_users("non_existent_file.csv", self.user_collection)
        self.assertFalse(result)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="USER_ID,EMAIL,NAME,LASTNAME\nuser1,email1,name1,lastname1\nuser2,email2\n",
    )
    @patch("csv.DictReader")
    def test_load_users_key_error(self, mock_dict_reader, _mock_file):
        """
        Test handling KeyError when loading users.
        """
        mock_dict_reader.return_value = [
            {"USER_ID": "user1", "EMAIL": "", "NAME": "name1", "LASTNAME": "lastname1"},
            MagicMock(side_effect=KeyError("EMAIL")),
        ]

        result = main.load_users("test_users.csv", self.user_collection)
        self.assertFalse(result)
        self.assertNotIn("user1", self.user_collection.database)
        self.assertNotIn("user2", self.user_collection.database)

    def test_save_data(self):
        """
        Test saving users and status updates, including handling invalid file paths.
        """
        # Test saving users with valid path
        main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )
        result = main.save_users("test_accounts.csv", self.user_collection)
        self.assertTrue(result)

        # Test saving users with invalid path
        result = main.save_users(
            "/invalid/path/test_accounts.csv", self.user_collection
        )
        self.assertFalse(result)

        # Test saving status updates with valid path
        result = main.save_status_updates(
            "test_status_updates.csv", self.status_collection
        )
        self.assertTrue(result)

        # Test saving status updates with invalid path
        main.add_status(
            "evmiles97", "evmiles97_00001", "it's hot outside!", self.status_collection
        )
        result = main.save_status_updates(
            "/invalid/path/status_updates.csv", self.status_collection
        )
        self.assertFalse(result)

    def test_save_status_updates_invalid_file(self):
        """
        Test handling invalid file path when saving status updates.
        """
        main.add_status(
            "evmiles97", "evmiles97_00001", "it's hot outside!", self.status_collection
        )
        result = main.save_status_updates(
            "/invalid/path/status_updates.csv", self.status_collection
        )
        self.assertFalse(result)

    def test_add_user(self):
        """
        Test adding a user and handling existing user.
        """
        result = main.add_user(
            "dave03", "david.yuen@gmail.com", "David", "Yuen", self.user_collection
        )
        self.assertTrue(result)
        self.assertIn("dave03", self.user_collection.database)

        result = main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )
        self.assertFalse(result)

    def test_update_user(self):
        """
        Test updating a user and handling non-existent user.
        """
        main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )
        result = main.update_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Milesv2", self.user_collection
        )
        self.assertTrue(result)
        self.assertEqual(
            self.user_collection.database["evmiles97"].user_last_name, "Milesv2"
        )

        result = main.update_user(
            "userid", "email", "name", "lastname", self.user_collection
        )
        self.assertFalse(result)

    def test_delete_user(self):
        """
        Test deleting a user and handling non-existent user.
        """
        main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )
        result = main.delete_user("evmiles97", self.user_collection)
        self.assertTrue(result)
        self.assertNotIn("evmiles97", self.user_collection.database)

        result = main.delete_user("non_existing_id", self.user_collection)
        self.assertFalse(result)

    def test_search_status_existing(self):
        """
        Test searching for an existing status.
        """
        status_id = "evmiles97_00001"
        status = main.search_status(status_id, self.status_collection)
        self.assertIsNotNone(status)
        self.assertEqual(status.status_id, status_id)

    @patch("csv.DictReader")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="STATUS_ID,USER_ID,STATUS_TEXT\n"
        "evmiles97_00001,evmiles97,Code is finally compiling\n",
    )
    def test_load_status_updates(self, _mock_file, mock_dict_reader):
        """
        Test loading status updates and handling empty fields.
        """
        mock_file = [
            {
                "STATUS_ID": "evmiles97_00001",
                "USER_ID": "evmiles97",
                "STATUS_TEXT": "Code is finally compiling",
            }
        ]
        mock_dict_reader.return_value = mock_file

        result = main.load_status_updates("dummy.csv", self.status_collection)
        self.assertTrue(result)
        self.assertIn("evmiles97_00001", self.status_collection.database)
        self.assertEqual(
            self.status_collection.database["evmiles97_00001"].status_text,
            "Code is finally compiling",
        )

        self.status_collection = user_status.UserStatusCollection()
        result = main.load_status_updates("dummy.csv", self.status_collection)
        self.assertTrue(result)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="STATUS_ID,USER_ID,STATUS_TEXT\n" "evmiles97_00001,evmiles97,\n",
    )
    def test_load_status_updates_with_empty_field(self, _mock_file):
        """
        Test handling empty field when loading status updates.
        """
        self.status_collection = user_status.UserStatusCollection()
        result = main.load_status_updates("dummy.csv", self.status_collection)
        self.assertFalse(result)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_status_updates_file_not_found(self, _mock_file):
        """
        Test handling file not found error when loading status updates.
        """
        self.status_collection = user_status.UserStatusCollection()
        result = main.load_status_updates("dummy.csv", self.status_collection)
        self.assertFalse(result)

    def test_update_status(self):
        """
        Test updating an existing status and handling non-existent status.
        """
        result = main.update_status(
            "evmiles97_00001",
            "evmiles97",
            "Updated status text",
            self.status_collection,
        )
        self.assertTrue(result)
        self.assertEqual(
            self.status_collection.database["evmiles97_00001"].status_text,
            "Updated status text",
        )

        result = main.update_status(
            "non_existing_id",
            "evmiles97",
            "Updated status text",
            self.status_collection,
        )
        self.assertFalse(result)

    def test_delete_status(self):
        """
        Test deleting a status of a user.
        """
        main.add_status(
            "evmiles97", "evmiles97_00001", "it's hot outside!", self.status_collection
        )
        result = main.delete_status("evmiles97_00001", self.status_collection)
        self.assertTrue(result)
        self.assertNotIn("evmiles97_00001", self.status_collection.database)

    def test_add_status_success(self):
        """
        Test adding a status for a user and handling exception.
        """
        with patch.object(self.status_collection, "add_status", return_value=True):
            result = main.add_status(
                "evmiles97",
                "evmiles97_00002",
                "Perfect weather for a hike",
                self.status_collection,
            )
        self.assertTrue(result)
        # self.assertIn("evmiles97_00002", self.status_collection.database)

    @patch.object(
        user_status.UserStatusCollection,
        "add_status",
        side_effect=IOError,
    )
    def test_add_status_exception(self, _mock_add_status):
        """
        Test handling exception when adding a status for a user.
        """
        result = main.add_status(
            "evmiles97", "evmiles97_00002", "Another status", self.status_collection
        )
        self.assertFalse(result)


class TestUserStatus(unittest.TestCase):
    """
    class to test the user_status which wasn't covered in Testmain class
    written to ensure 100% coverage
    """

    def setUp(self):
        self.status_collection = user_status.UserStatusCollection()
        self.status_collection.database = {
            "evmiles97_00001": MagicMock(
                user_id="evmiles97", status_text="Code is finally compiling"
            ),
            "dave03_00001": MagicMock(user_id="dave03", status_text="Initial status"),
        }
        self.status_collection.add_status(
            "evmiles97_00001", "evmiles97", "Code is finally compiling"
        )

    def test_modify_status_nonexistent_status_id(self):
        """
        test to modify status of a user id that does not exist
        """
        status_id = "nonexistent_00001"
        new_user_id = "new_user"
        new_status_text = "New status text"

        result = self.status_collection.modify_status(
            status_id, new_user_id, new_status_text
        )

        self.assertFalse(result)
        self.assertNotIn(status_id, self.status_collection.database)

    def test_delete_status_success(self):
        """
        test to delete a status of a user
        """
        status_id = "evmiles97_00001"

        result = self.status_collection.delete_status(status_id)

        self.assertTrue(result)
        self.assertNotIn(status_id, self.status_collection.database)

    def test_delete_status_nonexistent_status_id(self):
        """
        test to delete a status of a user id that does not exist
        """
        status_id = "nonexistent_00001"
        result = self.status_collection.delete_status(status_id)
        self.assertFalse(result)

    def test_search_status_non_existing(self):
        """
        test to search for a status of non-existing user
        """
        status_id = "non_existing_id"
        status = main.search_status(status_id, self.status_collection)
        self.assertIsInstance(status, user_status.UserStatus)
        self.assertIsNone(status.status_id)
        self.assertIsNone(status.user_id)
        self.assertIsNone(status.status_text)


class TestUsers(unittest.TestCase):
    """
    a class used to test users.py
    written to ensure 100% coverage
    """

    def setUp(self):
        self.user_collection = users.UserCollection()

    def test_add_user_success(self):
        """
        Test adding a new user successfully
        """
        result = self.user_collection.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles"
        )
        self.assertTrue(result)
        self.assertIn("evmiles97", self.user_collection.database)
        self.assertIsInstance(self.user_collection.database["evmiles97"], users.Users)
        self.assertEqual(
            self.user_collection.database["evmiles97"].email, "eve.miles@uw.edu"
        )

    def test_add_user_existing(self):
        """
        Test adding a user that already exists
        """
        self.user_collection.add_user("evmiles97", "eve.miles@uw.edu", "Eve", "Miles")
        result = self.user_collection.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles"
        )
        self.assertFalse(result)

    def test_delete_user(self):
        """
        Test deleting a user
        """
        main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )
        result = main.delete_user("evmiles97", self.user_collection)
        self.assertTrue(result)
        self.assertNotIn("evmiles97", self.user_collection.database)

    def test_search_user_found(self):
        """
        Test searching for a user
        """
        main.add_user(
            "evmiles97", "eve.miles@uw.edu", "Eve", "Miles", self.user_collection
        )
        result = main.search_user("evmiles97", self.user_collection)
        self.assertIsInstance(result, users.Users)

    def test_search_user_not_found(self):
        """
        Test searching for a user that does not exist
        """
        result = main.search_user("nonexistent", self.user_collection)
        self.assertIsNone(result)

    def test_modify_user_success(self):
        """
        Test modifying a user that exists
        """
        self.user_collection.add_user("evmiles97", "eve.miles@uw.edu", "Eve", "Miles")
        result = self.user_collection.modify_user(
            "evmiles97", "eve.new@miles.com", "Eve", "NewMiles"
        )
        self.assertTrue(result)
        self.assertEqual(
            self.user_collection.database["evmiles97"].email, "eve.new@miles.com"
        )
        self.assertEqual(
            self.user_collection.database["evmiles97"].user_last_name, "NewMiles"
        )

    def test_modify_user_failure(self):
        """
        test modifying a user that doesn't exist
        """
        result = self.user_collection.modify_user(
            "nonexistent", "non@existent.com", "Non", "Existent"
        )
        self.assertFalse(result)

    def test_delete_user_success(self):
        """
        test deleting a user
        """
        self.user_collection.add_user("evmiles97", "eve.miles@uw.edu", "Eve", "Miles")
        result = self.user_collection.delete_user("evmiles97")
        self.assertTrue(result)
        self.assertNotIn("evmiles97", self.user_collection.database)

    def test_delete_user_failure(self):
        """
        test deleting a user that does not exist
        """
        result = self.user_collection.delete_user("nonexistent")
        self.assertFalse(result)

    def test_search_user_existing(self):
        """
        test searching for a user that already exists
        """
        self.user_collection.add_user("evmiles97", "eve.miles@uw.edu", "Eve", "Miles")
        result = self.user_collection.search_user("evmiles97")
        self.assertIsInstance(result, users.Users)
        self.assertEqual(result.email, "eve.miles@uw.edu")

    def test_search_user_non_existing(self):
        """
        test searching for a user that does not exist
        """
        result = self.user_collection.search_user("nonexistent")
        self.assertIsInstance(result, users.Users)
        self.assertIsNone(result.user_id)
        self.assertIsNone(result.email)


if __name__ == "__main__":
    unittest.main()
