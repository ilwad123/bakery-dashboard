 LOAD CSV WITH HEADERS FROM
 "file:///product_modified2.csv" as csv
MERGE (c:Category{Category:csv.Category})
MERGE (p:Product {Name: csv.Name,Price:toInt(csv.price)})
MERGE (p) - [:BELONGS_TO] ->(c)
RETURN "Import Successful!"

