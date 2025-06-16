

MATCH (t:Transaction)
UNWIND t.Product_Names AS Product
WITH trim(Product) AS New_product ,t
RETURN New_product AS Product ,COUNT(*) AS Transaction_Count
ORDER BY Transaction_Count

//trimming is needed may be due to white spaces thats why it could not calculate properly the quantity 