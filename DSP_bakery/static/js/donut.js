document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    const donutCtx = document.getElementById('donut').getContext('2d');
    console.log('donutCtx:', donutCtx);

    new Chart(donutCtx, {
        type: 'doughnut',
        data: {
            labels: categories,
            datasets: [{
                data: quantities,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.4)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Total Sales per Product'
                }
            }
        }
    });
});