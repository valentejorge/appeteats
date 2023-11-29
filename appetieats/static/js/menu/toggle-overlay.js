function showProductDetails(productId) {
    event.stopPropagation();
    const product = products.find(p => p.id === productId)
    const div = `
            <div class="d-flex justify-content-center" style="width: 80vw; max-width: 400px; max-height: 100vh;">
                <div class="product-details" style="cursor: default;" >
                    <div class="" style="border: none;">
                        <img src="/static/cache/${product.image_path}" class="card-img-top mt-0" alt="${product.name}">
                        <div class="card-body p-2 d-flex flex-column align-items-start">
                            <h4 class="p-title mb-2">${product.name}</h4>
                            <p class="mb-2">${product.description}</p>
                            <h5 class="price mt-auto mb-3">$ ${product.price.toFixed(2)}</h5>
                            <button onclick="addToCart(${productId})" class="std-button button-click">Add to Cart</button>
                        </div>
                    </div>
                </div>
            </div>
        `

    const productOverlay = document.querySelector('#product-details')
    productOverlay.innerHTML = div;
    const overlay = document.querySelector('#product-overlay')
    overlay.classList.add('active');
}

function hideProductDetails() {
    const overlay = document.querySelector('#product-overlay')
    overlay.classList.remove('active');
}

function hideCategoryDetails() {
    const overlay = document.querySelector('#category-overlay')
    overlay.classList.remove('active');
}

function showCategory(categoryId) {
    const categoryProducts = products.filter(p => p.category_id === categoryId)

    let html = ''
    for (const product of categoryProducts) {
        html += productConstructor(product.id, product.name, product.price, product.image_path)
    }

    const productOverlay = document.querySelector('#category-details');
    productOverlay.innerHTML = html;

    const overlay = document.querySelector('#category-overlay')
    overlay.classList.add('active');
}
