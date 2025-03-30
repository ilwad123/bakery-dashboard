from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_dashboard_requires_login(self):
        #gets the views 
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_access_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total Revenue") 