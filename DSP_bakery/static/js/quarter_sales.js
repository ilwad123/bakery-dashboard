// Display quarter_sales with a currency symbol (£) and formatted to two decimal places
document.getElementById('quarter_sales').textContent = '£' + quarter_sales.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

// Display previous_quarter_sales with a currency symbol (£) and formatted to two decimal places
// document.getElementById('previous_quarter_sales1').textContent = '£' + previous_quarter_sales.toLocaleString(undefined, {
//     minimumFractionDigits: 2,
//     maximumFractionDigits: 2
// });

let percent_change = ((quarter_sales - previous_quarter_sales) / previous_quarter_sales) * 100;

//to show the percentage change with either a + or - sign 
if (percent_change > 0) {
    percent_change = "▲" + '+' + percent_change.toFixed(2) + '%';
} else {
    percent_change = "🔻" + percent_change.toFixed(2) + '%' + ' from the previous quarter';
}

document.getElementById('percent_change').textContent = percent_change;
