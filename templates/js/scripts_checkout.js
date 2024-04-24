document.addEventListener("DOMContentLoaded", function() {
    // Retrieve product id from URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('product_id');

    // Define product details
    const productDetails = {
        "product1": {
            "image": "/static/assets/product1.jpg",
            "price": "$10.00"
        },
        "product2": {
            "image": "/static/assets/product2.jpg",
            "price": "$15.00"
        },
        // Add more products as needed
    };

    // Populate product details
    const productDetailElement = document.getElementById('product-details');
    if (productId && productDetails.hasOwnProperty(productId)) {
        const product = productDetails[productId];
        const imageElement = document.createElement('img');
        imageElement.src = product.image;
        const priceElement = document.createElement('p');
        priceElement.textContent = "Price: " + product.price;
        productDetailElement.appendChild(imageElement);
        productDetailElement.appendChild(priceElement);
    } else {
        productDetailElement.textContent = "Product not found";
    }

    // Order button click event
    document.getElementById('order-btn').addEventListener('click', function() {
        const quantity = document.getElementById('quantity').value;
        const size = document.getElementById('size').value;
        const userName = "User"; // You can replace this with actual user name retrieval logic

        // Prepare data for POST request
        const postData = {
            "product_id": productId,
            "user_name": userName,
            "size": size,
            "quantity": quantity
        };

        // Send POST request to /orders_update
        fetch('/orders_update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        })
        .then(response => {
            if (response.ok) {
                // Redirect to home page after successful order placement
                window.location.href = "/home";
            } else {
                console.error('Failed to place order');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
