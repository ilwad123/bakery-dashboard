// Convert avgDelivTime (HH:mm:ss) to minutes
const avgDelivTimeInMinutes1 = avgDelivTime.map(time => {
    const [hours, minutes, seconds] = time.split(":").map(Number);
    return (hours * 60) + minutes + (seconds / 60); // Don't round here yet
});

// Calculate the average
const getAverage = (avgDelivTimeInMinutes1) =>
    ((avgDelivTimeInMinutes1.reduce((sum, currentValue) => sum + currentValue, 0)) / avgDelivTimeInMinutes1.length).toFixed(2); // Round after calculating the average

const avgDeliveryTime1 = getAverage(avgDelivTimeInMinutes1);

console.log(avgDeliveryTime1); 
document.getElementById('AverageDelivery').textContent = avgDeliveryTime1;

