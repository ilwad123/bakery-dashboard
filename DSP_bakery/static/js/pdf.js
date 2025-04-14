const generatePdfUrl = "{% url 'generate_pdf' %}";

    document.querySelector('.download_pdf').addEventListener('click', function() {
        const chartCanvas = document.getElementById('predictionChart');
        const chartImage = chartCanvas.toDataURL('image/png');  // Capture chart as base64 image

        // Send chart image data to the server (Django view)
        fetch(generatePdfUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chart_image: chartImage,  // Pass the chart image to the view
                revenue: document.getElementById("sum").textContent  // Pass the revenue data
            })
        })
        .then(response => response.blob())
        .then(data => {
            // Create a download link and trigger the download
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sales_report.pdf';
            a.click();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });