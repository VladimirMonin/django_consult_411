# Тема Django Формы Ч1. Как обрабатывать простые формы? Знакомство с инструментами. Урок 59

## Механизмы защиты в Djano - CSRF

CSRF - Cross-Site Request Forgery
Что такое CSRF?
Почему важно быть защищенным от CSRF?

>[!warning]
>#### ⚠️ Важность защиты от CSRF
>CSRF-атаки позволяют злоумышленникам выполнять действия от имени пользователя без его ведома. Защита критически важна для безопасности веб-приложений, так как предотвращает несанкционированные операции.

Тег шаблонизатора `{% csrf_token %}` и куда его помещать?

![csrf_token_browser.png](./images/csrf_token_browser.png)

*Пояснение:* Всегда добавляйте `{% csrf_token %}` внутри тега `<form>` для защиты от межсайтовой подделки запросов.

## Разберем пример просто формы

Мы сверстаем форму самостоятельно в HTML и обработаем ее в Django View

```html
{% extends "base.html" %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card mt-5">
                <div class="card-body text-center">
                    <h1 class="card-title">Запись на приём</h1>
                    <form action="" method="post">
                        {% csrf_token %}
                        <input type="text" name="name" placeholder="Имя" class="form-control mb-3 mt-3" required>
                        <input type="tel" name="phone" placeholder="Телефон" class="form-control mb-3" required>
                        <textarea name="comment" placeholder="Комментарий" class="form-control mb-3" rows="10"></textarea>
                        <button type="submit" class="btn btn-dark">Записаться</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

- Пояснения что мы должны использовать `{% csrf_token %}`
- Иначе Django не будет принимать POST запросы
- Про атрибуты `name`, `placeholder`, `class`, `rows` 

## View для обработки этой формы

Начальный вариант для демонстрации работы отладчика Django и анализа инструмента разработчика в браузере

![post_request_debug.png](./images/post_request_debug.png)

Этот вариант не будет работать правильно, однако мы сможем увидеть в инструментах разработчика, что данные приходят на сервер, а в отладчике Django, что данные приходят в словарь `request.POST`

![post_request_browser_console.png](./images/post_request_browser_console.png)

```python
def order_create(request):
    if request.method == "GET":
        return render(request, "order_form.html")
    
    elif request.method == "POST":
        return render(request, "order_form.html")
```

Конечный вариант

```python
def order_create(request):
    if request.method == "GET":
        return render(request, "order_form.html")
    
    elif request.method == "POST":
        # Получаем данные из формы
        
>[!info]
>#### ℹ️ Работа с request.POST
>Данные формы доступны через `request.POST` - это словарь-like объект. Используйте `.get()` для безопасного получения значений, чтобы избежать KeyError.

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        comment = request.POST.get("comment")

        # Проверка что есть имя и телефон
        if not name or not phone:
            return HttpResponse("Не заполнены обязательные поля", status=400)
        
        # Создаем объект заявки
        order = Order.objects.create(
            name=name,
            phone=phone,
            comment=comment,
        )
        
        # Редирект на страницу благодарности
        return redirect("thanks")
```

## Вариант формы для обновления Order

```python
def order_update(request, order_id):
    if request.method == "GET":
        # Получаем объект заявки
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponse("Заявка не найдена", status=404)
        
        context = {
            "title": "Редактирование заявки",
            "button_text": "Сохранить",
            "order": order,
        }
        return render(request, "order_form.html", context)
    
    elif request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        comment = request.POST.get("comment")

        # Проверка что есть имя и телефон
        if not name or not phone:
            return HttpResponse("Не заполнены обязательные поля", status=400)
        
        # Обновляем объект заявки
        
>[!highlight]
>#### 🌟 Использование update()
>Метод `update()` работает на уровне БД и эффективен для массовых обновлений. Для обновления одного объекта предпочтительнее использовать `save()`.

        try:
            order = Order.objects.get(id=order_id)
            order.name = name
            order.phone = phone
            order.comment = comment
            order.save()
        except Order.DoesNotExist:
            return HttpResponse("Заявка не найдена", status=404)
        
        # Редирект на страницу благодарности
        return redirect("thanks")
```

HTML мы можем просто взять и использовать универсальный шаблон. Тут мы модифицировали шаблон для создания заявки, добавив переменные:
- заголовок
- текст кнопки
- Подстановка данных в поля ввода

```html
{% extends "base.html" %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card mt-5">
                <div class="card-body text-center">
                    <h1 class="card-title">
                        {{ title }}
                    </h1>
                    <form action="" method="post">
                        {% csrf_token %}
                        <input type="text" name="name" placeholder="Имя" class="form-control mb-3 mt-3" value="{{ order.name }}" required>
                        <input type="tel" name="phone" placeholder="Телефон" class="form-control mb-3" value="{{ order.phone }}" required>
                        <textarea name="comment" placeholder="Комментарий" class="form-control mb-3" rows="10">{{ order.comment }}</textarea>
                        <button type="submit" class="btn btn-dark">{{ button_text }}</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}