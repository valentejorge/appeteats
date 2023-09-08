let restaurantData = null;
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products; 
let categories; 

async function takeData() {
    const currentURL = window.location.pathname;

    const productsURL = currentURL + '/data';

    const response = await fetch(productsURL);
    const data = await response.json();

    restaurantData = data;
    products = data[0].products;
    categories = data[1].categories;
    return data
}

async function init() {
    const data = await takeData();

    if (data) {
        const products = data[0];
        const categories = data[1];

        buildMenu(products, categories)
    }
}

function buildMenu(productsData, categoriesData) {
    let html = '';
    for (const category of categoriesData.categories) {
        html += categoryConstructor(category.category_name, category.id);

        for (const product of productsData.products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.id, product.name, product.price)
            }
        }
        html += '</div>'
        html += overlayConstructor(category.id);

        for (const product of productsData.products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.id, product.name, product.price)
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

function productConstructor(productId, productName, productPrice) {
    const div = `
        <div class="product-width">
            <div class="card">
                <img src="/static/assets/img/macaroni.jpg" class="card-img-top mt-0" alt="${productName}">
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
    
    const item = {
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image_path
    }

    console.log(item)
    cart.push(item);
    updateCartDisplay();
    updateCartStorage();
    return
}

function updateCartDisplay() {
    const cartDiv = document.querySelector('#cart-list');
    cartDiv.innerHTML = '';
    console.log(cartDiv)

    cart.forEach(item => {
        const html = `
            <li class="list-group-item cart-list">
                <img src="/static/assets/img/macaroni.jpg" class="cart-img">
                <h6 class="p-title">${item.name}</h6>
                <div class="qty-group">
                    <button onclick="decrementQty(this)" class="qty-button">
                        <span class="material-icons nav_icons decrement">remove</span>
                    </button>
                    <input type="number" min="1" class="qty-input text-center" value="1" disabled>
                    <button onclick="incrementQty(this)" class="qty-button increment">
                        <span class="material-icons nav_icons">add</span>
                    </button>
                </div>
                <h6 class="p-title">$ ${(item.price).toFixed(2)}</h6>
                <button class="remove-button" onclick="removeFromCart(${item.id})">
                    <span class="material-icons nav_icons">remove_circle_outline</span>
                </button>
            </li>
        `
        cartDiv.insertAdjacentHTML('beforeend', html)
    })
}

function updateCartStorage() {
    localStorage.setItem('cart', JSON.stringify(cart))
}

function removeFromCart(item) {
    const index = cart.findIndex(cartItem => cartItem.id === item);
    console.log(index)
    if (index !== -1) {
        cart.splice(index, 1);
        updateCartStorage();
        updateCartDisplay();
    }
    updateCartStorage();
    updateCartDisplay();
}

updateCartDisplay();

init();
