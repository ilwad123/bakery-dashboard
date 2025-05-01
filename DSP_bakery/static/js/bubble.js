window.addEventListener('DOMContentLoaded', function () {
    const avgDelivTimeInMinutes = avgDelivTime.map(time => {
        const [hours, minutes, seconds] = time.split(":").map(Number);
        return ((hours * 60) + minutes + (seconds / 60)).toFixed(2);
    });

    const scatterChartCtx = document.getElementById('scatterChart').getContext('2d');
    window.scatterChart = new Chart(scatterChartCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Driver Performance',
                data: salesPerKmData.map((value, index) => ({
                    x: value,
                    y: avgDelivTimeInMinutes[index],
                    label: driverLabels[index]
                })),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                pointRadius: 6
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
                        label: function (tooltipItem) {
                            const dataIndex = tooltipItem.dataIndex;
                            const label = tooltipItem.dataset.data[dataIndex].label;
                            const salesPerKm = tooltipItem.raw.x;
                            const deliveryTime = tooltipItem.raw.y;
                            return 'Driver ID ' + label + ": Sales per KM = " + salesPerKm + ", Delivery Time = " + deliveryTime;
                        }
                    }
                },
                legend: { display: false }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Sales per KM' }
                },
                y: {
                    title: { display: true, text: 'Average Delivery Time (minutes)' }
                }
            }
        }
    });

    const isDark = localStorage.getItem('theme') === 'dark';
    if (isDark) {
        document.body.classList.add('dark-mode');  

        const text = 'white';
        const grid = 'rgba(255,255,255,0.2)';

        scatterChart.options.plugins.title.color = text;
        scatterChart.options.scales.x.ticks.color = text;
        scatterChart.options.scales.y.ticks.color = text;
        scatterChart.options.scales.x.grid.color = grid;
        scatterChart.options.scales.y.grid.color = grid;
        scatterChart.options.scales.x.title.color = text;
        scatterChart.options.scales.y.title.color = text;
        scatterChart.update();
    }
});
