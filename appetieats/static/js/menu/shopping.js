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
        html += categoryConstructor(category.category_name);
        for (const product of data[0].products) {
            if (product.category_id == category.id) {
                html += productConstructor(product.name, product.price)
            }
        }
        html += '</div>'
    }
    document.querySelector('#new-cart-view').innerHTML = html;
}

function categoryConstructor(category_name) {
    const div = `
            <button class="view-all-button d-flex justify-content-between align-items-start">
                <h3>${category_name}</h3>
                <span class="material-icons nav_icons">
                    arrow_forward_ios
                </span>
            </button>
        <div class="products-line mb-3">
    `
    return div;
}

function productConstructor(product_name, product_price) {
    const div = `
        <div class="product-width">
            <div class="card">
                <img src="/static/assets/img/macaroni.jpg" class="card-img-top mt-0" alt="{{ product.name }}">
                <div class="card-body p-2 d-flex flex-column align-items-start">
                    <h6 class="p-title mb-2">${product_name}</h6>
                    <h6 class="price mt-auto mb-0">$ ${product_price.toFixed(2)}</h6>
                </div>
            </div>
        </div>
    `
    return div;
}

buildMenu();
