// Toggle user profile dropdown
document.getElementById('userProfile').addEventListener('click', function () {
    this.classList.toggle('active');
});

// Toggle dropdown content
document.querySelector('.profile-dropdown').addEventListener('click', function (event) {
    event.stopPropagation(); // Prevent window click from firing
    document.querySelector('.dropdown-content').classList.toggle('show');
});

// Unified window click handler
window.addEventListener('click', function (event) {
    const userProfile = document.getElementById('userProfile');
    const dropdown = document.querySelector('.dropdown-content');
    const modal = document.getElementById('profileModal');

    // Close dropdown if clicked outside
    if (!event.target.closest('#userProfile')) {
        if (userProfile.classList.contains('active')) {
            userProfile.classList.remove('active');
        }
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }

    // Close modal if clicked outside
    if (modal && event.target === modal) {
        modal.style.display = "none";
    }
});

// Open profile modal via AJAX
function openProfileModal(event) {
    event.preventDefault();
    fetch("{% url 'profile_view' %}", {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("profileModal").classList.add("show");
        document.getElementById("profileContent").innerHTML = data;
        document.getElementById("profileModal").style.display = "block";
    });
}

// Close profile modal
function closeModal() {
    document.getElementById("profileModal").style.display = "none";
}
