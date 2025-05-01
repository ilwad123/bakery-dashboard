window.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }

    
    const isDarkMode = document.body.classList.contains('dark-mode');
    const text = isDarkMode ? 'white' : '#333';
    const grid = isDarkMode ? 'rgba(255,255,255,0.2)' : '#ccc';
    
    const barCtx = document.getElementById('bar').getContext('2d'); 
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: neighborhoods,
            datasets: [{
                label: 'Sales by Neighborhood',
                data: neighborhoodSales,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(199, 199, 199, 0.5)',
                    'rgba(83, 102, 255, 0.5)',
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',

                ],

                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)',
                    'rgba(83, 102, 255, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',

                ],


                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { size: 12 },
                        color: text
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: text,
                        font: { size: 11 }
                    },
                    grid: { color: grid, lineWidth: 0.5 },
                },
                y: {
                    ticks: {
                        color: text,
                        font: { size: 13 }
                    },
                    grid: {color: grid, lineWidth: 0.5},
                }
            }
        }
    }); 
});

// const isDark = localStorage.getItem('theme') === 'dark';
// if (isDark) {
//     document.body.classList.add('dark-mode');  

//     const text = isDarkMode ? 'white' : '#333';
//     const grid = isDarkMode ? 'rgba(255,255,255,0.2)' : '#ccc';
//     barChart.options.scales.x.grid.color = grid;
//     barChart.options.scales.x.grid.lineWidth = 0.5;
//     barChart.options.scales.y.grid.color = grid;
//     barChart.options.scales.y.grid.lineWidth = 0.5;
//     barChart.options.plugins.title.color = text;
//     barChart.options.scales.x.ticks.color = text;
//     barChart.options.scales.y.ticks.color = text;
//     barChart.options.scales.x.title.color = text;
//     barChart.options.scales.y.title.color = text;
//     barChart.update();
// }
