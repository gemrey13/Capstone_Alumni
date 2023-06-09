const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");
const darkModePref = localStorage.getItem('darkMode');


document.addEventListener("DOMContentLoaded", () => {
    sidebar.classList.add("close");

    if (sidebar.classList.contains("close")) {
        sidebarExpand.style.display = "block";
        sidebarClose.style.display = "none";
    } else {
        sidebarExpand.style.display = "none";
        sidebarClose.style.display = "block";
    }
});


sidebarExpand.addEventListener("click", () => {
    sidebar.classList.remove("close", "hoverable");
    sidebarExpand.style.display = "none";
    sidebarClose.style.display = "block";
});


sidebarClose.addEventListener("click", () => {
    sidebar.classList.add("close", "hoverable");
    sidebarExpand.style.display = "block";
    sidebarClose.style.display = "none";
});


sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));


if (darkModePref === 'true') {
    body.classList.add('dark');
    darkLight.classList.replace("bx-sun", "bx-moon");
}


darkLight.addEventListener("click", () => {
    body.classList.toggle("dark");
    if (body.classList.contains("dark")) {
        document.setI;
        darkLight.classList.replace("bx-sun", "bx-moon");
        localStorage.setItem('darkMode', 'true');
    } else {
        darkLight.classList.replace("bx-moon", "bx-sun");
        localStorage.setItem('darkMode', 'false');
    }
});


submenuItems.forEach((item, index) => {
    item.addEventListener("click", () => {
        item.classList.toggle("show_submenu");
        submenuItems.forEach((item2, index2) => {
            if (index !== index2) {
                item2.classList.remove("show_submenu");
            }
        });
    });
});


if (window.innerWidth < 768) {
    sidebar.classList.add("close");
} else {
    sidebar.classList.remove("close");
}