from accounts.forms import UserRegisterForm, UserActivateAgainForm

from django.test import TestCase

from accounts.models import User


class TestForms(TestCase):
    def setUp(self):
        self.username = 'user_1'
        self.password = '456dsfadfs'
        self.email = 'user@gmail.com'

    def test_register_form_valid_data(self):
        form = UserRegisterForm(
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password
            }
        )

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class TestUserActivateAgainForm(TestCase):
    def setUp(self):
        self.data = {
            'email': 'user@gmail.com',
        }

        User.objects.create(
            username='user',
            password='456dsfadfs',
            email=self.data['email']
        )

        self.form = UserActivateAgainForm

    def test_reactivation_form_valid_data(self):
        form = self.form(data=self.data)
        form.is_valid()
        self.assertEqual(self.data['email'], form.clean_email())

    def test_reactivation_form_with_no_data(self):
        form = self.form(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
