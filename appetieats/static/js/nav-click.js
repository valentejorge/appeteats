const navLinks = document.querySelectorAll('.nav_link');

navLinks.forEach((link) => {
    link.addEventListener('click', () => {
        navLinks.forEach((link) => link.classList.remove('nav_link--active'));
        link.classList.add('nav_link--active');
    });
});
