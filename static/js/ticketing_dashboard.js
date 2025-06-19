// User Profile Dropdown Toggle
document.getElementById('userProfile').addEventListener('click', function(event) {
    this.classList.toggle('active');
    event.stopPropagation(); 
});

// Close dropdown if clicked outside
window.addEventListener('click', function(event) {
    const userProfile = document.getElementById('userProfile');
    if (!userProfile.contains(event.target)) {
        userProfile.classList.remove('active');
    }
});

// Sidebar Submenu Toggle
document.getElementById('masterDataToggle').addEventListener('click', function(event) {
    event.preventDefault(); 
    this.classList.toggle('expanded');
});

document.getElementById('reportsToggle').addEventListener('click', function(event) {
    event.preventDefault(); 
    this.classList.toggle('expanded');
});

// Hamburger menu for mobile sidebar toggle
document.getElementById('hamburger').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('active');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');

    if (sidebar.classList.contains('active') && !sidebar.contains(event.target) && !hamburger.contains(event.target)) {
        sidebar.classList.remove('active');
    }
});