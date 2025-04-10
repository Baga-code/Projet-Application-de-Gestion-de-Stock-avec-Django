document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("graphiqueProduits");
  if (!canvas) return;

  const labels = JSON.parse(canvas.dataset.labels);
  const stocks = JSON.parse(canvas.dataset.stocks);
  const colors = JSON.parse(canvas.dataset.colors);

  const ctx = canvas.getContext("2d");
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Stock produit',
        data: stocks,
        backgroundColor: colors,
        borderRadius: 8,
        barThickness: 40,
        hoverBackgroundColor: 'rgba(255, 206, 86, 0.9)',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: 20
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: '#1f2937',
          titleColor: '#fff',
          bodyColor: '#fff',
          cornerRadius: 8,
          padding: 10,
          callbacks: {
            label: function(context) {
              return `Quantité en stock: ${context.raw}`;
            }
          }
        },
        title: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(200, 200, 200, 0.2)',
            borderDash: [4, 4]
          },
          ticks: {
            color: '#4B5563',
            font: {
              weight: 'bold'
            }
          },
          title: {
            display: true,
            text: 'Quantité',
            color: '#6B7280',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#4B5563',
            font: {
              weight: 'bold'
            }
          },
          title: {
            display: true,
            text: 'Produits',
            color: '#6B7280',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        }
      }
    }
  });
});
