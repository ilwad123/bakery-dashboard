from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from neo4j import GraphDatabase
import os
#used to hash passwords and the authenticate function
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
#used to make pages that are paginated
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime
import json
from django.http import JsonResponse
#used to create heatmaps
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.use('Agg')


driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

@login_required(login_url="/login/")
def home(request):
    months, sales = line_graph(request)
    neighbourhood,total_neighborhood_sales=bar_graph(request)
    products_sales=most_popular(request)
    categories,quantities=popular_category(request)
    num_of_drivers1 = num_of_drivers(request)
    num_of_transactions = num_of_transactions1(request)
    months2,num_of_transactions_monthly=num_of_transactions_monthly1(request)
    popular_product = most_popular1(request)
    heatmap_path = plot_heatmap()
    context = {
        'months': json.dumps(months),
        'sales': json.dumps(sales),
        'products_sales': products_sales,
        'neighbourhood': json.dumps(neighbourhood),
        'total_neighborhood_sales': json.dumps(total_neighborhood_sales),
        'categories': json.dumps(categories),
        'quantities': json.dumps(quantities), 
        'num_of_drivers': json.dumps(num_of_drivers1),
        'num_of_transactions': json.dumps(num_of_transactions),
        'num_of_transactions_monthly': json.dumps(num_of_transactions_monthly),
        'months2': json.dumps(months2),
        'popular_product': popular_product,
        'heatmap_path': heatmap_path
    }
    print("context")
    return render(request, 'bakery.html', context)

def logged_in_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print(f"Attempting to authenticate user: {username}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("Authentication successful!")
            login(request, user)
            return redirect('home')
        else:
            print("Authentication failed!")
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

    
def logout_view(request):
    logout(request)
    # Redirect to a login page.
    return redirect('login')
    
def login_page(request):
    return render(request,'login.html')

# def create_admin():
#     user, created = User.objects.get_or_create(username="admin")
#     if created:
#         user.set_password("bakery123")  # Password is hashed when set
#         user.save()
#     return HttpResponse("Admin created")

# create_admin()  # Passing None as request, since we're in shell
#finish by create_admin in shell 
def heatmap(request):
    # Execute the Neo4j query to fetch datetime and total_sales
    with driver.session() as session:
        heatmap1 = session.run("""
        MATCH (t:Transaction)
        WITH t.Datetime AS datetime, t.Total AS total_sales
        // Extract day and hour from the datetime
        WITH datetime, total_sales,
                toInteger(date(datetime).dayOfWeek) AS day_of_week, 
                toInteger(datetime.hour) AS hour_of_day
        // get total sales by day and hour
        RETURN day_of_week, hour_of_day, SUM(total_sales) AS total_sales
        ORDER BY day_of_week, hour_of_day
        """)

        
        day_of_week = []
        time_of_day = []
        total_sales = []  

        # Get the datetime and total_sales values from the query 
        for record in heatmap1: 
                day = record['day_of_week']
                hour = record['hour_of_day']
                sales = record['total_sales']
                
                # Update the lists with the values
                day_of_week.append(day)
                time_of_day.append(hour)
                total_sales.append(sales)

        return day_of_week, time_of_day, total_sales
 

def plot_heatmap():
    # Assuming the heatmap function returns day_of_week, time_of_day, and total_sales
    day_of_week, time_of_day, total_sales = heatmap(None)
    # Create a 7x24 matrix to store the sales data
    sales_matrix = np.zeros((7, 24))
    #goes through each record and assigns sales to the specific day and hour 
    for i in range(len(day_of_week)):
        day = day_of_week[i]   - 1
        hour = time_of_day[i]
        sales = total_sales[i]
        # print(f"Day: {day}, Hour: {hour}, Sales: {sales}") used for debugging
        
        sales_matrix[day, hour] = sales

    hours1 = [f'{hour}:00' for hour in range(9, 24)]  # Hours from 9 to 23 

    # Plot the heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(sales_matrix[:, 9:], cmap='YlGnBu', annot=True, fmt=".2f",  
                xticklabels=hours1, 
                yticklabels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    plt.title('Heatmap of Sales Volume by Day and Hour')
    plt.xlabel('Hour of the Day (9-23)')
    plt.ylabel('Day of the Week (Monday to Sunday)')
    plt.tight_layout()
    # Save the plot as an image
    filepath = "static/data_files/sales_heatmap.png"
    plt.savefig(filepath)
    plt.close()
    return filepath



def reports(request):
    return render(request,'reports.html')

def my_view(request):
    # Open a session to run the Neo4j query
    with driver.session() as session:
        # Run a simple query to fetch nodes
        result = session.run("MATCH (n) RETURN n LIMIT 10")
        node = result.value()

def line_graph(request):
    print("Line graph view triggered") 
    with driver.session() as session:
        monthly_sales = session.run("""
            MATCH (t:Transaction)
            WITH datetime({ year: t.Datetime.year, month: t.Datetime.month, day: 1 }) AS month, SUM(t.Total) AS monthly_sales
            RETURN month, monthly_sales
            ORDER BY month
        """)

        months = []
        sales = []
        for record in monthly_sales:
            dt = record["month"]
            months.append(dt.strftime("%b %Y"))
            sales.append(round(record["monthly_sales"], 2))

        # print("Months:", months)
        # print("Sales:", sales)
    
    return months, sales


def bar_graph(request):
    print ("bar graph triggered")
    with driver.session() as session:
        neighbourhoodsales = session.run("""
            MATCH (t:Transaction)
            WITH t.Place AS Place, SUM(t.Total) AS total_neighborhood_sales
            RETURN Place , total_neighborhood_sales
            ORDER BY total_neighborhood_sales
        """)
        neighbourhood = []
        total_neighborhood_sales= []
        for record in neighbourhoodsales:
            neighbourhood.append(record['Place'])
            total_neighborhood_sales.append(record["total_neighborhood_sales"])

    return neighbourhood, total_neighborhood_sales



def popular_category(request):
    with driver.session() as session:
            print("popular category triggered/donut chart")
            category1=session.run("""
                MATCH (t:Transaction)
                UNWIND t.Product_Names AS Product
                UNWIND t.Quantity_Per_Product AS Quantity
                WITH TRIM(Product) AS New_product, 
                TOFLOAT(TRIM(REPLACE(REPLACE(Quantity, "[", ""), "]", ""))) AS New_quantity
                WHERE New_quantity IS NOT NULL  // Filter out invalid or NULL quantities
                MATCH (p:Product {Name: New_product})-[:BELONGS_TO]->(c:Category)
                WITH c.Category AS Category, SUM(New_quantity) AS Total_quantity
                RETURN Category, Total_quantity
                ORDER BY Total_quantity DESC

            """)
            
            categories = []
            quantities= []
            for record in category1:
                categories.append(record['Category'])
                quantities.append(record["Total_quantity"])

    return categories,quantities

def num_of_drivers(request):
    with driver.session() as session:
        num_of_drivers1 = session.run("""
            MATCH (d:Driver)
            RETURN COUNT(d) AS num_of_drivers
        """)
        for record in num_of_drivers1:
            num_of_drivers1 = record["num_of_drivers"]
    return num_of_drivers1

def num_of_transactions1(request):
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Transaction)
            RETURN COUNT(t) AS num_of_transactions
        """)
        for record in result:
            num_of_transactions = record["num_of_transactions"]
    return num_of_transactions
def num_of_transactions_monthly1(request):
    with driver.session() as session:
        print("Fetching monthly transactions")
        result = session.run("""
            MATCH (t:Transaction)
            WITH datetime({ year: t.Datetime.year, month: t.Datetime.month, day: 1 }) AS month, COUNT(t) AS num_of_transactions
            RETURN month, num_of_transactions
            ORDER BY month
        """)
        
        months2 = []  # List to hold the month names
        num_of_transactions_monthly = []  # List to hold the number of transactions per month
        
        # Loop through the result and store the month and transaction count
        for record in result:
            dt = record["month"]
            months2.append(dt.strftime("%b %Y"))  # Format month as "Month Year" (e.g., Jan 2025)
            num_of_transactions_monthly.append(record["num_of_transactions"]) 
        
    # Return the months and transaction counts
    return months2, num_of_transactions_monthly


def most_popular(request):
    with driver.session() as session:
        most_popular = session.run("""
                MATCH (t:Transaction)
                UNWIND t.Product_Names AS Product
                UNWIND t.Quantity_Per_Product AS Quantity 
                WITH TRIM(Product) AS New_product, TOFLOAT(TRIM(Quantity)) AS New_quantity
                WHERE New_quantity IS NOT NULL  
                RETURN New_product, SUM(New_quantity) AS Total_product
                ORDER BY Total_product DESC
            """)
        
        products_sales = [(record['New_product'], record["Total_product"]) for record in most_popular]
        
        per_page = 5  
        page_number = request.GET.get('page', 1)  
        paginator = Paginator(products_sales, per_page)  
        paginated_products = paginator.get_page(page_number)  
    
    return paginated_products

def most_popular1(request):
    #just get the first product most popular
    #just return one product name
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Transaction)
            UNWIND t.Product_Names AS Product
            UNWIND t.Quantity_Per_Product AS Quantity 
            WITH TRIM(Product) AS New_product, TOFLOAT(TRIM(Quantity)) AS New_quantity
            WHERE New_quantity IS NOT NULL  
            RETURN New_product, SUM(New_quantity) AS Total_product
            ORDER BY Total_product DESC
            LIMIT 1  // Limit to top product
            """)
        for record in result:
            popular = record['New_product']
            
    return popular