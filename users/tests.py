from django.test import TestCase
from django.urls import reverse

from users.forms import CustomUserCreationForm


class TestRegistration(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'stinky',
            'email': 'stinky@gmail.com',
            'password1': 'SeKrIt123',
            'password2': 'SeKrIt123'}

        self.valid_response = self.client.post(
            reverse('users:signup'),
            self.valid_data,
            follow=True
        )

    def test_valid_form(self):
        """
        Test valid registration.
        """
        response = self.valid_response
        self.assertRedirects(response, reverse('pages:home'))

    def test_valid_message(self):
        """Test valid registration messages, both in the html and the context."""
        response = self.valid_response
        expected_message = f"Account created for {self.valid_data['email']}!"
        messages = list(response.context['messages'])

        # Test message in html
        self.assertIn(expected_message.encode('utf-8'), response.content)

        # Test the messages iterable
        for message in messages:
            self.assertEqual(str(message), expected_message)

    def test_invalid_data_bad_password(self):
        """Test no redirect for a common password ('password')."""
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'password'

        response = self.client.post(
            reverse('users:signup'),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_data_no_username(self):
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = ''

        response = self.client.post(
            reverse('users:signup'),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)


class TestRegistrationForm(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'stinky',
            'email': 'stinky@gmail.com',
            'password1': 'SeKrIt123',
            'password2': 'SeKrIt123'}

        form = CustomUserCreationForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'email': '',
                'password1': 'sEkRit12',
                }

        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
