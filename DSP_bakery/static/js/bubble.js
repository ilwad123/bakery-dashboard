
// Convert the time (HH:mm:ss) into total minutes
const avgDelivTimeInMinutes = avgDelivTime.map(time => {
    const [hours, minutes, seconds] = time.split(":").map(Number);
    return ((hours * 60) + minutes + (seconds / 60)).toFixed(2);
    //round to 2 decimal places

});
console.log(avgDelivTimeInMinutes); // Check the converted values


const scatterChartCtx = document.getElementById('scatterChart').getContext('2d');
const scatterChart = new Chart(scatterChartCtx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Driver Performance',
            data: salesPerKmData.map((value, index) => ({
                x: value,  // Sales per KM
                y: avgDelivTimeInMinutes[index],  // Average Delivery Time
                label: driverLabels[index]  // Add label for each point
            })),
            backgroundColor: 'rgba(54, 162, 235, 0.6)', 
            borderColor: 'rgba(54, 162, 235, 1)',  
            borderWidth: 1,
            pointRadius: 6,  
        }]
    },
    options: {
        responsive: false,
        plugins: {
            title: {
                display: true,
                text: 'Driver Efficiency vs. Average Delivery Time',
                font: { size: 18 }
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        const dataIndex = tooltipItem.dataIndex;
                        const label = tooltipItem.dataset.data[dataIndex].label; // Driver label
                        const salesPerKm = tooltipItem.raw.x; // Sales per KM
                        const deliveryTime = tooltipItem.raw.y; // Average Delivery Time
                        return 'Driver ID' + label + ": " + "Sales per KM = " + salesPerKm + ", Delivery Time = " + deliveryTime;
                    }
                }
            },
            legend: { display: false }
        },
        scales: {
            x: {
                title: { display: true, text: 'Sales per KM' },
                min: 0,
                max: 5
            },
            y: {
                title: { display: true, text: 'Average Delivery Time (minutes)' },
                min: 0,
                max: 70
            }
        }
    }
});
