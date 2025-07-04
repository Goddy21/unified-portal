document.addEventListener("DOMContentLoaded", function () {
  const userProfile = document.getElementById('userProfile');
  if (userProfile) {
    userProfile.addEventListener('click', function (e) {
      this.classList.toggle('active');
      e.stopPropagation();
    });

    window.addEventListener('click', function (e) {
      if (!userProfile.contains(e.target)) {
        userProfile.classList.remove('active');
      }
    });
  }

  const hamburger = document.getElementById('hamburger');
  if (hamburger) {
    hamburger.addEventListener('click', function () {
      document.getElementById('sidebar')?.classList.toggle('active');
    });
  }
});
