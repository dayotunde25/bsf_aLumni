from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_directory_view(self):
        # Login user to access directory
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('users:directory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/directory.html')

    def test_profile_view_requires_login(self):
        # Logout user to test redirect
        self.client.logout()
        response = self.client.get(reverse('users:profile', args=[self.user.id]))
        self.assertRedirects(response, f'/accounts/login/?next=/users/profile/{self.user.id}/')
