from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successfuly(self):
        """Test creating new user with email"""
        email = "test@gmail.com"
        password = "p455WORDC#"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test whether email for new user has been normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "test1234")

        self.assertEqual(user.email, email.lower())

    def test_new_user_valid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test1234")

    def test_create_new_superuser(self):
        """Test creating new super user"""
        user = get_user_model().objects.create_superuser(
            "test@GMAIL.com", "test213"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
