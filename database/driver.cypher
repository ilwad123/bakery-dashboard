LOAD CSV WITH HEADERS FROM
 "file:///driver.csv" as csv


CREATE (d:Driver {

    Driver_id: toInteger(csv.Driver_id),
    Driver_name: csv.Driver_name,
    avgDelivTime: time(csv.avgDelivTime),//double check how to do split the time 
    total_deliveries: toInteger(csv.total_deliveries),
    driver_location: point({
        latitude: toFloat(split(csv.driver_location, ',')[0]),
        longitude: toFloat(split(csv.driver_location, ',')[1])
    })
      //example:"37.88312583086898, 127.73614140725172"
})

MERGE (d)-[:Delivers]->(t)


