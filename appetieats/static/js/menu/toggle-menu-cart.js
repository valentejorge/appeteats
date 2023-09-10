/*
document.addEventListener("DOMContentLoaded", function() {
    const menu = document.querySelector('.menu');
    const cart = document.querySelector('.cart');

    const menuBtn = document.querySelector("#menuBtn");
    const cartBtn = document.querySelector("#cartBtn");

    menuBtn.addEventListener('click', () => {
        menu.classList.add('active');
        cart.classList.remove('active');
    })

    cartBtn.addEventListener('click', () => {
        cart.classList.add('active');
        menu.classList.remove('active');
    })


    console.log(menuBtn);
    console.log(cartBtn);
});
*/
document.addEventListener("DOMContentLoaded", function() {
const menuNav = document.querySelector('#menuBtn')
const cartNav = document.querySelector('#cartBtn')
    function checkHashUrl() {
        const menu = document.querySelector('.menu');
        const cart = document.querySelector('.cart');


        const hash = window.location.hash;
        if (hash == "#cart") {
            cart.classList.add('active');
            menu.classList.remove('active');

            cartNav.classList.add('nav_link--active')
            menuNav.classList.remove('nav_link--active')
        }
        else if (hash == "#menu") {
            menu.classList.add('active');
            cart.classList.remove('active');

            cartNav.classList.remove('nav_link--active')
            menuNav.classList.add('nav_link--active')
        }
    }
    window.addEventListener("hashchange", checkHashUrl);
    checkHashUrl();
});

