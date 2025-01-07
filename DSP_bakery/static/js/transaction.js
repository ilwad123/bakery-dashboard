console.log("transaction.js is loaded");

// Get this month's transactions 
const thisMonthTransactions = num_of_transactions_monthly[num_of_transactions_monthly.length - 1];
console.log("This month's transactions:", thisMonthTransactions);

// Get last month's transactions 
const lastMonthTransactions = num_of_transactions_monthly[num_of_transactions_monthly.length - 2];
const percentChange = ((thisMonthTransactions - lastMonthTransactions) / lastMonthTransactions * 100).toFixed(2);

// Display the percent change in the HTML element
const percentElement = document.getElementById('percent_change');
if (percentElement) {
    percentElement.textContent = `${percentChange}% change from last month`;

    if (thisMonthTransactions > lastMonthTransactions) {
        percentElement.style.color = "green"; // Positive change
    } else {
        percentElement.style.color = "red"; // Negative change
    }
} 
