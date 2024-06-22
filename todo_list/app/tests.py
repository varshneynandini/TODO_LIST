from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import TODO
from app.forms import TODOForm


class ToDoAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.add_todo_url = reverse('add_todo')
        self.signout_url = reverse('signout')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.todo_data = {
            'title': 'Test Todo',
            'status': 'P',
            'priority': '1'
        }

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_signout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_unauthenticated(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.home_url}')

    def test_add_todo_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.add_todo_url, self.todo_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        todo_exists = TODO.objects.filter(title='Test Todo').exists()
        self.assertTrue(todo_exists)

    def test_delete_todo_view(self):
        self.client.login(username='testuser', password='testpass')
        todo = TODO.objects.create(user=self.user, **self.todo_data)
        response = self.client.get(reverse('delete_todo', args=[todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        todo_exists = TODO.objects.filter(id=todo.id).exists()
        self.assertFalse(todo_exists)

    def test_change_todo_view(self):
        self.client.login(username='testuser', password='testpass')
        todo = TODO.objects.create(user=self.user, **self.todo_data)
        response = self.client.get(reverse('change_todo', args=[todo.id, 'C']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        todo.refresh_from_db()
        self.assertEqual(todo.status, 'C')
