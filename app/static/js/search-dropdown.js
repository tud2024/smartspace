document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchDropdown = document.getElementById("search-dropdown");

    // When the user types in the input field, show the dropdown
    searchInput.addEventListener("input", function () {
        if (searchDropdown) {
            searchDropdown.style.display = "block";
        }
    });

    // Hide the dropdown if the user clicks outside the input field or the dropdown
    document.addEventListener("click", function (event) {
        if (!searchInput.contains(event.target) && !searchDropdown.contains(event.target)) {
            if (searchDropdown) {
                searchDropdown.style.display = "none";
            }
        }
    });
});
