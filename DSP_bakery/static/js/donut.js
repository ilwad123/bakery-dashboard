const myUniqueDonutCTX = document.getElementById('donut').getContext('2d');

    const isDarkMode = document.body.classList.contains('dark-mode');
    const text = isDarkMode ? 'white' : '#333';
    donutChart = new Chart(myUniqueDonutCTX, {
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
                    labels: {
                        color: text
                    }
                },
                title: {
                    display: true,
                    text: 'Total Sales per Product',
                    color: text,
                },
                tooltip: { 
                    callbacks: {
                        label: function (tooltipItem) {
                            const dataset = this.chart.data.datasets[tooltipItem.datasetIndex];
                            //get the sum of the quantites and iterates through the array
                            //initially at zero 
                            const total = dataset.data.reduce((sum, value) => sum + value, 0);
                            const currentValue = dataset.data[tooltipItem.dataIndex];
                            const percentage = Math.floor(((currentValue / total) * 100) + 0.5);
                            return percentage + "%" + ',' + currentValue;
                        }
                    }
                }
            }
        }
    });    
    