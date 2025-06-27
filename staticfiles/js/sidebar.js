function toggleSidebar() {
const sidebar = document.getElementById("sidebar");
const overlay = document.querySelector(".sidebar-overlay");
sidebar.classList.toggle("active");
overlay.classList.toggle("active");
}

document.querySelectorAll(".has-submenu > a").forEach(link => {
link.addEventListener("click", function (e) {
    e.preventDefault();
    this.parentElement.classList.toggle("expanded");
});
});

