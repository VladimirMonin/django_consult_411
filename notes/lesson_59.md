# Тема Django Формы Ч1. Как обрабатывать простые формы? Знакомство с инструментами. Урок 59


## Механизмы защиты в Djano - CSRF

CSRF - Cross-Site Request Forgery
Что такое CSRF?
Почему важно быть защищенным от CSRF?
Тег шаблонизатора `{% csrf_token %}` и куда его помещать?

![csrf_token_browser.png](./images/csrf_token_browser.png)

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

Начальный варант для демонстрации работы отладчика Django и анализа инструмента разарботчика в браузере

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