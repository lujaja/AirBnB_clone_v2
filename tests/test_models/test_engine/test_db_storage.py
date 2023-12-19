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
        self.db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                                  host=os.getenv('HBNB_MYSQL_HOST'),
                                  passwd=os.getenv('HBNB_MYSQL_PWD'),
                                  port=3306,
                                  db=os.getenv('HBNB_MYSQL_DB'))
        self.cursor = self.db.cursor()

    def tearDown(self):
        """Cleans up after each test."""
        self.cursor.close()
        self.db.close()

    def test_new_and_save(self):
        """Tests creation of new user and  saves to database."""
        self.cursor.execute('SELECT COUNT(*) FROM users')
        old_count = self. cursor.fetchall()

        new_user = User(**{
            'first_name': 'jack',
            'last_name': 'bond',
            'email': 'jack@bond.com',
            'password': 12345
            })

        new_user.save()

        self.cursor.execute('SELECT COUNT(*) FROM users')
        new_count = self.cursor.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)

    def test_retrieve_all_users(self):
        """Tests retrieving all users from database."""
        self.cursor.execute('SELECT COUNT(*) FROM users')
        old_count = self.cursor.fetchall()

        all_users = storage.all(User)
        self.assertEqual(len(all_users), old_count[0][0])

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

        self.assertEqual(updated_user[1], 'johnny@gmail.com')

    def test_retrieve_specific_user(self):
        """Test retrieving a specific user from the database."""
        new_user = User(
                email='john2020@gmail.com'
                password='password'
                first_name='John'
                last_name='Zoldyck'
                )
        new_user.save()
        retrieved_user = storage.get(User, new_user.id)
        self.assertEqual(new_user.id, retrieved_user.id)
        self.assertEqual(new_user.email, retrieved_user.email)

        invalid_data = [
                ['Invalid', 'Input'],
                {'email': 123, 'password': 'pass', 'firstname': 'John'},
                {'email': 'jack@bond.com', 'password': 'pass'},
                {}
                ]

    def test_invalid_input_handling(self):
        """Tests how the system handles invalid input data."""
        for data in self.invalid_data:
            with self.assertRaises(TypeError):
                invalid_user = User(**data)
                invalid_user.save()
