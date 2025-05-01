window.addEventListener('DOMContentLoaded', function () {
    
    const isDark = localStorage.getItem('theme') === 'dark';
    const text = isDark ? 'white' : '#333';
    const grid = isDark ? 'rgba(255,255,255,0.2)' : '#ccc';

    
    const lineCtx = document.getElementById('barchart23').getContext('2d');
    window.barchart23 = new Chart(lineCtx, {
        type: 'bar',
        data: {
            labels: driverLabels,
            label: 'Driver ID',
            datasets: [{
                label: 'Total Deliveries per Driver',
                data: totalDeliveries,
                borderWidth: 1,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)'
            }]
        },
        options: {
            responsive: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Total Deliveries per Driver',
                    font: { size: 18 },
                    color: text
                },
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: text },
                    grid: { color: grid },
                    title: {
                        display: true,
                        text: 'Total Deliveries',
                        color: text
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Driver ID',
                        color: text
                    },
                    ticks: { color: text },
                    grid: { color: grid }
                }
            }
        }
    });
});
