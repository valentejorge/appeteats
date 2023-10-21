const buttons = document.querySelectorAll('.nav_link')
const pages = document.querySelectorAll(`[name="page"]`)
console.log(buttons)
console.log(pages)

buttons.forEach((button) => {
    button.addEventListener('click', () => {

        pages.forEach((page) => {
            page.classList.remove('active');
        });

        const page = document.querySelector(`#${button.name}`)
        console.log(page)
        page.classList.add('active');
    });
});

function clickHash() {
    const buttonHash = window.location.hash;
    const buttonName = buttonHash.slice(1);
    console.log(buttonName)
    if (buttonHash) {
        const button = document.querySelector(`[name="${buttonName}"]`);
        button.click();
    }
}

document.addEventListener("DOMContentLoaded", clickHash);
window.addEventListener("hashchange", clickHash);
