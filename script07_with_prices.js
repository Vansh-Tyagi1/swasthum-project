document.addEventListener("DOMContentLoaded", () => {
    const searchBar = document.getElementById("searchBar");
    const medicines = document.querySelectorAll(".medicine");
    const cart = [];
    const cartDisplay = document.createElement("div");

    cartDisplay.id = "cart-display";
    document.body.appendChild(cartDisplay);

    cartDisplay.style = `
        position: fixed;
        top: 80px; /* Adjusted to not overlap header */
        right: 20px;
        width: 300px;
        max-height: 400px;
        overflow-y: auto;
        background-color: white;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        z-index: 1000; /* Ensure cart stays on top */
    `;

    // Render Cart
    function renderCart() {
        cartDisplay.innerHTML = "<h3>Your Cart</h3>";
        let totalSum = 0;
        if (cart.length === 0) {
            cartDisplay.innerHTML += "<p>Cart is empty</p>";
        } else {
            cart.forEach((item, index) => {
                totalSum += item.price;
                cartDisplay.innerHTML += `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <span>${item.name} - ₹${item.price.toFixed(2)}</span>
                        <button class="remove" data-index="${index}" style="color: red; background: none; border: none; cursor: pointer;">Remove</button>
                    </div>`;
            });
            cartDisplay.innerHTML += `
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <strong>Total: ₹${totalSum.toFixed(2)}</strong>
                </div>
                <button id="checkout" style="width: 100%; margin-top: 10px; padding: 10px; background-color:rgb(175, 76, 158); color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Checkout
                </button>`;
        }

        // Checkout Button: Redirect to index4.html and pass total to payment form
        const checkoutButton = document.getElementById("checkout");
        if (checkoutButton) {
            checkoutButton.addEventListener("click", () => {
                console.log("Checkout clicked!");
                // Store the total amount in sessionStorage to transfer it to the payment page
                sessionStorage.setItem('totalAmount', totalSum.toFixed(2));
                window.location.href = "index4.html"; // Change this to your actual path if needed
            });
        } else {
            console.log("Checkout button not found!");
        }
    }

    // Add to Cart
    document.querySelectorAll(".add-to-cart").forEach((button) => {
        button.addEventListener("click", () => {
            const medicineName = button.getAttribute("data-name");
            const medicinePrice = parseFloat(button.parentElement.querySelector("p:nth-of-type(2)").textContent.replace('Price: ₹', '').trim());
            cart.push({ name: medicineName, price: medicinePrice });
            renderCart();
        });
    });

    // Remove from Cart
    cartDisplay.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove")) {
            const index = event.target.getAttribute("data-index");
            cart.splice(index, 1);
            renderCart();
        }
    });

    // Search Functionality
    searchBar.addEventListener("input", (event) => {
        const query = event.target.value.toLowerCase();
        medicines.forEach((medicine) => {
            const name = medicine.querySelector("h3").textContent.toLowerCase();
            if (name.includes(query)) {
                medicine.style.display = "block";
            } else {
                medicine.style.display = "none";
            }
        });
    });

    // Initial Render
    renderCart();
});
