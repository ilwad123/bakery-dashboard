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

const lineCtx = document.getElementById('line').getContext('2d');
const lineChart = new Chart(lineCtx, {
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
        scales: {
            y: { beginAtZero: true }
        }
    }
});

    // Line graph setup
    const ctx = document.getElementById('line').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: months1,
            datasets: [{
                label: 'Monthly Sales',
                data: sales1,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 13
                        }
                    }
                }
            }
        }
    });
