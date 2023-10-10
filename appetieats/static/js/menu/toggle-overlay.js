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

function showProductDetails(productDiv) {
    event.stopPropagation();
    const productOverlay = document.querySelector('#product-details')
    productOverlay.innerHTML = productDiv;
    const overlay = document.querySelector('#product-overlay')
    overlay.classList.add('active');
}
function hideProductDetails() {
    const overlay = document.querySelector('#product-overlay')
    overlay.classList.remove('active');
}
