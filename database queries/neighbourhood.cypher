LOAD CSV WITH HEADERS FROM "file:///neighbourhood.csv" AS csv

CREATE (n:Neighbourhood {
    Name: csv.Neighborhood,
    driver_location: point({
        latitude: toFloat(split(csv.Coordinates, ',')[0]), 
        longitude: toFloat(split(csv.Coordinates, ',')[1]) 
    })
})


MERGE (n)-[:DELIVERED_TO]->(t)
