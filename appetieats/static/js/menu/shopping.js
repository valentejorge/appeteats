async function takeData() {
    const currentURL = window.location.pathname;

    const productsURL = currentURL + '/data';

    const response = await fetch(productsURL);
    const products = await response.json();

    console.log(products);
    return products
}
async function buildMenu() {
    const data = await takeData();
    let html = '';
    for (const category of data[1].categories) {
        html += categoryConstructor(category.category_name, category.id);

        for (const product of data[0].products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.name, product.price)
            }
        }
        html += '</div>'
        html += overlayConstructor(category.id);

        for (const product of data[0].products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.name, product.price)
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

function productConstructor(productName, productPrice) {
    const div = `
        <div class="product-width">
            <div class="card">
                <img src="/static/assets/img/macaroni.jpg" class="card-img-top mt-0" alt="${productName}">
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

buildMenu();
