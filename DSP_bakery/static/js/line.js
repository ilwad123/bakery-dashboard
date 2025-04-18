const currentSales = sales[sales.length - 1];
const previousSales = sales[sales.length - 2];
const percent = ((currentSales - previousSales) / previousSales * 100).toFixed(2);

const currentSalesElement1 = document.getElementById('currentSales');
currentSalesElement1.textContent = currentSales.toFixed(2); 

    if (currentSales > previousSales) {
        const arrowup = document.getElementById("arrow");
        arrowup.innerText = "▲";
        arrowup.style.color = "green";
    } 
    else {
        const arrowdown = document.getElementById("arrow");
        arrowdown.innerText = "🔻";
        arrowdown.style.color = "red";
        arrowdown.style.fontSize = "0.9em";
        document.getElementById("percent").textContent = percent + "%";
    }

    let lineChart;
        
    window.onload = function () {
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
        }
    
        const isDarkMode = document.body.classList.contains('dark-mode');
        const lineCtx = document.getElementById('line').getContext('2d');
    
        lineChart = new Chart(lineCtx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Monthly Sales',
                    data: sales,
                    borderColor:'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: isDarkMode ? 'white' : '#333'  
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: isDarkMode ? 'white' : '#333', 
                            font: { size: 12 }
                        },
                        grid: {
                            color: isDarkMode ? 'white' : '#ccc',
                            lineWidth: 0.7
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: isDarkMode ? 'white' : '#333',
                            font: { size: 13 }
                        },
                        grid: {
                            color: isDarkMode ? 'white' : '#ccc',
                            lineWidth: 0.7
                        }
                    }
                }
            }
        });
    };
    

    
    console.log('Chart.js version:', Chart.version);
