//get the last month transactions
const last_month_transactions= num_of_transactions_monthly[num_of_transactions_monthly.length-2];
// calculate the difference between the number of the transaction 
const percent_difference= (( num_of_transactions2 - last_month_transactions) / last_month_transactions * 100).toFixed(2);
// get the element by id
const percent_Element = document.getElementById('percent_change');
percent_Element.textContent = percent_difference + "% from last month";








