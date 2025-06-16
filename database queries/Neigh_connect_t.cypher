MATCH (t:Transaction), (n:Neighbourhood) //retrive the nodes data from graphs like select query 
WHERE t.Place= n.Name //Place from transaction and Name from neighbourhood nodes 
MERGE (t)-[:DELIVERED_TO]->(n) //make the relationship

// . to retrive the property 
//: to retrive the label 

