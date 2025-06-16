
//CREATE A PERFORMANCE NODE
LOAD CSV WITH HEADERS FROM "file:///performance.csv" AS csv
CREATE (p:Performance {
    Driver_id: toInteger(csv.Driver_id),
    performance_id: csv.performance_id,
    total_sales: toFloat(csv.total_sales),
    total_distance: toFloat(csv.total_distance)
})
RETURN "Performance Nodes Created"

//CREATE RELATIONSHIP BETWEEN DRIVER AND PERFORMANCE
MATCH (d:Driver), (p:Performance)
WHERE d.Driver_id = p.Driver_id
MERGE (d)-[:HAS_PERFORMANCE]->(p)
RETURN d, p

