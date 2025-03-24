   // JavaScript for scroll functionality
        const leftArrow = document.getElementById('leftArrow');
        const rightArrow = document.getElementById('rightArrow');
        const categoryNav = document.getElementById('categoryNav');

        // Scroll left
        leftArrow.addEventListener('click', () => {
            categoryNav.scrollBy({
                top: 0,
                left: -200, // Adjust scroll amount
                behavior: 'smooth'
            });
        });

        // Scroll right
        rightArrow.addEventListener('click', () => {
            categoryNav.scrollBy({
                top: 0,
                left: 200, // Adjust scroll amount
                behavior: 'smooth'
            });
        });