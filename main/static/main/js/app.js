const sideToggle = document.querySelector('.js-side-toggle');
const side = document.querySelector('.js-side');
const mainContent = document.querySelector('.js-main');

sideToggle.addEventListener('click', () => {
    side.classList.toggle('minify');
    mainContent.classList.toggle('wide');
})


document.addEventListener('DOMContentLoaded', function() {
    var currentUrl = window.location.pathname;

    // Поиск всех ссылок в навигации
    var navLinks = document.querySelectorAll('.nav__list-link');

    // Перебор всех ссылок и установка активного класса на соответствующей ссылке
    navLinks.forEach(function(link) {
        var linkUrl = link.getAttribute('href');

        // Проверка, соответствует ли текущий URL ссылке
        if (currentUrl === linkUrl) {
            link.classList.add('active');
        }
    });
});