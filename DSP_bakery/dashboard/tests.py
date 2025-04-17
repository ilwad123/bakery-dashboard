from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTestCase(TestCase):
    def setUp(self):
        #creates a fake user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_dashboard_access_with_login(self):
        protected_views = ['home', 'performance', 'predicted-sales']
        templates = ['bakery.html', 'performance.html', 'predicted_sales.html']
        for view_name in protected_views:
            #fake user is logged in 
            self.client.login(username='testuser', password='testpass123')
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, templates[protected_views.index(view_name)])

    def test_requires_login_for_protected_views(self):
        #tests that the user is not logged in and should be redirected to the login page
        protected_views = ['home', 'performance', 'predicted-sales']

        for view_name in protected_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)



    # def test_dashboard_access_with_login(self):
    #     #fake user is logged in 
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     #checks if these are found in the HTML
    #     # self.assertContains(response, "Total Revenue")             
    # #make tests to see all graphs are rendered
    
    # def test_predict_sales_page(self):
    #     #tests user is logged in should allow us to access the page
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get(reverse('predicted-sales'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'predicted_sales.html')
    
    # def test_performance_page(self):
    #     #tests user is logged in should allow us to access the page
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get(reverse('performance'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'performance.html')
        
