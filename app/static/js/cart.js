
// JavaScript for quantity increment and decrement
document.querySelectorAll('.quantity').forEach(quantityElement => {
    const decrementButton = quantityElement.querySelector('.minus');
    const incrementButton = quantityElement.querySelector('.plus');
    const countDisplay = quantityElement.querySelector('.count');

    let count = parseInt(countDisplay.textContent);

    decrementButton.addEventListener('click', () => {
        if (count > 1) { // Prevent count from going below 1
            count--;
            countDisplay.textContent = count;
        }
    });

    incrementButton.addEventListener('click', () => {
        count++;
        countDisplay.textContent = count;
    });
});
// Fix variable redeclaration and ensure both elements exist before adding event listeners

document.addEventListener('DOMContentLoaded', () => {
    let bodyElement = document.querySelector('body');
    let closeCart = document.querySelector('.close');
    let basketLink = document.querySelector('a[href="/cart/basket"]');  // Target the Basket link

    // Listen for clicks on the basket link
    basketLink.addEventListener('click', (event) => {
        // Check if the link has already been clicked and cart is visible
        if (window.location.hash !== "#cart") {
            window.location.hash = "#cart";  // Change URL to indicate the cart is open
        } else {
            window.location.hash = "";  // Remove the hash, indicating the cart should be hidden
        }

        // Toggle the cart visibility
        bodyElement.classList.toggle('showCart');
    });

    // Listen for changes in the URL hash (to handle back button / page reload)
    window.addEventListener("hashchange", function() {
        if (window.location.hash === "#cart") {
            bodyElement.classList.add('showCart');  // Show cart if the hash is #cart
        } else {
            bodyElement.classList.remove('showCart');  // Hide cart if the hash is empty
        }
    });

    // Close the cart when the close button inside the cart is clicked
    closeCart.addEventListener('click', () => {
        window.location.hash = "";  // Remove the hash when closing the cart
        bodyElement.classList.remove('showCart');  // Hide the cart
    });
});








