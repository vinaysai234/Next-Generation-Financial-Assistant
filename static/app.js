// app.js - Handles Income vs Expense & Category Breakdown charts dynamically
document.addEventListener('DOMContentLoaded', () => {

    // ----- Income vs Expense Chart -----
    const incomeCanvas = document.getElementById('incomeChart');
    if (incomeCanvas) {
        const income = parseFloat(incomeCanvas.dataset.income) || 0;
        const expense = parseFloat(incomeCanvas.dataset.expense) || 0;

        const ctx = incomeCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Income', 'Expense'],
                datasets: [{
                    label: 'Amount (₹)',
                    data: [income, expense],
                    backgroundColor: ['#4CAF50', '#F44336']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutBounce'
                }
            }
        });
    }

    // ----- Category Breakdown Pie Chart -----
    const categoryCanvas = document.getElementById('categoryChart');
    if (categoryCanvas) {
        const categories = [];
        const amounts = [];
        const colors = [];
        const tableRows = document.querySelectorAll('.recent-transactions tbody tr');
        const colorPalette = ['#FF6384','#36A2EB','#FFCE56','#8E44AD','#1ABC9C','#F39C12','#2ECC71','#E74C3C'];

        tableRows.forEach((row, index) => {
            const category = row.cells[3].textContent;
            const amount = parseFloat(row.cells[2].textContent.replace('₹','')) || 0;
            
            categories.push(category);
            amounts.push(amount);
            colors.push(colorPalette[index % colorPalette.length]);
        });

        const ctx2 = categoryCanvas.getContext('2d');
        new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Category Breakdown',
                    data: amounts,
                    backgroundColor: colors
                }]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1500,
                    easing: 'easeOutBounce'
                }
            }
        });
    }

});
