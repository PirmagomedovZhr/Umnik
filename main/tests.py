from django.test import TestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from .forms import SignInForm
from .models import User
from .forms import SignUpForm


class SignUpFormTestCase(TestCase):
    def test_form_valid(self):
        form_data = {
            'username': 'testuser',
            'position': 'architect',
            'password': 'password123',
            'repeat_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'username': 'testuser',
            'position': 'architect',
            'password': 'password123',
            'repeat_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.position, 'architect')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')


class SignInViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('signin')
        self.user = User.objects.create_user(
            username='testuser', password='secretpassword'
        )

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main/signin.html')

    def test_view_displays_form(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsInstance(form, SignInForm)

    def test_view_does_not_authenticate_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)
