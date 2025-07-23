$(document).ready(function() {
    console.log("Document is ready");
    console.log("Data in javascript is", data);

    // Declare chart instances outside of updateCharts function
    let dayChart, weekdayChart, hourChart, monthChart, yearChart;

    // Initialize the chart rendering with the default data
    updateCharts(data);

    // Function to destroy existing chart if it exists
    function destroyChart(chartInstance) {
        if (chartInstance) {
            chartInstance.destroy();
        }
    }

    function updateCharts(data) {
      const ctxDay = document.getElementById('ticketsPerDayChart').getContext('2d');
      const ctxWeekday = document.getElementById('ticketsPerWeekdayChart').getContext('2d');
      const ctxHour = document.getElementById('ticketsPerHourChart').getContext('2d');
      const ctxMonth = document.getElementById('ticketsPerMonthChart').getContext('2d');
      const ctxYear = document.getElementById('ticketsPerYearChart').getContext('2d');

      destroyChart(dayChart);
      destroyChart(weekdayChart);
      destroyChart(hourChart);
      destroyChart(monthChart);
      destroyChart(yearChart);

      // Per day chart
      dayChart = new Chart(ctxDay, {
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

      // Per weekday chart
      weekdayChart = new Chart(ctxWeekday, {
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

      // Per hour chart
      hourChart = new Chart(ctxHour, {
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

      // Per month chart
      monthChart = new Chart(ctxMonth, {
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

      // Per year chart
      yearChart = new Chart(ctxYear, {
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
  }

    // Populate Dropdowns
    function populateDropdown(id, items, idKey, nameKey) {
        const dropdown = document.getElementById(id);
        dropdown.innerHTML = "";
        items.forEach(item => {
            const opt = document.createElement("option");
            opt.value = item[idKey];
            opt.text = item[nameKey];
            dropdown.appendChild(opt);
        });
    }

    // Apply the initial data
    populateDropdown("customer-filter", data.customers, "id", "name");
    populateDropdown("region-filter", data.regions, "id", "name");
    populateDropdown("terminal-filter", data.terminals, "id", "cdm_name");

    // Handle filter changes and update charts dynamically
    $('#time-period, #customer-filter, #terminal-filter, #region-filter').change(function() {
        console.log("Filter changed");
        const timePeriod = $('#time-period').val();
        const customer = $('#customer-filter').val();
        const terminal = $('#terminal-filter').val();
        const region = $('#region-filter').val();

        $.ajax({
            url: '/statistics/',
            type: 'GET',
            data: {
                'time-period': timePeriod,
                'customer': customer,
                'terminal': terminal,
                'region': region,
            },
            success: function(response) {
                console.log("Server response:", response);
                if (response) {
                    try {
                        // No need to parse if response is already a valid object
                        console.log("New Data:", response); 
                        updateCharts(response); // Directly use the response object
                    } catch (error) {
                        console.error("Error while updating charts:", error);
                    }
                } else {
                    console.error("No data received from server.");
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
            }
        });
    });
});
