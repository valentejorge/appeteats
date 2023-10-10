/*
function toggleOverlay() {
    const overlayBg = document.querySelector("#overlay-bg")
    const products = this.parentElement.nextElementSibling;
    console.log(products)
    products.classList.toggle('overlay');
    overlayBg.classList.toggle('hide-important');
}

const viewAllButtons = document.querySelectorAll('.view-all-button');

viewAllButtons.forEach(button => {
    button.addEventListener('click', toggleOverlay);
});
*/

/*
const newCartView = document.querySelector('#new-cart-view');

newCartView.addEventListener('click', (event) => {
    const target = event.target;
    if (target.classList.contains('view-all-button')) {
        const categoryId = target.getAttribute('category');
        const overlay = document.querySelector(`[data-category="${categoryId}"]`);
        overlay.classList.add('active');
    }
    else if (target.classList.contains('back-button')) {
        const overlay = target.closest('.overlay');

        overlay.classList.remove('active');
    }
});
*/

function showOverlay(overlayId) {
    const overlay = document.querySelector(`[data-category="${overlayId}"]`)
    overlay.classList.add('active');
}

function hideOverlay(overlayId) {
    const overlay = document.querySelector(`[data-category="${overlayId}"]`)
    overlay.classList.remove('active');
}

function showProductDetails(productId) {
    event.stopPropagation();
    const product = products.find(p => p.id === productId)
    const div = `
            <div class="" style="width: 50vh;">
                <div class="product-details" >
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
