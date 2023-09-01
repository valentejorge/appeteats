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


const viewAllButtons = document.querySelectorAll('.view-all-button');
const backButtons = document.querySelectorAll('.back-button');
const overlayContainers = document.querySelectorAll('.overlay');

viewAllButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        overlayContainers[index].classList.add('active');
    });
});

backButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        overlayContainers[index].classList.remove('active');
    });
});
