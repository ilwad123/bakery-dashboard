document.addEventListener('DOMContentLoaded', () => {
    const currentSales1 = sales[sales.length - 1];
    const previousSales1 = sales[sales.length - 2];

    // const percentchange= ((currentSales1 - previousSales1) / previousSales1 * 100).toFixed(2);
    // const percentElement = document.getElementById('percent1');
    // percentElement.textContent = percentchange + "% from last week";
    
    const currentSalesElement = document.getElementById('currentSales1');
    currentSalesElement.textContent = currentSales1.toFixed(2); 
    const graphLine = document.getElementById('graphLine');
    const graphGlow = document.getElementById('graphGlow');

    
  
    if (currentSales1 > previousSales1) {
        // Line graph goes up
        graphLine.setAttribute('points', '0,40 20,30 40,20 60,15 80,10 100,5');
        graphGlow.setAttribute('points', '0,40 20,30 40,20 60,15 80,10 100,5 100,50 0,50');
        const arrowup1 = document.getElementById("arrow1");
        arrowup1.innerText = "▲";
        arrowup1.style.color = "green";
    } else if (currentSales1 < previousSales1) {
        // Line graph goes down
        graphLine.setAttribute('points', '0,40 20,50 40,45 60,35 80,30 100,40');
        graphGlow.setAttribute('points', '0,40 20,50 40,45 60,35 80,30 100,40 100,50 0,50');
        const arrowdown1 = document.getElementById("arrow1");
        arrowdown1.innerText = "🔻";
        arrowdown1.style.color = "red";
    } else {
        // Line graph remains flat
        graphLine.setAttribute('points', '0,40 20,40 40,40 60,40 80,40 100,40');
        graphGlow.setAttribute('points', '0,40 20,40 40,40 60,40 80,40 100,40 100,50 0,50');
    }
});
