#!/usr/bin/python3
"""Module forstorage tests."""

import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os


class TestDBStorage(unittest.TestCase):
    """Tests the dbstorage."""
    def setUp(self):
        """Sets up a test environment."""
        self.db = self.setup_database_connection()

    def tearDown(self):
        """Cleans up after each test."""
        self.db.close()

    def setup_database_connection(self):
        """Creates a reusable database connection."""
        required_env_vars = ['HBNB_MYSQL_USER', 'HBNB_MYSQL_HOST',
                             'HBNB_MYSQL_PWD', 'HBNB_MYSQL_DB']
        missing_vars = [var for var in required_env_vars
                        if os.getenv(var) is None]

        if missing_vars:
            raise ValueError(f"The following MySQL environment variables are "
                             "missing or not accessible: {', '.join "
                             "(missing_vars)}")
        try:
            return MySQLdb.connect(
                user=os.getenv('HBNB_MYSQL_USER'),
                host=os.getenv('HBNB_MYSQL_HOST'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                port=3306,
                db=os.getenv('HBNB_MYSQL_DB')
                )
        except Exception as e:
            raise ValueError(f"Unable to establish a MySQL connection: "
                             "{str(e)}")

    def test_new_and_save(self):
        """Tests creation of new user and  saves to database."""
        db = self.db.cursor()
        db.execute('SELECT COUNT(*) FROM users')
        old_count = db.fetchone()[0]

        new_user = User(**{
            'first_name': 'jack',
            'last_name': 'bond',
            'email': 'jack@bond.com',
            'password': '12345'
            })

        new_user.save()

        db.execute('SELECT COUNT(*) FROM users')
        new_count = db.fetchone()[0]
        db.close()
        self.assertEqual(new_count, old_count + 1)

    def test_retrieve_all_users(self):
        """Tests retrieving all users from database."""
        db = self.db.cursor
        self.cursor.execute('SELECT COUNT(*) FROM users')
        old_count = db.fetchone()[0]

        all_users = storage.all(User)
        db.close()
        self.assertEqual(len(all_users), old_count)

    def test_update_user(self):
        """Test updating a user's attributes."""
        new_user = User(
                email='john2020@gmail.com',
                password='password',
                first_name='John',
                last_name='Zoldyck'
                )
        new_user.save()
        new_user.email = 'johnny@gmail.com'
        new_user.save()

        self.cursor.execute('SELECT * FROM users WHERE id="{}"'
                            .format(new_user.id))
        updated_user = self.cursor.fetchone()
        db.close

        self.assertEqual(updated_user[1], 'johnny@gmail.com')

    def test_retrieve_specific_user(self):
        """Test retrieving a specific user from the database."""
        db = self.db.cursor()
        new_user = User(
                email='john2020@gmail.com',
                password='password',
                first_name='John',
                last_name='Zoldyck'
                )
        new_user.save()

        retrieved_user = storage.get(User, new_user.id)
        db.close()

        self.assertEqual(new_user.id, retrieved_user.id)
        self.assertEqual(new_user.email, retrieved_user.email)

    def test_invalid_input_handling(self):
        """Tests how the system handles invalid input data."""
        invalid_data = [
                ['Invalid', 'Input'],
                {'email': 123, 'password': 'pass', 'firstname': 'John'},
                {'email': 'jack@bond.com', 'password': 'pass'},
                {}
                ]
        for data in invalid_data:
            with self.assertRaises(TypeError):
                invalid_user = User(**data)
                invalid_user.save()


if __name__ == "__main__":
    unittest.main()
