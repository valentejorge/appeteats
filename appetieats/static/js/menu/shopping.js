let restaurantData = null;
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products; 
let restaurantID;
let categories; 

async function takeData() {
    const currentURL = window.location.pathname;

    const productsURL = currentURL + '/data';

    const response = await fetch(productsURL);
    const data = await response.json();

    restaurantData = data;
    products = data[0].products;
    categories = data[1].categories;
    if (data[0].products[0]) {
        restaurantID = data[0].products[0].user_id;
    }
    return data
}

async function init() {
    const data = await takeData();


    if (data) {
        const products = data[0];
        const categories = data[1];

        updateCart();
        buildMenu(products, categories)
    }
}

function buildMenu(productsData, categoriesData) {
    let html = '';
    for (const category of categoriesData.categories) {
        html += categoryConstructor(category.category_name, category.id);

        for (const product of productsData.products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.id, product.name, product.price, product.image_path)
            }
        }
        html += '</div>'
        html += overlayConstructor(category.id);

        for (const product of productsData.products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.id, product.name, product.price, product.image_path)
            }
        }
        html += `
            </div>
            </div>
            `
    }
    const menuDiv = document.querySelector('#menu');
    console.log(menuDiv);
    menuDiv.insertAdjacentHTML('beforeend', html)
}

function categoryConstructor(categoryName, categoryId) {
    const div = `
            <button class="view-all-button d-flex justify-content-between align-items-start" onclick="showOverlay(${categoryId})">
                <h3>${categoryName}</h3>
                <span class="material-icons nav_icons">
                    arrow_forward_ios
                </span>
            </button>
        <div class="products-line mb-3">
    `
    return div;
}

function productConstructor(productId, productName, productPrice, productImage) {
    const div = `
        <div class="product-width">
            <div class="card">
                <img src="/static/cache/${productImage}" class="card-img-top mt-0" alt="${productName}">
                <button onclick="addToCart(${productId})" class="add-to-cart-button">
                    <span class="material-icons nav_icons">add</span>
                </button>
                <div class="card-body p-2 d-flex flex-column align-items-start">
                    <h6 class="p-title mb-2">${productName}</h6>
                    <h6 class="price mt-auto mb-0">$ ${productPrice.toFixed(2)}</h6>
                </div>
            </div>
        </div>
    `
    return div;
}

function overlayConstructor(categoryId) {
    const div = `
        <div class="overlay" data-category="${categoryId}">
            <button class="back-button d-flex align-items-start justify-content-start" onclick="hideOverlay(${categoryId})">
                <span class="material-icons nav_icons">chevron_left</span>
                <span class="flex-grow-1 text-start">
                    Back
                </span>

            </button>
        <div class="main-overlay">
    `
    return div
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) {
        console.error('Product not found.');
        return
    }
    const productInCart = cart.find(p => p.id === productId);
    if (productInCart) {
        productInCart.quantity += 1;
        productInCart.subtotal = productInCart.price * productInCart.quantity;
    }
    else {
        const item = {
            id: product.id,
            name: product.name,
            price: product.price,
            subtotal: product.price,
            quantity: 1,
            image: product.image_path,
            restaurant_id: product.user_id
        }
        cart.push(item);
    }
    
    updateCart();
    return
}

function updateCartDisplay() {
    const cartDiv = document.querySelector('#cart-list');
    cartDiv.innerHTML = '';

    const cartItemsCurrentRestaurant = cart.filter(item => item.restaurant_id == restaurantID);

    cartItemsCurrentRestaurant.forEach(item => {
        const html = `
            <li class="list-group-item cart-list">
                <img src="/static/cache/${item.image}" class="cart-img">
                <h6 class="mb-0">${item.name}</h6>
                <div class="qty-group">
                    <button onclick="updateQty(this, ${item.id})" class="qty-button decrement">
                        <span class="material-icons nav_icons decrement">remove</span>
                    </button>
                    <input type="number" min="1" class="qty-input text-center" value="${item.quantity}" disabled>
                    <button onclick="updateQty(this, ${item.id})" class="qty-button increment">
                        <span class="material-icons nav_icons">add</span>
                    </button>
                </div>
                <h6 class="mb-0">$ ${(item.subtotal).toFixed(2)}</h6>
            </li>
        `
        cartDiv.insertAdjacentHTML('beforeend', html)
    })
}

function updateCartStorage() {
    localStorage.setItem('cart', JSON.stringify(cart))
}

function updateQty(button, id) {
    const qtyGroup = button.closest(".qty-group");
    const quantityInput = qtyGroup.querySelector(".qty-input");
    const currentValue = parseInt(quantityInput.value);
    const product = cart.find(p => p.id === id);
    
    if (!isNaN(currentValue) && button.classList.contains('increment')) {
        product.quantity += 1;
        product.subtotal= product.price * product.quantity;
        updateCart();
    }
    else if (!isNaN(currentValue) && button.classList.contains('decrement') && currentValue == 1) {
        removeFromCart(id);
    }
    else if (!isNaN(currentValue) && button.classList.contains('decrement')) {
        product.quantity -= 1;
        product.subtotal = product.price * product.quantity;
        updateCart();
    }
}

function removeFromCart(item) {
    const index = cart.findIndex(cartItem => cartItem.id === item);
    console.log(index)
    if (index !== -1) {
        cart.splice(index, 1);
        updateCart();
    }
    updateCart();
}

function updateCart() {
    updateCartStorage();
    updateCartDisplay();
}

init();
