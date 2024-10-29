LOAD CSV WITH HEADERS FROM "file:///neighbourhood.csv" AS csv

Create (n:Neighbourhood{

Name:csv.Name
driver_location: point({
        latitude: toFloat(split(csv., ',')[0]),
        longitude: toFloat(split(csv.driver_location, ',')[1])
    })
})
Merge (n)-[:DELIVERED_TO]->(t)
