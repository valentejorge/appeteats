const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach((link) => {
    link.addEventListener('click', () => {
        navLinks.forEach((link) => link.classList.remove('nav-link-active'));
        link.classList.add('nav-link-active');
    });
});
