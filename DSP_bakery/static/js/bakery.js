//object.keys useful for:
//make a page for dashboard of current data
//make a link to upload csv adding it in
//make a link to change prices of the menu items or delete?? what not (maybe)
//make a page for predictive trends and then a button to export pdf 
// convert the charts into pdf image to be used for export 
// add filters for realtime data and yearly
//make seperate js for machine learning charts for predictive trends.. like what would be the mos popular 
//trends in popularity 
//from that maybe prices would need to be changed 
//find what would be bought together ->this could be used to promote other combos or promote this one 
//different products over time category line charts 
//

document.addEventListener('DOMContentLoaded', async function () {
    const salesCSV = "/static/data_files/sales_modified.csv";
    const pricesCSV = "/static/data_files/product_modified.csv";

    const fetchData = async () => {
        try {
            const response = await fetch(salesCSV);
            const response2 = await fetch(pricesCSV);
            if (!response.ok || !response2.ok) {
                throw new Error('Network response was not ok');
            }
            const csvData = await response.text();
            const csvData2 = await response2.text();
            processCSVData(csvData, csvData2);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };
    
    const processCSVData = (csvData, csvData2) => {
        let salesread, pricesread;

        // Use PapaParse to parse the sales CSV data.
        Papa.parse(csvData, {
            header: true,
            skipEmptyLines: true,
            complete: function (results) {
                salesread = results.data;
                salesread = results.data.map(row => {
                    row.month = convertToMonth(row.datetime);
                    return row;
                });
            
                if (pricesread) {
                    calculateTotalSales(salesread, pricesread);
                    calculateMonthlySales(salesread);// Calculate monthly sales
                    calculateProfitPerPlace(salesread);
                }
            }
        });

        // Use PapaParse to parse the prices CSV data.
        Papa.parse(csvData2, {
            header: true,
            skipEmptyLines: true,
            complete: function (results) {
                pricesread = results.data;
                if (salesread) {
                    calculateTotalSales(salesread, pricesread);
                    calculateMonthlySales(salesread);  // Calculate monthly sales
                    calculateProfitPerPlace(salesread);//calculate profit per place
                }
            }
        });
    };

    const convertToMonth = (datetime) => {
        const date = new Date(datetime);
        return date.toLocaleString('default', { month: 'long', year: 'numeric' });
    };


    const calculateTotalSales = (salesData, pricesData) => {
        // Create a dictionary to store product prices
        const productPrices = {};
        pricesData.forEach(item => {
            productPrices[item.Name] = parseInt(item.price, 10);
        });

        // Initialise a dictionary to store total sales per product
        const totalSalesPerProduct = {};

        // Go over sales data line by line => total sales for each product
        salesData.forEach(row => {
            //object.keys used to iterate over productprices
            Object.keys(productPrices).forEach(product => {
                const quantity = parseInt(row[product], 10);
                // quantity is not a number
                if (!isNaN(quantity)) {
                    if (!totalSalesPerProduct[product]) {
                        totalSalesPerProduct[product] = 0;
                    }
                    totalSalesPerProduct[product] += quantity * productPrices[product];
                }
            });
        });

        const labels = pricesData.map(item => item.Name);  // Get labels from pricesData (pricecsv)
        const data = labels.map(label => totalSalesPerProduct[label] || 0);  // Get data in the same order as labels

        // Create Donut Chart
        const ctx = document.getElementById('donut').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.4)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(199, 199, 199, 0.2)',
                        'rgba(83, 102, 255, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(199, 199, 199, 0.2)',
                        'rgba(83, 102, 255, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(199, 199, 199, 0.2)'
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
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)',
                        'rgba(83, 102, 255, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)'
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
    };

    const calculateMonthlySales = (salesData) => {
        const monthlySales = {};
        //create a dictionary for monthlysales

        // go over sales data to compute total sales for each month
        salesData.forEach(row => {
            const month = row.month;//finds the month 
            const total = parseInt(row.total, 10);//finds total column
            if (!isNaN(total)) {
                if (!monthlySales[month]) {
                    monthlySales[month] = 0;
                }
                monthlySales[month] += total;
                //month would be the array so like january 
                //add on whatever the total is found each time 
                //for each transaction
            }
        });


        const labels = Object.keys(monthlySales);
        ///returns the array which would be the month 
        const data = Object.values(monthlySales);
        //returns the array which would be total corresponding to the month
        const currentSales = data[data.length - 1];
        //at the last index of sales total
        const previousSales = data[data.length - 2];
        //the one before the last 
        const percent = Math.round((currentSales - previousSales) / previousSales * 100);
        //percent change 
        // responsive arrow css decrease and increase from each month 
        document.getElementById('currentSales').textContent = currentSales;
        if (currentSales > previousSales) {
            var arrowup = document.getElementById("arrow");
            arrowup.innerText = "▲";
            arrowup.style.color = "green";
        } else {
            var arrowdown = document.getElementById("arrow");
            var percentage = document.getElementById("percent");
            arrowdown.innerText = "🔻";
            arrowdown.style.fontSize = "20px";
            arrowdown.style.color = "red";
            percentage.innerText = percent;
        }

        //line graph
        const ctx = document.getElementById('line').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
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
                                size: 12 //  x-axis labels font size
                            }
                        },
                    },
                    y: {
                        ticks: {
                            font: {
                                size: 13 //  y-axis labels font size
                            }
                        },
                       
                    }
                }
            }
        });
    };

    fetchData();
});
    const calculateProfitPerPlace = (salesData) => {
        const profitPerPlace = {};  

        salesData.forEach(row => {
            const total = parseFloat(row.total); // finds the total column
            const place = row.place; // finds the place column
            if (!isNaN(total)) {
                // total is a number
                if (!profitPerPlace[place]) {
                    // if there is nothing in place make it zero 
                    profitPerPlace[place] = 0;
                }
                // else add its total to the place 
                profitPerPlace[place] += total;
            }
        });

        
        const placelabel = Object.keys(profitPerPlace);
        //returns the array which would be the places 
        const datalabel = Object.values(profitPerPlace);
        //returns the array with all the totals 
        const chart2 = document.getElementById('bar').getContext('2d');
        new Chart(chart2, {
            type: 'bar',
            data: {
                labels: placelabel,
                datasets: [{
                    data: datalabel,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.4)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(199, 199, 199, 0.2)',
                        'rgba(83, 102, 255, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132,1)',
                        'rgba(54, 162, 235,1)',
                        'rgba(255, 206, 86,1)',
                        'rgba(75, 192, 192,1)',
                        'rgba(153, 102, 255,1)',
                        'rgba(255, 159, 64,1)',
                        'rgba(199, 199, 199,1)',
                        'rgba(83, 102, 255,1)',
                        'rgba(255, 99, 132,1)',
                        'rgba(54, 162, 235,1)',
                        'rgba(255, 206, 86,1)',
                        'rgba(75, 192, 192,1)',
                        'rgba(153, 102, 255,1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                barPercentage:1.2,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 18 
                            }
                        }
                    },
                    
                },
                scales: {
                    x: {
                        ticks: {
                            font: {
                                size: 12 //  x-axis labels font size
                            }
                        },
                    },
                    y: {
                        ticks: {
                            font: {
                                size: 13 //  y-axis labels font size
                            }
                        },
                       
                    }
                }
            }
        });
        };


        fetchData();
        function getSortedProductList(pricesData, totalSalesPerProduct) {
            const labels = pricesData.map(item => item.Name); // Get labels from pricesData
            const data = labels.map(label => totalSalesPerProduct[label] || 0); // Get data in the same order as labels
        
            // Combine labels and data into an array of objects
            const combined = labels.map((label, index) => ({
                label: label,
                sales: data[index]
            }));
        
            // Sort combined array by sales in descending order
            combined.sort((a, b) => b.sales - a.sales);
        
            // Return sorted list of products and their sales
            return combined;
        }
        
        // Example usage
        const sortedProductList = getSortedProductList(pricesData, totalSalesPerProduct);
        
        // To create a list (HTML, for instance)
        const productListElement = document.createElement('ul');
        sortedProductList.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.label}: ₩${item.sales}`;
            productListElement.appendChild(listItem);
        });
        
        // Append to the document body or a specific container
        document.body.appendChild(productListElement);
        
        
    const calculateSortedTotalSales = (salesData, pricesData) => {
        // Create a dictionary to store product prices
        const productPrices = {};
        pricesData.forEach(item => {
            productPrices[item.Name] = parseInt(item.price, 10);
        });

        // Initialise a dictionary to store total sales per product
        const totalSalesPerProduct = {};

        // Go over sales data line by line => total sales for each product
        salesData.forEach(row => {
            //object.keys used to iterate over productprices
            Object.keys(productPrices).forEach(product => {
                const quantity = parseInt(row[product], 10);
                // quantity is not a number
                if (!isNaN(quantity)) {
                    if (!totalSalesPerProduct[product]) {
                        totalSalesPerProduct[product] = 0;
                    }
                    totalSalesPerProduct[product] += quantity * productPrices[product];
                }
            });
        });
    }
        //convert object to array 
        const result_array = Object.entries(totalSalesPerProduct).map(([product,total]) => {(product,total)});
        //sort the array in descending order 
        result_array.sort(((a,b) => a.total - b.total));
        console.log(result_array) ;
    // function displaylist{

    // }
    
    // const list  = document.getElementById('list');

        //start doing the drinks sales donut one for the current month
        //add a filter for different dates in the card maybe??idk
        
       