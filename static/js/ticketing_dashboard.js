// === User Profile Dropdown Toggle ===
const userProfile = document.getElementById('userProfile');
if (userProfile) {
  userProfile.addEventListener('click', function (event) {
    this.classList.toggle('active');
    event.stopPropagation();
  });

  window.addEventListener('click', function (event) {
    if (!userProfile.contains(event.target)) {
      userProfile.classList.remove('active');
    }
  });
}

// === Sidebar Submenu Toggles ===
const masterDataToggle = document.getElementById('masterDataToggle');
if (masterDataToggle) {
  masterDataToggle.addEventListener('click', function (event) {
    event.preventDefault();
    this.classList.toggle('expanded');
  });
}

const reportsToggle = document.getElementById('reportsToggle');
if (reportsToggle) {
  reportsToggle.addEventListener('click', function (event) {
    event.preventDefault();
    this.classList.toggle('expanded');
  });
}

// === Hamburger menu toggle ===
const hamburger = document.getElementById('hamburger');
const sidebar = document.getElementById('sidebar');
if (hamburger && sidebar) {
  hamburger.addEventListener('click', function () {
    sidebar.classList.toggle('active');
  });

  // Close sidebar when clicking outside (mobile only)
  document.addEventListener('click', function (event) {
    if (sidebar.classList.contains('active') &&
        !sidebar.contains(event.target) &&
        !hamburger.contains(event.target)) {
      sidebar.classList.remove('active');
    }
  });
}

// Search Filter Function (targets dashboard cards)
const searchInput = document.getElementById('navbarSearchInput');

if (searchInput) {
  searchInput.addEventListener('keyup', function () {
    const query = this.value.toLowerCase().trim();
    const cards = document.querySelectorAll('.dashboard-grid .card');

    cards.forEach(card => {
      const title = card.querySelector('.card-title')?.innerText.toLowerCase();
      if (title?.includes(query)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
}


// === Chart Animation and Styling Config ===
const animationOptions = {
  animation: {
    duration: 1000,
    easing: 'easeOutQuart'
  },
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        boxWidth: 15,
        padding: 20,
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      enabled: true,
      backgroundColor: '#333',
      titleFont: { size: 13 },
      bodyFont: { size: 12 },
      padding: 10
    }
  }
};

// === Initialize Ticket Report Chart ===
const ticketReportChart = document.getElementById('ticketReportChart');
if (ticketReportChart) {
  new Chart(ticketReportChart, {
    type: 'bar',
    data: {
      labels: ['Open', 'In Progress', 'Closed'],
      datasets: [{
        label: 'Tickets',
        data: [12, 8, 5],
        backgroundColor: ['#007bff', '#ffc107', '#28a745'],
        borderRadius: 5,
        barThickness: 40
      }]
    },
    options: {
      ...animationOptions,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
          grid: { drawBorder: false }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}

// === Monthly Trend Chart ===
const monthlyTrendChart = document.getElementById('monthlyTrendChart');
if (monthlyTrendChart) {
  new Chart(monthlyTrendChart, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr'],
      datasets: [{
        label: 'Tickets',
        data: [3, 7, 4, 9],
        borderColor: '#007bff',
        backgroundColor: 'rgba(0, 123, 255, 0.1)',
        tension: 0.3,
        fill: true,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      ...animationOptions,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// === Tickets per Terminal Chart ===
const terminalChart = document.getElementById('terminalChart');
if (terminalChart) {
  new Chart(terminalChart, {
    type: 'bar',
    data: {
      labels: ['Terminal A', 'B', 'C'],
      datasets: [{
        label: 'Tickets',
        data: [5, 3, 9],
        backgroundColor: ['#6c757d', '#17a2b8', '#ffc107'],
        borderRadius: 5,
        barThickness: 35
      }]
    },
    options: {
      ...animationOptions,
      scales: {
        y: {
          beginAtZero: true
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}

// === Priority Chart (Pie) ===
const priorityChart = document.getElementById('priorityChart');
if (priorityChart) {
  new Chart(priorityChart, {
    type: 'pie',
    data: {
      labels: ['High', 'Medium', 'Low', 'Urgent'],
      datasets: [{
        data: [10, 15, 8, 2],
        backgroundColor: ['#007bff', '#ffc107', '#28a745', '#dc3545'],
        borderWidth: 1
      }]
    },
    options: animationOptions
  });
}

// === Status Chart (Pie) ===
const statusChart = document.getElementById('statusChart');
if (statusChart) {
  new Chart(statusChart, {
    type: 'pie',
    data: {
      labels: ['Open', 'Pending', 'In Progress', 'Closed'],
      datasets: [{
        data: [6, 4, 3, 5],
        backgroundColor: ['#28a745', '#ffc107', '#007bff', '#6c757d'],
        borderWidth: 1
      }]
    },
    options: animationOptions
  });
}
