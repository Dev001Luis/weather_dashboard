function renderForecastChart(forecastData) {
  const ctx = document.getElementById('forecastChart').getContext('2d');
  
  const labels = forecastData.map(item => item.date);
  const temps = forecastData.map(item => item.temp);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Temperature',
        data: temps,
        borderWidth: 2,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.3,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      }
    }
  });
}
