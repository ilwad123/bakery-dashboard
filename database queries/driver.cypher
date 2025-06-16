LOAD CSV WITH HEADERS FROM
 "file:///driver.csv" as csv


CREATE (d:Driver {

    Driver_id: toInteger(csv.Driver_id),
    Driver_name: csv.Driver_name,
    avgDelivTime: time(csv.avgDelivTime), 
    total_deliveries: toInteger(csv.total_deliveries),
    driver_location: point({
        latitude: toFloat(split(csv.driver_location, ',')[0]),
        longitude: toFloat(split(csv.driver_location, ',')[1])
    })
     
})

MATCH (t:Transaction), (d:Driver)
WHERE t.driver_id= d:Driver_id 
MERGE (t)-[:DELIVERED_TO]->(n)

//should 
