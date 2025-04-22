from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from neo4j import GraphDatabase
import time
#authentication tests
class AuthTestCase(TestCase):
    def setUp(self):
        #creates a fake user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')  

    def test_dashboard_access_with_login(self):
        protected_views = ['home', 'performance', 'predicted-sales']
        templates = ['bakery.html', 'performance.html', 'predicted_sales.html']
        for view_name in protected_views:
            #fake user is logged in 
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, templates[protected_views.index(view_name)])

    def test_requires_login_for_protected_views(self):
        #tests that the user is not logged in and should be redirected to the login page
        #failed the test so went to views to add the login required decorator
        protected_views = ['home', 'performance', 'predicted-sales']

        for view_name in protected_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)
            self.assertRedirects(response, reverse('login'))
            self.assertTemplateUsed(response, 'login.html')
            self.assertContains(response, 'Please log in to access this page.')
          
    # def logout_tests(self):
    #     #tests that the user is logged in and should be redirected to the home page
    #     response = self.client.get(reverse('logout'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'logout.html')
    #     self.assertContains(response, 'You have been logged out.')
    #     #check if user is logged out
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertIn('/login/', response.url)
    #     self.assertRedirects(response, reverse('login'))
    #     self.assertTemplateUsed(response, 'login.html')
    #     self.assertContains(response, 'Please log in to access this page.')

#Neo4j scalability tests 
class Neo4jScalabilityTestCase(TestCase):
    
    def setUp(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

    def tearDown(self):
        self.driver.close()

    def test_transaction_node_scalability(self):
        with self.driver.session() as session:
            start_time = time.time()
            result = session.run("MATCH (t:Transaction) RETURN count(t) AS total")
            total = result.single()["total"]
            end_time = time.time()

            duration = round(end_time - start_time, 3)

            print(f"Total Transaction nodes: {total}")
            print(f"Query time: {duration} seconds")

            self.assertGreaterEqual(total, 1000, "Not enough transaction nodes for scalability test")
            self.assertLess(duration, 2.5, "Query took too long — may not scale well")
