from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTestCase(TestCase):
    def setUp(self):
        #creates a fake user
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_dashboard_requires_login(self):
        #gets the views home which gets the printed statements of those functions that are called in home 
        #checks the dashboard page loads
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_access_with_login(self):
        #fake user is logged in 
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        #checks if these are found in the HTML
        self.assertContains(response, "Total Revenue") 
        self.assertContains(response,"Total delivery sales per neighbourhood (£)")
            
    #make tests to see all graphs are rendered
