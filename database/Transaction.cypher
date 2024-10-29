LOAD CSV WITH HEADERS FROM "file:///sales_modified4.csv" AS csv

CREATE (t:Transaction {
    Datetime: datetime(replace(csv.datetime, " ", "T")), 
    Day_of_week: csv.`day of week`,
    Total: toFloat(csv.total),
    Place: csv.place,
    Product_Names: split(csv.product_names, ','),
    Quantity_Per_Product: split(csv.quantities_product, ','),
    Order_status: csv.`Order status`,
    Location: point({
        latitude: toFloat(split(csv.location, ',')[0]),
        longitude: toFloat(split(csv.location, ',')[1])
    }),
    Driver_id: toInteger(csv.Driver_id),
})
WITH t, split(csv.product_names, ',') AS productNames//
UNWIND productNames AS productName //
MATCH (p:Product {Name:productName})//match the
MERGE (t)-[:CONTAINS]->(p)

RETURN "Transaction and product connection successful!"
