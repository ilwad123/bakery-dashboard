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
#used for cache 
from django.shortcuts import render
from django.utils.cache import patch_cache_control


import pandas as pd
from datetime import date, timedelta
from datetime import datetime
#used to retrieve cnn model 
from .cnn_model import predict_from_graph_data
import pandas as pd

from neo4j.time import DateTime as Neo4jDateTime

#PDF generation imports 
import base64
import json
from io import BytesIO
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


# Set up logging
matplotlib.use('Agg')


driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))


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

def get_last_complete_business_week(today=None):
    if today is None:
        today = date.today()
        #gets the current date 


    today_weekday = today.weekday() #gets the current dayofweek as num 
    days_since_last_tuesday = (today_weekday - 1) % 7 # calculates how many days passed from tuesday=1
    last_tuesday = today - timedelta(days=days_since_last_tuesday)
    #Subtracts the number of days since the last Tuesday to get the date of the last Tuesday
    last_wednesday = last_tuesday - timedelta(days=6)
    # Subtracts 6 days from the last Tuesday to get the date of the last Wednesday
    #returns results
    return last_wednesday, last_tuesday

@login_required(login_url="/login/")
def predict_sales_page(request):
    #Fake today's date for testing when production starts with real data would remove fake_today
    fake_today = date(2024, 4, 5)
    last_wednesday, last_tuesday = get_last_complete_business_week(today=fake_today)

    with driver.session() as session:
        result = session.run("""
            MATCH (t:Transaction)
            WHERE date(t.Datetime) >= date($start_date)
              AND date(t.Datetime) <= date($end_date)
            WITH date(t.Datetime) AS day, SUM(t.Total) AS total
            RETURN day, total
            ORDER BY day
        """, start_date=str(last_wednesday), end_date=str(last_tuesday))
        #queries the start_date and end_date of the last 7 day window of wednesday and Tuesday 

        current_week_sales = [
            {"day": record["day"], "total": record["total"]}
            for record in result
        ]

        current_week_sales_total = 0 
        #loops through list of totals and increments into current sales total 
        for day_data in current_week_sales:
            current_week_sales_total += day_data["total"]

        print(current_week_sales, "week")
        print(current_week_sales_total, "total")

            
    # # gets the sales data from graph database 
    # df = sales_data_CNNLTSM()
    # #get the results from the algorithm in cnn_model.py
    # predicted_sales = predict_from_graph_data(df)
    # dates=[]
    # # Loop through the next 7 days and append to the dates list
    # for i in range(7):
    #     #would use this for present however the data i have is static 
    #     # dates.append((date.today() + timedelta(days=i)).isoformat())        
    #     last_date = df['date'].max()
    #     dates.append((last_date + timedelta(days=i+1)).isoformat())
    
    file_path = os.path.join(settings.BASE_DIR, "predicted_sales_cron_output.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            cron_data = json.load(f)
            predicted_sales = cron_data["predictions"] #get the predictions from the json 
            dates = cron_data["dates"]  #get the dates from the file 
    except Exception as e:
        predicted_sales = []
        dates = []
        print("Failed to load cron output:", e)

    return render(request, 'predicted_sales.html', {
        'predicted_sales': json.dumps(predicted_sales),
        'dates': json.dumps(dates),
        'previous_week_sales': json.dumps(current_week_sales_total)
    })

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from io import BytesIO
import base64, json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import re


@csrf_exempt  # dev‑only; add proper CSRF in prod
def predicted_sales_pdf(request):
    if request.method != "POST":
        return HttpResponse("Only POST allowed", status=405)

    try:
        data = json.loads(request.body)

        chart_image_b64 = data.get("chart_image", "").split(",", 1)[1]
        start_date      = data.get("start_date", "N/A")
        revenue         = data.get("revenue", "N/A")

        max_value       = data.get("max_value", "N/A")
        max_day         = data.get("max_day", "N/A")
        max_day_name    = data.get("max_day_name", "N/A")

        min_value       = data.get("min_value", "N/A")
        min_day         = data.get("min_day", "N/A")
        min_day_name    = data.get("min_day_name", "N/A")

        current_sales       = data.get("current_sales", "N/A")
        percentage_change   = data.get("percentage_change", "N/A") 
        kpi_message         = data.get("kpi_message", "")

        chart_bytes = base64.b64decode(chart_image_b64)
        chart_image = ImageReader(BytesIO(chart_bytes))

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        margin   = 50
        y = height - 50  

        # Title
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(margin, y, f"Predicted Sales Report (w/c {start_date})")
        y = y - 40
        
        # kpi insight message
        if kpi_message:
            box_height = 30
            box_padding = 5
            box_width = 400
            page_width = width 
            
            
            kpi_message1 = [kpi_message.replace(',','.') for x in re.findall('\d*[,.]?\d*%', kpi_message)]
            print(kpi_message1)

            x= (page_width / 2) - (box_width / 2)  # Center the box horizontally
            # Draw the box at (15, y - box_height + box_padding) so it wraps the text
            pdf.setFillColor(colors.HexColor("#F1E9C3"))
            pdf.roundRect(x , (y+12) - box_height + box_padding, box_width, box_height, 4, stroke=1, fill=1)

            pdf.setFillColor(colors.black)
            pdf.setFont("Helvetica", 12)
            pdf.drawString((x + 6) , y, kpi_message)
            y = y - (box_height + box_padding * 2)
        else:
            y = y - 20
            
        #seperator line
        pdf.setStrokeColor(colors.grey)
        pdf.setLineWidth(1)
        pdf.line(margin, y, width - margin, y)
        y = y - 30

        # KPI Section
        pdf.setFont("Helvetica-Bold", 13)
        pdf.setFillColor(colors.HexColor("#34495E"))
        pdf.drawString(margin, y, "Key Performance Indicators")
        pdf.setFillColor(colors.black)
        y = y - 25

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, y, "Predicted Revenue:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margin + 180, y, f"{revenue}")
        y = y - 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, y, "Current Week Sales:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margin + 180, y, f"£{current_sales}")
        y = y - 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, y, "Highest Sales Value:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margin + 180, y, f"£{max_value}")
        y = y - 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, y, "Day of Highest Sales:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margin + 180, y, f"{max_day} ({max_day_name})")
        y = y - 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, y, "Lowest Sales Value:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margin + 180, y, f"£{min_value}")
        y = y - 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, y, "Day of Lowest Sales:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margin + 180, y, f"{min_day} ({min_day_name})")
        y = y - 30


        #seperator line
        pdf.setStrokeColor(colors.grey)
        pdf.setLineWidth(1)
        pdf.line(margin, y, width - margin, y)
        y = y - 30
        

        # Chart Title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margin, y, "Sales Prediction Chart")
        y = y - 2

        # Chart Image
        chart_height = 300
        pdf.drawImage(
            chart_image,
            margin,
            y - chart_height + 20,
            # y - chart_height,
            width=width - 2 * margin,
            height=chart_height,
            preserveAspectRatio=True,
            mask='auto'
        )

        # Footer
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.setFillColor(colors.grey)
        pdf.drawString(margin, 30, "Generated by Sales Prediction System")
        pdf.drawRightString(width - margin, 30, f"Page {pdf.getPageNumber()}")

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type="application/pdf")

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {e}", status=500)

    
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
    print("Login view hit")

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
    
def driver_info(request):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Driver)
            RETURN d.Driver_id AS driver_id,
                    d.Driver_name AS name,                 
                   d.total_deliveries AS total_deliveries,
                   d.avgDelivTime AS avgDelivTime
        """)

        driver_id = []
        total_deliveries = []
        avgDelivTime = []
        all_drivers = []

        # Iterate through the result and process each record
        for record in result:
            driver_id.append(record["driver_id"])
            total_deliveries.append(record["total_deliveries"])

            # Check if avgDelivTime exists and is not None
            if record["avgDelivTime"] is not None:
                # Extract hour, minute, and second from the Neo4j time object
                time_obj = record["avgDelivTime"]
                normal_time = f"{time_obj.hour:02}:{time_obj.minute:02}:{time_obj.second:02}"
            else:
                normal_time = "00:00:00"  # Default value if there's no time data

            avgDelivTime.append(normal_time)
        
            driver_data = {
                "driver_id": record["driver_id"],
                "name": record["name"],
                "total_deliveries": record["total_deliveries"],
                "avgDelivTime": normal_time
            }
            all_drivers.append(driver_data)

        # Find top driver by total deliveries
        if all_drivers:
            top_driver = max(all_drivers, key=lambda d: d["total_deliveries"])
            top_driver["rank"] = 1
        else:
            top_driver = None
            
        # Debug print to check the data
        print(driver_id)
        print(total_deliveries)
        print(avgDelivTime)

    return driver_id, total_deliveries, avgDelivTime,top_driver


def performance_each_driver(request):
    ## Get the performance data for each driver
    with driver.session() as session:
        result = session.run("""
           MATCH (p:Performance)
           RETURN p.Driver_id AS driver_id,
                  p.performance_id AS performance_id,
                  p.total_sales AS total_sales,
                  p.total_distance AS total_distance
        """)
        # Initialise empty lists to store the values
        driver_id = []
        performance_id = []
        total_sales=[]
        total_distance=[]
        sales_per_km=[]
        for record in result:
            driver_id.append(record["driver_id"])
            performance_id.append(record["performance_id"])
            total_sales.append(record["total_sales"])
            total_distance.append(record["total_distance"])
            sales_per_km.append(round(record["total_sales"] / record["total_distance"], 2))
        print(driver_id)  
        print(performance_id)
        print(total_sales)
        print(total_distance)
        print(sales_per_km)
        # return the values to be used in the performance page
    return driver_id, performance_id, total_sales, total_distance, sales_per_km

def total_sales_from_the_last_quarter(request):
    # Get the total sales for the last 3 months
    with driver.session() as session:
        result = session.run("""
            // Matches the transaction node
            MATCH (t:Transaction)
            // Converts the datetime so it can be readable 
            //sums the total sales for the last 3 months
            WITH datetime({ year: t.Datetime.year, month: t.Datetime.month, day: 1 }) AS month, 
                 SUM(t.Total) AS monthly_sales
            RETURN month, monthly_sales
            ORDER BY month DESC
            LIMIT 3
        """)

        #initialise the variable to store the sales
        quarter_sales = 0.0
        # Loop through the result and sum the monthly sales
        for record in result:
            sales = record["monthly_sales"]
            if sales is not None:
                quarter_sales += sales

        print("Quarter sales (sum of last 3 months):", quarter_sales)
    return quarter_sales

def previous_quarter_sales(request):
    # Get the total sales for the previous quarter (3 months before the last quarter)
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Transaction)
            WITH datetime({ year: t.Datetime.year, month: t.Datetime.month, day: 1 }) AS month, 
                 SUM(t.Total) AS monthly_sales
            RETURN month, monthly_sales
            ORDER BY month DESC
            SKIP 3
            LIMIT 3
        """)

        #initialise the variable to store the sales
        previous_quarter_sales1 = 0.0
        # Loop through the result and sum the monthly sales
        for record in result:
            sales = record["monthly_sales"]
            if sales is not None:
                previous_quarter_sales1 += sales

        print("Quarter sales (previous_quarter):", previous_quarter_sales1)
    return previous_quarter_sales1

@login_required(login_url="/login/")
def performance_page(request):
    # Get the performance data for each driver
    driver_id, performance_id, total_sales, total_distance, sales_per_km = performance_each_driver(request)
    quarter_sales = total_sales_from_the_last_quarter(request)
    # Get the driver info
    driver_id, total_deliveries, avgDelivTime,top_driver = driver_info(request)
    previous_quarter_sales1 = previous_quarter_sales(request)
    context = {
        'driver_id': json.dumps(driver_id),
        'sales_per_km': json.dumps(sales_per_km),
        'performance_id': json.dumps(performance_id),
        'total_sales': json.dumps(total_sales),
        'total_distance': json.dumps(total_distance),
        'quarter_sales': json.dumps(quarter_sales),
        'total_deliveries': json.dumps(total_deliveries),
        'avgDelivTime': json.dumps(avgDelivTime),
        'previous_quarter_sales': json.dumps(previous_quarter_sales1),
        'top_driver': top_driver,

        # 'timestamp': int(datetime.now().timestamp())
        #COULD ADD THIS AT THE TOP OF THE PAGE TO SHOW IT HAS BEEN UPDATED
    }   

    return render(request, 'performance.html', context)
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
    # Get the sales data for specific holidays
    # This query will get the sales data for the specified holidays
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

#test run to see if the neo4j connection works
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