"""
Testes para os models.
"""

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase


class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """Teste: Criar um usuário com email."""
        email = 'test@example.com'
        password = 'tespass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_exists(self):
        "Teste: Criar um usuário com um email já cadastrado."
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        exists = get_user_model().objects.filter(email=email).exists()
        self.assertTrue(exists)

        with self.assertRaises(ValueError):
            user2 = get_user_model().objects.create_user(
                email=email,
                password='testpass1234',
            )
        
    def test_new_user_email_normalized(self):
        """Teste: Normalização para os emails cadastrados."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email)
            self.assertEqual(user.email, expected)
    
    def test_new_user_without_email_raises_error(self):
        """Teste: Criar um usuário sem lançar um error de ValueError no email."""

        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email='',
                password='testpass123',
            )

    def test_create_superuser(self):
        """Teste: Criar um superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
