const buttons = document.querySelectorAll('.top-button')
const pages = document.querySelectorAll('.kanban-page')
pages[0].classList.add('active');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        window.location.hash = button.name;
        buttons.forEach((button) => button.classList.remove('active'));
        button.classList.add('active');

        pages.forEach((page) => {
            page.classList.remove('active');
        })

        const page = document.querySelector(`#${button.name}`)
        page.classList.add('active');
    });
});

document.addEventListener("DOMContentLoaded", clickHash);

function clickHash() {
    const buttonHash = window.location.hash;
    const buttonName = buttonHash.slice(1);
    console.log(buttonName)
    if (buttonHash) {
        const button = document.querySelector(`[name=${buttonName}]`);
        button.click();
    }
}
window.addEventListener("hashchange", clickHash);
