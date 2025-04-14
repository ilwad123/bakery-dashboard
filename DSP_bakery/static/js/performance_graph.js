

const lineCtx = document.getElementById('barchart23').getContext('2d');
const barchart23 = new Chart(lineCtx, {
    type: 'bar',
    data: {
        labels: driverLabels,
        label: 'Driver ID',
        datasets: [{
            label: 'Total Deliveries per Driver',
            data: totalDeliveries,
            borderWidth: 1,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
        }]
    },
    options: {
        responsive: false,
        plugins: {
            title: {
                display: true,
                text: 'Total Deliveries per Driver',
                font: {
                    size: 18
                }
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Total Deliveries'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Driver ID'
                }
            }
        }
    }
});