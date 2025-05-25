// Сделаем alert по клику на заголовок H1
document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('h1');
    if (header) {
        header.addEventListener('click', function() {
            alert('Вы кликнули по заголовку H1!');
        });
    } else {
        console.error('Заголовок H1 не найден на странице.');
    }
});