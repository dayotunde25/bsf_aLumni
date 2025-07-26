from django.test import TestCase
from django.urls import reverse

class DashboardViewsTest(TestCase):
    def test_home_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_home_view_logged_in(self):
        # Create and login a user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')
