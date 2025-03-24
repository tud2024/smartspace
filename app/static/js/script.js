const cartIcon = document.querySelector("#cart-icon");
const cart = document.querySelector(".cart");
const cartClose = document.querySelector("#cart-close");

cartIcon.addEventListener("click", () => cart.classList.add("active"));
cartClose.addEventListener("click", () => cart.classList.remove("active"));

const addCartButtons = document.querySelectorAll(".add-cart");

addCartButtons.forEach(button => {
    button.addEventListener("click", event => {
        const productBox = event.target.closest(".product-box");
        addToCart(productBox);
    });
});

const cartContent = document.querySelector(".cart-content");

const addToCart = productBox => {
    const productImgSrc = productBox.querySelector("img").src;
    const productTitle = productBox.querySelector(".product-title").textContent;
    const productPrice = productBox.querySelector(".price").textContent;

    // Check if item already exists in the cart
    const cartItems = cartContent.querySelectorAll(".cart-product-title");

    for (let item of cartItems) {
        if (item.textContent === productTitle) {
            alert("Item is already in the cart");
            return;
        }
    }

    const cartBox = document.createElement("div");
    cartBox.classList.add("cart-box");

    cartBox.innerHTML = `
        <img src="${productImgSrc}" class="cart-img">
        <div class="cart-detail">
            <h2 class="cart-product-title">${productTitle}</h2>
            <span class="cart-price">${productPrice}</span>
            <div class="cart-quantity">
                <button class="decrement">-</button>
                <span class="number">1</span>
                <button class="increment">+</button>
            </div>
        </div>
        <i class="ri-delete-bin-line cart-remove"></i>
    `;

    cartContent.appendChild(cartBox);
    
    cartBox.querySelector(".cart-remove").addEventListener("click",() => {
        cartBox.remove();
        updateCartCount(-1);
        updateTotalPrice();
    });

    cartBox.querySelector(".cart-quantity").addEventListener("click", event => {
        const numberElement = cartBox.querySelector(".number");
        const decrementButton = cartBox.querySelector(".decrement");
        const incrementButton = cartBox.querySelector(".increment");
        
        console.log("Before conversion:", numberElement.textContent, typeof numberElement.textContent);
        
        let quantity = parseInt(numberElement.textContent, 10);
        
        if (event.target === decrementButton && quantity > 1) {
            quantity--;
            if (quantity === 1) {
                decrementButton.style.color = "#999";
            }
        } else if (event.target === incrementButton) {
            quantity++;
            decrementButton.style.color = "#333";
        }
        
        numberElement.textContent = quantity;
        updateTotalPrice();
    });
    updateCartCount(1);
    updateTotalPrice();

};

const updateTotalPrice = () => {
    const totalPriceElement = document.querySelector(".total-price");
    const cartBoxes = cartContent.querySelectorAll(".cart-box");
    let total = 0;
    cartBoxes.forEach(cartBox => {
        const priceElement = cartBox.querySelector(".cart-price");
        const quantityElement = cartBox.querySelector(".number");
        const price = priceElement.textContent.replace("€","");
        const quantity = quantityElement.textContent;
        total += price * quantity;
    });
    totalPriceElement.textContent = `$${total}`;
};

// Count cart item

let cartItemCount = 0;
const updateCartCount = change =>{
    const cartItemCountBadge = document.querySelector(".cart-item-count");
    cartItemCount += change;
    if (cartItemCount > 0) {
        cartItemCountBadge.style.visibility ="visible";
        cartItemCountBadge.textContent = cartItemCount;


    }else {
        cartItemCountBadge.style.visibility ="hidden";
        cartItemCountBadge.textContent = "";

    }
};

