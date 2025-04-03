from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from neo4j import GraphDatabase
import os
from django import forms
from captcha.fields import CaptchaField
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
from django.shortcuts import render
from django.utils.cache import patch_cache_control

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import date, timedelta

from .cnn_model import predict_from_graph_data
import pandas as pd
import datetime
from datetime import datetime


# Set up logging

matplotlib.use('Agg')


driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

from neo4j.time import DateTime as Neo4jDateTime

from .cnn_model import predict_from_graph_data
import pandas as pd
from datetime import datetime
from datetime import date, timedelta

def get_previous_weeks_per_total(request):
    # gets the sales data from graph database of the last 7 days 
    #just return each days total sales
    #don't use native just return the date as a string
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Transaction)
            WHERE date(t.Datetime) >= date() - duration({ days: 7 })
            WITH date(t.Datetime) AS day, SUM(t.Total) AS total
            RETURN day, total
            ORDER BY day DESC
        """)
        previous_week_sales = []
        for record in result:
            previous_week_sales = record["total"]

        return json.dump(previous_week_sales)
    
        
def sales_data_CNNLTSM():
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Transaction)
            WITH date(t.Datetime) AS day, SUM(t.Total) AS total
            RETURN day, total
            ORDER BY day
        """)
        records = []
        for record in result:
            records.append({
                "date": record["day"].to_native(),
                "total": record["total"]
            })
        return pd.DataFrame(records)


def predict_sales_page(request):
    # gets the sales data from graph database 
    df = sales_data_CNNLTSM()
    #get the results from the algorithm in cnn_model.py
    predicted_sales = predict_from_graph_data(df)
    dates=[]
    # Loop through the next 7 days and append to the dates list
    for i in range(7):
        #would use this for present however the data i have is static 
        # dates.append((date.today() + timedelta(days=i)).isoformat())        
        last_date = df['date'].max()
        dates.append((last_date + timedelta(days=i+1)).isoformat())

    return render(request, 'predicted_sales.html', {
        'predicted_sales': json.dumps(predicted_sales.tolist()),  # Convert to JSON
        'dates': json.dumps(dates)
    })

    
@login_required(login_url="/login/")
def home(request):
    months, sales = line_graph(request)
    neighbourhood, total_neighborhood_sales = bar_graph(request)
    products_sales = most_popular(request)
    categories, quantities = popular_category(request)
    num_of_drivers1 = num_of_drivers(request)
    num_of_transactions = num_of_transactions1(request)
    months2, num_of_transactions_monthly = num_of_transactions_monthly1(request)
    popular_product = most_popular1(request)
    heatmap_path = plot_heatmap()
    month_heatmap=plot_monthly_heatmap()
    holiday_heatmap=plot_holiday_heatmap()
    popular_asso = popular_product_association_list(request)
    # weather_data = weather_heatmap(request)

    
    
    timestamp = int(datetime.now().timestamp())

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
        'heatmap_path': heatmap_path,
        'popular_asso': popular_asso,
        'timestamp':timestamp,
        'month_heatmap':month_heatmap,
        'holiday_heatmap':holiday_heatmap,
        # 'weather_data': weather_data  # Include weather data in context

    }
    

    # PREVENTS UNAUTHORISED ACESS WHEN LOGGED OUT ALREADY 
    # Clears the browser cache for this page.
    response = render(request, 'bakery.html', context)
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)

    return response

# @login_required(login_url="/login/")
# def predicted_sales_view(request):
#     predicted_sales = get_predicted_sales()  # This returns a list of 7 values
#     context = {
#         'predicted_sales': predicted_sales
#     }
#     return render(request, 'predicted_sales.html', context)

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField() 
    
def logged_in_login(request):
    #gets the inputs from the form 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        form = CaptchaTestForm(request.POST)

        if form.is_valid():
            print(f"Attempting to authenticate user: {username}")
            #checks if user info matches
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authentication successful!")
                login(request, user)
                return redirect('home')
            else:
                print("Authentication failed!")
                return render(request, 'login.html',  {'form': form, 'error': 'Invalid username or password'})

        else:
            return render(request, 'login.html', {'form': form, 'error': "Invalid CAPTCHA. Please try again."})
    else:
        form = CaptchaTestForm()

    return render(request, 'login.html',  {'form': form})



    
def logout_view(request):
    logout(request)
    # Redirect to a login page.
    return redirect('login')
    
def login_page(request):
    return render(request,'login.html')

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

        #initilise empty lists to store the values
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

def heatmap_month_day(request):
    with driver.session() as session:
        heatmap1 = session.run("""
        MATCH (t:Transaction)
        WITH t.Datetime AS datetime, t.Total AS total_sales
        // Extract month and day of the week
        WITH datetime, total_sales,
             toInteger(date(datetime).month) AS month_sales, 
             toInteger(datetime.dayOfWeek) AS day_of_week  
        // Get total sales by month and day
        RETURN month_sales, day_of_week, SUM(total_sales) AS total_sales
        ORDER BY month_sales, day_of_week
        """)

        days_sales = []
        month_sales = []
        total_sales_month = []

        for record in heatmap1:
            days_sales.append(record['day_of_week'])
            month_sales.append(record['month_sales'])
            total_sales_month.append(record['total_sales'])

    return days_sales, month_sales, total_sales_month

def plot_monthly_heatmap():
    # Assuming the heatmap function returns day_of_week, time_of_day, and total_sales
    days_sales, month_sales, total_sales_month = heatmap_month_day(None)
    # Create a 12x7 matrix to store the sales data
    sales_matrix = np.zeros((12, 7))
    #goes through each record and assigns sales to the specific day and hour 
    for i in range(len(days_sales)):
        month = month_sales[i] - 1
        day = days_sales[i] -1 
        sales = total_sales_month[i]
        # print(f"Month: {month}, Hour: {hour}, Sales: {sales}") used for debugging
        
        sales_matrix[month, day] = sales

    # Plot the heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(sales_matrix[:,:], cmap='YlGnBu', annot=True, fmt=".2f",  
                xticklabels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                yticklabels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    plt.title('Heatmap of Sales Volume by Month and Day')
    plt.xlabel('Day of the Week (Monday to Sunday)')
    plt.ylabel('Months')
    plt.tight_layout()
    # Save the plot as an image
    filepath = "static/data_files/monthly_sales.png"
    plt.savefig(filepath)
    plt.close()
    return filepath



# def weather_heatmap(request):
#     with driver.session() as session:
#         result = session.run("""
#             MATCH (t:Transaction)
#             RETURN t.Datetime AS datetime, t.Location AS location
#         """)
        
#         data = []
#         for record in result:
#             # Assuming the 'location' is a Point and you need latitude and longitude
#             location = record['location']
#             latitude = location.latitude
#             longitude = location.longitude
#             date1 = record['datetime']  # This is your date to pass into the weather API
            
#             # Now call the weather API with the extracted parameters
#             weather_data = get_weather_api(date1, latitude, longitude)

#             # You can process the weather_data further here if needed
#             data.append({
#                 'datetime': record['datetime'],
#                 'latitude': latitude,
#                 'longitude': longitude,
#                 'weather_data': weather_data  # Store the weather data with each record
#             })

#         print(data)
#         return data

# def get_weather_api(date1,latitude,longitude):   
#     date1 = date1.strftime('%Y-%m-%d') 
#     url = 'https://api.open-meteo.com/v1/forecast'
#     cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
#     retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
#     openmeteo = openmeteo_requests.Client(session = retry_session)

#     # Make sure all required weather variables are listed here
#     # The order of variables in hourly or daily is important to assign them correctly below
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "start_date": date1,
#         "end_date": date1,
#         "hourly": "temperature_2m"
#     }
#     response = openmeteo.weather_api(url, params=params)

#     if response:
#         responses = response[0]  # The first response corresponds to the location
#         hourly = responses.Hourly()
#         hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

#         times = hourly.Time()  # This will give a list of time in seconds
#         times = pd.to_datetime(times, unit='s', utc=True)

#         # Combine the data into a dataframe or a heatmap
#         weather_dataframe = pd.DataFrame({
#             "time": times,
#             "temperature": hourly_temperature_2m
#         })
    
#     # Extract the temperature data
#         print(weather_dataframe)  # You can process or store this data as needed
        
#         return weather_dataframe
#     else:
#         print("No weather data found.")

from datetime import date

def heatmap_holiday(request):
    with driver.session() as session:
        heatmap = session.run("""
           MATCH (t:Transaction)
           WHERE (
            (date(t.Datetime).month = 12 AND date(t.Datetime).day = 23) OR // Day before Christmas Eve
            (date(t.Datetime).month = 12 AND date(t.Datetime).day = 24) OR // Christmas Eve
            (date(t.Datetime).month = 12 AND date(t.Datetime).day = 25) OR // Christmas Day
            (date(t.Datetime).month = 12 AND date(t.Datetime).day = 26) OR // Boxing Day
            (date(t.Datetime).month = 12 AND date(t.Datetime).day = 30) OR // Day before New Year's Eve
            (date(t.Datetime).month = 12 AND date(t.Datetime).day = 31) OR // New Year's Eve (kept in the query)
            (date(t.Datetime).month = 1 AND date(t.Datetime).day = 1) OR // New Year's Day
            (date(t.Datetime).month = 3 AND date(t.Datetime).day = 28) OR // Day before Good Friday
            (date(t.Datetime).month = 3 AND date(t.Datetime).day = 29) OR // Good Friday
            (date(t.Datetime).month = 3 AND date(t.Datetime).day = 30) OR // Easter Saturday
            (date(t.Datetime).month = 3 AND date(t.Datetime).day = 31) OR // Easter Sunday
            (date(t.Datetime).month = 4 AND date(t.Datetime).day = 1) OR // Easter Monday
            (date(t.Datetime).month = 2 AND date(t.Datetime).day = 13) OR // Day before Valentine's Day
            (date(t.Datetime).month = 2 AND date(t.Datetime).day = 14) OR // Valentine's Day
            (date(t.Datetime).month = 3 AND date(t.Datetime).day = 9) OR // Day before Mother's Day (UK, 2024)
            (date(t.Datetime).month = 3 AND date(t.Datetime).day = 10) OR // Mother's Day (UK, 2024)
            (date(t.Datetime).month = 6 AND date(t.Datetime).day = 15) OR // Day before Father's Day
            (date(t.Datetime).month = 6 AND date(t.Datetime).day = 16) OR // Father's Day
            (date(t.Datetime).month = 10 AND date(t.Datetime).day = 30) OR // Day before Halloween
            (date(t.Datetime).month = 10 AND date(t.Datetime).day = 31) OR // Halloween
            (date(t.Datetime).month = 11 AND date(t.Datetime).day = 1)    // Day after Halloween
        )
        WITH date(t.Datetime) AS datetime, t.Total AS total_sales
        RETURN datetime AS date, 
            SUM(total_sales) AS total_sales
        ORDER BY date(datetime);
            """)
        
        dates = []
        sales = []
        
        for record in heatmap:
            dates.append(record['date'])
            sales.append(record['total_sales'])

    return dates, sales


def plot_holiday_heatmap():
    # Get sales data from Neo4j
    dates, sales = heatmap_holiday(None)

    # Define holiday dates and names (now includes Mother's Day & Halloween)
    holiday_data = [
        # ("12-24", "Christmas Eve"), 
        ("12-25", "Christmas Day"), 
        # ("12-26", "Boxing Day"),
        ("01-01", "New Year's Day"),
        ("03-29", "Good Friday"),("03-31", "Easter Sunday"),
        ("02-14", "Valentine's Day"), ("03-10", "Mother's Day"), ("06-16", "Father's Day"),
        ("10-31", "Halloween")
    ]

    # Initialize a 2D matrix (rows: holidays, cols: Day -1, 0, +1)
    sales_matrix = np.zeros((len(holiday_data), 3))

    # Map sales data to the matrix
    for i, date_obj in enumerate(dates):
        py_date = date(date_obj.year, date_obj.month, date_obj.day)
        date_str = f"{py_date.month:02d}-{py_date.day:02d}"

        for j, (holiday_date, holiday_name) in enumerate(holiday_data):
            holiday_dt = date(py_date.year, int(holiday_date.split("-")[0]), int(holiday_date.split("-")[1]))

            if py_date == holiday_dt:  # Holiday itself (Day 0)
                sales_matrix[j, 1] = sales[i]
            elif py_date == holiday_dt - timedelta(days=1):  # Day -1
                sales_matrix[j, 0] = sales[i]
            elif py_date == holiday_dt + timedelta(days=1):  # Day +1
                sales_matrix[j, 2] = sales[i]

    print("Sales Matrix:\n", sales_matrix)

    # Generate heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(sales_matrix, annot=True, fmt=".0f", cmap='YlGnBu',
                xticklabels=['Day -1', 'Day 0', 'Day +1'], yticklabels=[name for _, name in holiday_data])

    plt.xlabel("Days Relative to Holiday")
    plt.ylabel("Holiday")
    plt.title("Sales Around Holidays (Before, During, After)")

    # Save and return filepath
    filepath = "static/data_files/holiday_heatmap.png"
    plt.savefig(filepath)
    plt.close()
    
    return filepath


def classify_heatmap(sales_matrix):
    labels = []
    for row in sales_matrix:
        before, during, after = row  # Extract Day -1, 0, +1
        if during > before or after > before:
            labels.append(1)  # Increased sales
        else:
            labels.append(0)  # No increase
    return np.array(labels)


@login_required(login_url="/login/")
def upload(request):
    return render(request,'uploadcsv.html')
@login_required(login_url="/login/")
def reports(request):
    return render(request,'reports.html')

def my_view(request):
    # Open a session to run the Neo4j query to see if it works 
    #use the print statement to see if the view is triggered
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

        #initalise empty lists to store the values
        months = []
        sales = []
        #check through the records and append the values to the lists
        for record in monthly_sales:
            dt = record["month"]
            # Format month as "Month Year" (e.g., Jan 2025)
            months.append(dt.strftime("%b %Y"))
            # Round the sales to 2 decimal places
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
        #initialise empty lists to store the values
        neighbourhood = []
        total_neighborhood_sales= []
        #check through the records and append the values to the lists
        for record in neighbourhoodsales:
            # Append the neighbourhood and total sales to the lists
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
            
            #initialise empty lists to store the values
            categories = []
            quantities= []
            #check through the records and append the values to the lists
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
        
        # Paginate the products
        #5 per page 
        per_page = 5  
        #get the page number from the request
        page_number = request.GET.get('page', 1)  
        #create a paginator object
        paginator = Paginator(products_sales, per_page)
        #get the products for the page number  
        paginated_products = paginator.get_page(page_number)  
    
    return paginated_products

def most_popular1(request):
    #just get the first product most popular
    #just return one product name
    #used to be displayed in a small card at the top of the page
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


def popular_product_association_list(request):
    print("Popular product association list view triggered!")  # Debugging line to ensure function is called
    
    with driver.session() as session:
        print("hello this works")  # Check if the function is being entered
        
        # Running the Cypher query to get product pair counts
        query = """
              MATCH (t:Transaction)
                UNWIND t.Product_Names AS Product1
                UNWIND t.Product_Names AS Product2
                WITH TRIM(Product1) AS P1, TRIM(Product2) AS P2, t.Datetime AS TransactionDate
                WHERE P1 <> P2
                WITH CASE WHEN P1 < P2 THEN P1 ELSE P2 END AS P1, 
                        CASE WHEN P1 < P2 THEN P2 ELSE P1 END AS P2, 
                        COUNT(DISTINCT TransactionDate) AS PairCount
                ORDER BY PairCount DESC
                RETURN P1 AS Product1, P2 AS Product2, PairCount AS Frequency
        """
        
        print("Running query...")
        popular2 = session.run(query)
        print("Database query executed.")

        # Convert popular2 result to a list of tuples for easier reading
        popular_asso = [(record['Product1'], record['Product2'], record['Frequency']) for record in popular2]
        
         # Paginate the products
        per_page1 = 5
        page_number1 = request.GET.get('page_associations', 1)
        paginator1 = Paginator(popular_asso, per_page1)
        paginated_products1 = paginator1.get_page(page_number1) 
        print("First few product associations:", popular_asso[:5])  # Debugging line

    # Pass paginated results to the template
    return paginated_products1