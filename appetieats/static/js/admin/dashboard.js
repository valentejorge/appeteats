const buttons = document.querySelectorAll('.top-button')
const pages = document.querySelectorAll('.kanban-page')
pages[0].classList.add('active');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        buttons.forEach((button) => button.classList.remove('active'));
        button.classList.add('active');

        pages.forEach((page) => {
            page.classList.remove('active');
        })

        const page = document.querySelector(`#${button.name}`)
        page.classList.add('active');
    });
});
