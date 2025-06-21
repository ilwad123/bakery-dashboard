document.querySelector('.download_pdf').addEventListener('click', async function () {
    const chartCanvas = document.getElementById('predictionChart');
    const chartImage = chartCanvas.toDataURL('image/png');

    const revenue = document.getElementById("sum").textContent;
    const startDate = labels[0];  // From your script context

    console.log(predictedSales);
    // let max = predictedSales[0]; // initialize to the first value
    let max = Math.max(...predictedSales); // find the maximum value
    let min = Math.min(...predictedSales); // find the minimum value
    
    //get the index (position in the array)
    let maxIndex = predictedSales.indexOf(max);
    let minIndex = predictedSales.indexOf(min);
    //get the label at that index
    let maxday = labels[maxIndex];
    let minday = labels[minIndex];

    // based on the position of the labels is the day of the week 
    dayofWeek = ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday'];
    const mappedDays = labels.map((_, i) => dayofWeek[i]); //maps labels to days of the week window 

    // =findMaxIndex(predictedSales, labels);
    //map the max and min values to the labels
    
    let maxDayName = mappedDays[maxIndex];
    let minDayName = mappedDays[minIndex];

    console.log(max, maxday, maxDayName);
    console.log(min, minday, minDayName);

    const percentageChange = ((sum - currentSales) / currentSales) * 100;

    let changeType = percentageChange > 0 ? "increase" : "decrease";

    const kpiMessage = `Predicted week ${changeType}d by ${Math.abs(percentageChange).toFixed(2)}% compared to current week sales.`;

    const response = await fetch('/predicted-sales/pdf/', {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            chart_image: chartImage,
            revenue: revenue,
            start_date: startDate, 
            max_value: max.toFixed(2), 
            max_day: maxday,
            max_day_name: maxDayName,
            min_value: min.toFixed(2), 
            min_day: minday,
            min_day_name: minDayName,
            current_sales: currentSales,  // pass current sales if you want backend to verify
            percentage_change: percentageChange.toFixed(2), // pass KPI data explicitly
            kpi_message: kpiMessage  // message to display in PDF
        })
    });

    if (response.ok) {
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `Predicted_Sales_Report_w_c_${startDate}.pdf`;
        link.click();
    } else {
        alert("Failed to generate PDF");
    }
});
