function openTab(evt, tabName) {
  var i, tabContent, tabLinks;

  // Get all tab content elements
  tabContent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabContent.length; i++) {
    tabContent[i].style.display = "none"; // Hide all tab content
  }

  // Get all tab link elements and remove the "active" class
  tabLinks = document.getElementsByClassName("tab");
  for (i = 0; i < tabLinks.length; i++) {
    tabLinks[i].classList.remove("active");
  }

  // Show the current tab content and add the "active" class to the clicked tab
  var currentTabContent = document.getElementById(tabName);
  currentTabContent.style.display = "block";
  evt.currentTarget.classList.add("active");
}

// Show the first tab by default when the page loads
document.addEventListener("DOMContentLoaded", function() {
  var firstTab = document.getElementsByClassName("tab")[0];
  var firstTabName = firstTab.getAttribute("data-tab");
  openTab(null, firstTabName);
});
