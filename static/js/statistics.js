$(document).ready(function() {
    console.log("Data is",data); 
  // Initialize charts with the data
  const ctxDay = document.getElementById('ticketsPerDayChart').getContext('2d');
  const ctxWeekday = document.getElementById('ticketsPerWeekdayChart').getContext('2d');
  const ctxHour = document.getElementById('ticketsPerHourChart').getContext('2d');
  const ctxMonth = document.getElementById('ticketsPerMonthChart').getContext('2d');
  const ctxYear = document.getElementById('ticketsPerYearChart').getContext('2d');

  // Tickets per Day Chart
  new Chart(ctxDay, {
    type: 'bar',
    data: {
      labels: data.days,
      datasets: [{
        label: 'Tickets per Day',
        data: data.ticketsPerDay,
        backgroundColor: '#007bff',
      }]
    }
  });

  // Tickets per Weekday Chart
  new Chart(ctxWeekday, {
    type: 'bar',
    data: {
      labels: data.weekdays,
      datasets: [{
        label: 'Tickets per Weekday',
        data: data.ticketsPerWeekday,
        backgroundColor: '#28a745',
      }]
    }
  });

  // Tickets per Hour Chart
  new Chart(ctxHour, {
    type: 'bar',
    data: {
      labels: data.hours,
      datasets: [{
        label: 'Tickets per Hour',
        data: data.ticketsPerHour,
        backgroundColor: '#ffc107',
      }]
    }
  });

  // Tickets per Month Chart
  new Chart(ctxMonth, {
    type: 'bar',
    data: {
      labels: data.months,
      datasets: [{
        label: 'Tickets per Month',
        data: data.ticketsPerMonth,
        backgroundColor: '#dc3545',
      }]
    }
  });

  // Tickets per Year Chart
  new Chart(ctxYear, {
    type: 'bar',
    data: {
      labels: data.years,
      datasets: [{
        label: 'Tickets per Year',
        data: data.ticketsPerYear,
        backgroundColor: '#17a2b8',
      }]
    }
  });
});
