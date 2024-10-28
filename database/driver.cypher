LOAD CSV WITH HEADERS FROM
 "file:///driver.csv" as csv


CREATE (d:Driver {
    Driver_id,Driver_name,avgDelivTime,total_deliveries,driver_location

    Driver_id: toInt(csv.Driver_id),
    Driver_name: csv.Driver_name,
    avgDelivTime: time(csv.avgDelivTime),//double check how to do split the time 
        minutes:split(csv.avgDelivTime,',')
        seconds:split(csv.avgDelivTime,',')
    total_deliveries: toInt(csv.total_deliveries),
    driver_location = (
        latitude:toFloat(split(csv.driver_location,',')[0]),longtitude:toFloat(split(csv.driver_location,',')[1]))
      //example:"37.88312583086898, 127.73614140725172"
})

MATCH (t:Transaction), (d:Driver)
//randomly assign the driver to a transaction find out how 
//research yourself tommorow 
CREATE (d)-[:Delivers]->(t)
