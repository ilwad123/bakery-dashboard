console.log("transaction.js is loaded");

// Get the this month's transactions (last entry in the array)
const thisMonthTransactions = num_of_transactions_monthly[num_of_transactions_monthly.length - 1];
console.log("This month's transactions:", thisMonthTransactions);

// Get the last month's transactions (second-to-last entry in the array)
const lastMonthTransactions = num_of_transactions_monthly[num_of_transactions_monthly.length - 2];
console.log("Last month's transactions:", lastMonthTransactions);

// Calculate the percent change between this month and last month
const percentChange = ((thisMonthTransactions - lastMonthTransactions) / lastMonthTransactions * 100).toFixed(2);

// Display the percent change in the HTML element
const percentElement = document.getElementById('percent_change');
(percentElement.textContent = `${percentChange}% change from last month`);
