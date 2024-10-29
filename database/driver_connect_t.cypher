MATCH (t:Transaction), (d:Driver)//connect nodes
WHERE t.driver_id= d:Driver_id //driver_id from transaction and driver_id from driver 
MERGE (t)-[:DELIVERED_TO]->(n) //make the relationship