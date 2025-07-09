// Toggle hamburger menu for responsive navbar
document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger');
  const userProfile = document.getElementById('userProfile');

  if (hamburger && userProfile) {
    hamburger.addEventListener('click', () => {
      userProfile.classList.toggle('show-dropdown');
    });

    // Close dropdown when clicking outside
    window.addEventListener('click', function (event) {
      if (!userProfile.contains(event.target) && !hamburger.contains(event.target)) {
        userProfile.classList.remove('show-dropdown');
      }
    });
  }
});

function filterTable() {
  const input = document.getElementById("searchInput");
  const filter = input.value.toLowerCase();
  const table = document.querySelector("table"); 
  if (!table) return;

  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    const rowText = rows[i].innerText.toLowerCase();
    rows[i].style.display = rowText.includes(filter) ? "" : "none";
  }
}

function openProfileModal(event) {
  event.preventDefault();
  alert("Profile modal coming soon.");
}
