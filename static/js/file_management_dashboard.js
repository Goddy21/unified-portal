    // Toggle user profile dropdown
document.getElementById('userProfile').addEventListener('click', function() {
    this.classList.toggle('active');
});

// Close dropdown if clicked outside
window.addEventListener('click', function(event) {
    if (!event.target.closest('#userProfile')) {
        const userProfile = document.getElementById('userProfile');
        if (userProfile.classList.contains('active')) {
            userProfile.classList.remove('active');
        }
    }
});