document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const sidebar = document.querySelector('.sidebar');
  const userProfile = document.getElementById('userProfile');

  // Toggle sidebar for mobile
  if (hamburger && sidebar) {
    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  }

  // Toggle user dropdown
  if (userProfile) {
    userProfile.addEventListener('click', () => {
      userProfile.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
      if (!userProfile.contains(e.target)) {
        userProfile.classList.remove('active');
      }
    });
  }
});

// Ticket Report (Bar)
new Chart(document.getElementById('ticketReportChart'), {
type: 'bar',
data: {
    labels: ['Open', 'In Progress', 'Closed'],
    datasets: [{
    label: 'Tickets',
    data: [12, 8, 5],
    backgroundColor: ['#007bff', '#ffc107', '#28a745']
    }]
},
options: { responsive: true }
});

// Monthly Trends (Line)
new Chart(document.getElementById('monthlyTrendChart'), {
type: 'line',
data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [{
    label: 'Tickets',
    data: [3, 7, 4, 9],
    borderColor: '#007bff',
    fill: false
    }]
},
options: { responsive: true }
});

// Terminal Chart (Bar)
new Chart(document.getElementById('terminalChart'), {
type: 'bar',
data: {
    labels: ['Terminal A', 'B', 'C'],
    datasets: [{
    label: 'Tickets',
    data: [5, 3, 9],
    backgroundColor: ['#6c757d', '#17a2b8', '#ffc107']
    }]
},
options: { responsive: true }
});

// Priority Pie
new Chart(document.getElementById('priorityChart'), {
type: 'pie',
data: {
    labels: ['High', 'Medium', 'Low', 'Urgent'],
    datasets: [{
    data: [10, 15, 8, 2],
    backgroundColor: ['#007bff', '#ffc107', '#28a745', '#dc3545']
    }]
},
options: { responsive: true }
});

// Status Pie
new Chart(document.getElementById('statusChart'), {
type: 'pie',
data: {
    labels: ['Open', 'Pending', 'In Progress', 'Closed'],
    datasets: [{
    data: [6, 4, 3, 5],
    backgroundColor: ['#28a745', '#ffc107', '#007bff', '#6c757d']
    }]
},
options: { responsive: true }
});