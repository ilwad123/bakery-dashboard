from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from neo4j import GraphDatabase
import time
from .views import line_graph ,bar_graph, popular_category,sales_data_CNNLTSM,most_popular,performance_each_driver,driver_info,popular_product_association_list
from .cnn_model import predict_from_graph_data

from django.urls import reverse
import pandas as pd
import numpy as np 
import torch
#authentication tests
class AuthTestCase(TestCase):
    def setUp(self):
        #creates a fake user
        self.user = User.objects.create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

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
        self.client.logout()
        #needs to be logged out to test the login required decorator
        protected_views = ['home', 'performance', 'predicted-sales']

        
        for view_name in protected_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)
            response = self.client.get(reverse(view_name), follow=True)
            self.assertTemplateUsed(response, 'login.html')
            self.assertContains(response, 'WELCOME BACK')

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

class smoketest_TestCase(TestCase):
            #202 means the page was created successfully
            #302 means it redirected to the login page
    def setUp(self):
        #creates a fake user
        self.user = User.objects.create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

    def test_smoke_test(self):
        # Test that the home page loads successfully
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bakery.html')
        self.assertContains(response, 'Net Sales')
        
    def test_performance_page(self):
        # Test that the performance page loads successfully
        response = self.client.get(reverse('performance'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'performance.html')
        self.assertContains(response, 'Average delivery time of all Drivers')
    
    def test_predicted_sales_page(self):
        # Test that the predicted sales page loads successfully
        response = self.client.get(reverse('predicted-sales'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'predicted_sales.html')
        #checks the page has the right content
        self.assertContains(response, 'Projected Revenue')
        #checks the chart is on the page
        self.assertContains(response, 'predictionChart')     
        
    def test_login_page(self):
        # Test that the login page loads successfully
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'WELCOME BACK')
    
    def test_logout_redirects(self):
        response = self.client.get(reverse('logout'))
        #302 means it redirected to the login page
        self.assertEqual(response.status_code, 302)  
        self.assertIn(reverse('login'), response.url) 
        
class graphs_Tests(TestCase):
    def test_line_graph_returns_months_and_sales(self):
        #call the function to test the line graph
        months, sales = line_graph(None) 
        # Check that the function returns two lists
        self.assertIsInstance(months, list)
        self.assertIsInstance(sales, list)
        # Check that the lengths of the lists are equal
        self.assertEqual(len(months), len(sales))
        # Check format of months like "Jan 2024"
        for month in months:
            self.assertRegex(month, r"^[A-Z][a-z]{2} \d{4}$")
        # Check sales are all float
        for value in sales:
            self.assertIsInstance(value, float)
        # Print the results to see the output test 
        print("Months:", months)
        print("Sales:", sales)
    
    def test_bar_graph(self):
        neighbourhood, total_neighborhood_sales=bar_graph(None) 
        self.assertIsInstance(neighbourhood, list)
        self.assertIsInstance(total_neighborhood_sales, list)
        # Check that the lengths of the lists are equal
        self.assertEqual(len(neighbourhood), len(total_neighborhood_sales))
        # Check that the neighbourhood names are strings
        for name in neighbourhood:
            self.assertIsInstance(name, str)
        # Check that the sales values are floats
        for value in total_neighborhood_sales:
            self.assertIsInstance(value, float)
        print("Neighbourhood:", neighbourhood)
        print("Total Neighborhood Sales:", total_neighborhood_sales)
    
    def test_pie_chart_graph(self):
        #Total quantities sold by category
        categories,quantities=popular_category(None)
        # Check that the function returns two lists
        self.assertIsInstance(categories, list)
        self.assertIsInstance(quantities, list)
        # Check that the lengths of the lists are equal
        self.assertEqual(len(categories), len(quantities))
        self.assertGreaterEqual(len(categories),4 , "Expected at least 4 product categories")
        #decreasing order
        self.assertTrue(all(quantities[i] >= quantities[i+1] for i in range(len(quantities)-1)),
                        "Quantities are not in decreasing order")
        print("Categories:", categories)
        print("Quantities:", quantities)
    
from django.test import TestCase, RequestFactory
from .views import most_popular

class PopularProductTest(TestCase):
    def test_most_popular_product_returns_valid_data(self):
        factory = RequestFactory()
        #create a fake request with the first page of products
        request = factory.get('/?page=1')  
        # Call your view-like function with the fake request
        paginated_data = most_popular(request)
        items = list(paginated_data)
        # checks that the function returns a list of tuples
        # where each tuple contains a product name and quantity sold
        self.assertIsInstance(items, list)
        self.assertGreaterEqual(len(items), 1)
        self.assertIsInstance(items[0][0], str)  # Product name
        self.assertIsInstance(items[0][1], (int, float))  # Quantity
        # Check descending order of quantities
        for i in range(len(items) - 1):
            self.assertGreaterEqual(items[i][1], items[i + 1][1])
        print("Most popular products (page 1):", items)

class MLModelTests(TestCase):
    def test_cnn_lstm_prediction_output(self):
        # runs the model and checks the output
        df = sales_data_CNNLTSM()
        predictions = predict_from_graph_data(df)

        #checks the output is in an array and has a length of 7
        self.assertIsInstance(predictions, np.ndarray)
        self.assertEqual(len(predictions), 7)
        #prints the predictions to see the output of the test
        print("Model Predictions:", predictions)
        

class DriverInfoTests(TestCase):
    def test_driver_info_returns_correct_structure(self):
        driver_ids, total_deliveries, avg_times ,top_driver= driver_info(None)

        # Ensure all lists are the same length
        self.assertEqual(len(driver_ids), len(total_deliveries))
        self.assertEqual(len(driver_ids), len(avg_times))

        #checks the data types are right 
        for d in driver_ids:
            self.assertIsInstance(d, (int, str))
        for t in total_deliveries:
            self.assertIsInstance(t, (int, float))
        for a in avg_times:
            self.assertIsInstance(a,str)

        
        print("Driver Info Test Passed:", driver_ids, total_deliveries, avg_times,top_driver)


class PerformanceEachDriverTests(TestCase):
    def test_performance_data_returns_valid_metrics(self):
        driver_ids, perf_ids, total_sales, total_distance, sales_per_km = performance_each_driver(None)

        #lengths match 
        #so the system doesn't break 
        self.assertEqual(len(driver_ids), len(perf_ids))
        self.assertEqual(len(perf_ids), len(total_sales))
        self.assertEqual(len(total_sales), len(total_distance))
        self.assertEqual(len(sales_per_km), len(driver_ids))

        self.assertTrue(all(isinstance(val, (int, str)) for val in driver_ids))
        self.assertTrue(all(isinstance(val, (int, float)) for val in total_sales))
        self.assertTrue(all(isinstance(val, (int, float)) for val in total_distance))
        self.assertTrue(all(isinstance(val, float) for val in sales_per_km))

        print("Performance Per Driver:", driver_ids, sales_per_km)

class PopularTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')
        # You can create mock data here if needed

    def test_popular_product_combinations_table_renders_correctly_on_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bakery.html')
        self.assertContains(response, '<table id="Popular_Product_Associations">')

        # popular_asso = popular_product_association_list(None)

         # Get paginated data passed to template
        product_sales = response.context.get('products_sales')
        self.assertIsNotNone(product_sales)
        self.assertGreater(len(product_sales), 0)

        print("Popular product combinations appear on home page.")
