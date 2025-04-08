document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('stockChart').getContext('2d');
  
    const labels = JSON.parse(document.getElementById('stockChart').dataset.labels);
    const stocks = JSON.parse(document.getElementById('stockChart').dataset.stocks);
    const colors = JSON.parse(document.getElementById('stockChart').dataset.colors);
  
    const stockchart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Quantité en stock',
          data: stocks,
          backgroundColor: colors,
          borderColor: '#ddd',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.label}: ${context.raw} unités`;
              }
            }
          }
        }
      }
    });
  });
  