# Lesson 53

## Псевдонимы маршрутов и заблонный тег URL

name = "order_list"
# Так маршрут добывается в Python коде через функцию reverse
url = reverse("order_list")

# Так маршрут добывается в шаблоне через тег url
<a href="{% url 'order_list' %}">Список заявок</a>

# А не так

<a href="/orders/">Список заявок</a>


## Наш вариант
Мы остановились на 

def get_main_menu():
    """Функция возвращает список пунктов меню для сайта"""
    return [
        {"name": "Главная", "url": reverse("landing")},
        {"name": "О нас", "url": reverse("landing") + "#about"},
        {"name": "Преимущества", "url": reverse("landing") + "#benefits"},
        {"name": "Мастера", "url": reverse("landing") + "#masters"},
        {"name": "Услуги", "url": reverse("landing") + "#services"},
        {"name": "Запись", "url": reverse("landing") + "#booking"},
        {"name": "Управление", "url": reverse("order_list")},
    ]


Потому что мы не можем использовать в шаблонах тег URL с якорными ссылками.

<!-- Пояснить почему -->

## Контекстный процессор