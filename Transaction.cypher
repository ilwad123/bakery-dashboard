LOAD CSV WITH HEADERS FROM
 "file:///sales_modified4.csv" as csv


CREATE (t:Transaction {
    Datetime: datetime(csv.datetime),
    Day_of_week: csv.day of week,
    Total: toFloat(csv.total),
    Place: csv.place,
    Product_Names = split(csv.product_names, ','),//convert these strings into lists
    Quantity_Per_Product = split(csv.quantities_product, ','),
    Order_status: csv.`Order status`,
    Location: csv.location
})

WITH t, split(csv.product_names, ',') AS productNames

UNWIND productNames AS productName 
MATCH (p:product {name: productNames})//connect the product node with the transaction productnames
MERGE (t) - [:CONTAINS] -> (p) //estabilish the relationship 

RETURN "Transaction and product connection successful!"

//connect with neighbourhood and driver 