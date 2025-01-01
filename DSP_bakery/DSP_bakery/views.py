from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from neo4j import GraphDatabase
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime
import json


driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

def home(request):
    months, sales = line_graph(request)
    neighbourhood,total_neighborhood_sales=bar_graph(request)
    products_sales=most_popular(request)
    categories,quantities=popular_category(request)
    context = {
        'months': json.dumps(months),
        'sales': json.dumps(sales),
        'products_sales': products_sales,
        'neighbourhood': json.dumps(neighbourhood),
        'total_neighborhood_sales': json.dumps(total_neighborhood_sales),
        'categories': json.dumps(categories),
        'quantities': json.dumps(quantities),
    }
  
    return render(request, 'bakery.html', context)

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
        print(node)

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
            print(record)
            dt = record["month"]
            months.append(dt.strftime("%b %Y"))
            sales.append(round(record["monthly_sales"], 2))

        print("Months:", months)
        print("Sales:", sales)
    
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
            print(record)
            neighbourhood.append(record['Place'])
            total_neighborhood_sales.append(record["total_neighborhood_sales"])
            
        
        print("Neighbourhood:",neighbourhood)

    return neighbourhood, total_neighborhood_sales

def most_popular(request):
    with driver.session() as session:
        most_popular = session.run("""
                MATCH (t:Transaction)
                UNWIND t.Product_Names AS Product
                UNWIND t.Quantity_Per_Product AS Quantity 
                WITH TRIM(Product) AS New_product, TOFLOAT(TRIM(Quantity)) AS New_quantity
                WHERE New_quantity IS NOT NULL  // Filter out NULL quantities
                RETURN New_product, SUM(New_quantity) AS Total_product
                ORDER BY Total_product DESC
            """)
        
        products_sales = [(record['New_product'], record["Total_product"]) for record in most_popular]
        
        per_page = 5  
        page_number = request.GET.get('page', 1)  
        paginator = Paginator(products_sales, per_page)  
        paginated_products = paginator.get_page(page_number)  
    
    return paginated_products

def popular_category(request):
    with driver.session() as session:
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
                print(record)
                categories.append(record['Category'])
                quantities.append(record["Total_quantity"])

    return categories,quantities