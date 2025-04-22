
const isDarkMode= document.body.classList.contains('dark-mode');
const darkText = '#ffffff';
const lightText = '#333333';
const darkGrid = 'rgba(255,255,255,0.1)';
const lightGrid = '#cccccc';
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
                ticks: {
                    color: isDarkMode ? darkText : lightText
                },
                grid: {
                    color: isDarkMode ? darkGrid : lightGrid
                },
                title: {
                    display: true,
                    text: 'Total Deliveries',
                    color: isDarkMode ? darkText : lightText
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Driver ID',
                    color: isDarkMode ? darkText : lightText
                }
            }
        }
    }
});