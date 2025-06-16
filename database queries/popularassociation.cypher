MATCH (t:Transaction)//match to the transaction node
UNWIND t.Product_Names AS Product1 //unwind the product list 
UNWIND t.Product_Names AS Product2   //unwind the product list 
WITH TRIM(Product1) AS P1, TRIM(Product2) AS P2, ID(t) AS Transaction   
//removes any whitespaces and assigns variables to them
WHERE P1 <> P2 // exclude pairs where the same product is compared with itself
WITH P1, P2, COUNT(DISTINCT Transaction) AS PairCount //counts 
ORDER BY PairCount DESC //order by highest to lowest 
RETURN P1 AS Product1, P2 AS Product2, PairCount AS Frequency
//return the product name pairs with their frequencies 
        