const buttons = document.querySelectorAll('.nav_link')
const pages = document.querySelectorAll(`[name="page"]`)

buttons.forEach((button) => {
    button.addEventListener('click', () => {

        pages.forEach((page) => {
            page.classList.remove('active');
        });

        const page = document.querySelector(`#${button.name}`)
        page.classList.add('active');
    });
});

function clickHash() {
    const buttonHash = window.location.hash;
    const buttonName = buttonHash.slice(1);
    if (buttonHash) {
        const button = document.querySelector(`[name="${buttonName}"]`);
        button.click();
    }
}

document.addEventListener("DOMContentLoaded", clickHash);
window.addEventListener("hashchange", clickHash);
