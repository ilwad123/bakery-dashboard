from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from neo4j import GraphDatabase
import os
from django.conf import settings
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime
import json
import pandas as pd


driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

def home(request):
    months, sales = line_graph(request)
    neighbourhood,total_neighborhood_sales=bar_graph(request)
    products_sales=most_popular(request)
    categories,quantities=popular_category(request)
    datetime1, total_sales = heatmap(request)
    num_of_drivers1 = num_of_drivers(request)
    num_of_transactions = num_of_transactions1(request)
    months2,num_of_transactions_monthly=num_of_transactions_monthly1(request)
    popular_product = most_popular1(request)  # Get the most popular product
    
    context = {
        'months': json.dumps(months),
        'sales': json.dumps(sales),
        'products_sales': products_sales,
        'neighbourhood': json.dumps(neighbourhood),
        'total_neighborhood_sales': json.dumps(total_neighborhood_sales),
        'categories': json.dumps(categories),
        'quantities': json.dumps(quantities),
        'datetime': datetime1,
        'total_sales': total_sales,
        'num_of_drivers': json.dumps(num_of_drivers1),
        'num_of_transactions': json.dumps(num_of_transactions),
        'num_of_transactions_monthly': json.dumps(num_of_transactions_monthly),
        'months2': json.dumps(months2),
        'popular_product': popular_product,
    }
    print("context")
    return render(request, 'bakery.html', context)


def create_datetime_dataframe(datetime1, total_sales):
    # Check if lists are non-empty
    if not datetime1 or not total_sales:
        print("Data lists are empty. DataFrame not created.")
        return None

    # Create a DataFrame from datetime1 and total_sales
    datetime_df = pd.DataFrame({'Datetime': datetime1, 'Total Sales': total_sales})

    # Ensure that the file path is within your project directory (e.g., in MEDIA_ROOT)
    file_path = os.path.join('datetime.csv')
    
    # Save the DataFrame to a CSV file with a proper file path
    datetime_df.to_csv(file_path, index=False)
    print(f"DataFrame saved to: {file_path}")

    return datetime_df


def login(request):
    return render(request,'login.html')

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

#heatmap should have total volume sales day and hour wise
def heatmap(request):  
    with driver.session() as session:
        heatmap = session.run("""
            MATCH (t:Transaction)
            WITH t.Datetime AS datetime, SUM(t.Total) AS total_sales
            RETURN datetime, total_sales
            ORDER BY datetime
        """)

        datetime1 = []
        total_sales = []
        for record in heatmap:
            datetime1.append(record['datetime'])
            total_sales.append(record["total_sales"])
        
    return datetime1, total_sales

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
        print("transaction")
        result = session.run("""
            MATCH (t:Transaction)
            WITH datetime({ year: t.Datetime.year, month: t.Datetime.month, day: 1 }) AS month, COUNT(t) AS num_of_transactions
            RETURN month, num_of_transactions
            ORDER BY month
        """)
        months2 = []
        num_of_transactions_monthly = []
        for record in result:
            dt = record["month"]
            months2.append(dt.strftime("%b %Y"))
            num_of_transactions_monthly.append(record["num_of_transactions"]) 
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