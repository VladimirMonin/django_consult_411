## Создание и подключение приложения users 🚀

Для начала работы с системой аутентификации пользователей в Django, первым шагом является создание отдельного приложения, которое будет отвечать за всю логику, связанную с пользователями. Это помогает поддерживать чистоту кода и модульность проекта.

Для создания нового приложения `users` в вашем проекте Django необходимо выполнить следующую команду в терминале, находясь в корневой директории проекта:

```bash
poetry run python manage.py startapp users
```

Эта команда сгенерирует базовую структуру каталогов и файлов для нового приложения `users`. После создания приложения, его необходимо зарегистрировать в основном конфигурационном файле проекта, чтобы Django знал о его существовании и мог использовать его функциональность. Для этого откройте файл `barbershop/settings.py` и добавьте `'users'` в список `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "core",
    "users", # NEW
]
```

>[!info]
>
>#### Модульность Django 🧩
>
>Принцип создания отдельных приложений для различных функциональных областей (например, `users` для аутентификации, `core` для основной логики) является ключевым аспектом архитектуры Django. Он способствует лучшей организации кода, упрощает его поддержку и повторное использование.

### Настройка маршрутов: urls.py приложения users 🔗

После создания и подключения приложения `users`, следующим шагом является определение его собственных URL-маршрутов. Это позволяет изолировать адреса, относящиеся к пользовательской функциональности, от общих маршрутов проекта. Внутри директории `users` необходимо создать новый файл `urls.py`, если его там еще нет. В этом файле будут определены маршруты для регистрации, входа и выхода пользователей.

```python
# users/urls.py
from django.urls import path
from .views import register, login, logout

# Маршруты будут иметь префикс /users/
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
```

Как видно из примера, мы импортируем функции представлений (`register`, `login`, `logout`) из файла `views.py` этого же приложения и связываем их с соответствующими URL-путями. Параметр `name` для каждого маршрута позволяет ссылаться на эти URL-адреса по их именам в шаблонах и коде, что делает систему более гибкой и устойчивой к изменениям URL.

Далее, чтобы эти маршруты стали доступны в вашем проекте, необходимо подключить `urls.py` приложения `users` к основному файлу маршрутов проекта `barbershop/urls.py`. Это делается с помощью функции `include()`.

```python
# barbershop/urls.py
from django.contrib import admin
from django.urls import path, include # Убедитесь, что include импортирован
from users import urls as users_urls # Импортируем urls из приложения users

urlpatterns = [
    path("admin/", admin.site.urls),
    # ... другие маршруты ...
    # Пользователи
    path("users/", include(users_urls))
]
```

Благодаря этой настройке, все маршруты, определенные в `users/urls.py`, будут автоматически иметь префикс `/users/`. Например, страница регистрации будет доступна по адресу `/users/register/`, страница входа — по `/users/login/`, а выхода — по `/users/logout/`.

### Создание вью-заглушек для тестирования 🏗️

На данном этапе, когда маршруты настроены, но полная логика форм и аутентификации еще не реализована, удобно создать простые "заглушки" для функций представлений. Эти заглушки помогут убедиться, что маршрутизация работает корректно и что при переходе по соответствующим URL-адресам вызываются правильные функции.

Откройте файл `users/views.py` и добавьте следующий код:

```python
from django.shortcuts import render, HttpResponse

def register(request):
    return HttpResponse("Регистрация")

def login(request):
    return HttpResponse("Авторизация")

def logout(request):
    return HttpResponse("Выход")
```

Теперь, если вы запустите сервер разработки Django (`python manage.py runserver`) и перейдете по адресам `/users/register/`, `/users/login/` или `/users/logout/`, вы увидите соответствующий текстовый ответ в браузере. Это является подтверждением того, что все базовые настройки маршрутизации выполнены верно, и мы готовы к дальнейшей реализации более сложной логики аутентификации.

В следующих разделах мы перейдем к созданию форм и полноценной реализации логики регистрации, входа и выхода пользователей.

---

## Минимальный вариант login - logout - register 🔐

В этом разделе мы погрузимся в создание основных форм для регистрации и авторизации пользователей в приложении Django. Эти формы являются фундаментом для взаимодействия пользователей с вашей системой, обеспечивая безопасный ввод данных и их проверку. Мы рассмотрим две ключевые формы: `RegistrationForm` для регистрации новых пользователей и `LoginForm` для их последующей авторизации.

### Форма регистрации пользователя (RegistrationForm) 📝

Форма регистрации `RegistrationForm` предназначена для сбора необходимой информации от нового пользователя, такой как имя пользователя, адрес электронной почты и пароль. Она также включает повторный ввод пароля для подтверждения, что помогает избежать опечаток.

```python
# users/forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data
```

Давайте детально разберем каждый компонент этой формы:

* **Импорты**: В начале файла импортируются необходимые модули: `forms` из Django для создания форм, а также `get_user_model` и `authenticate` из `django.contrib.auth`. Функция `get_user_model()` позволяет получить текущую активную модель пользователя, что делает код более гибким и не привязывает его к конкретной модели `User` напрямую.
* **Определение полей**: Форма `RegistrationForm` наследуется от `forms.Form` и определяет четыре поля: `username`, `email`, `password` и `password2`. Каждое поле имеет `label` (отображаемое имя) и `widget`, который определяет HTML-элемент для ввода данных. В данном случае используются `TextInput` для имени пользователя, `EmailInput` для email и `PasswordInput` для паролей, что обеспечивает скрытый ввод символов. Класс `form-control` добавляется для стилизации с помощью Bootstrap.

>[!info]
>
>#### Примечание о виджетах 🎨
>
>Виджеты в Django Forms определяют, как поле будет отображаться в HTML. Использование `forms.PasswordInput` гарантирует, что вводимые символы будут скрыты, повышая безопасность ввода пароля.

* **Метод `clean_username()`**: Этот метод отвечает за валидацию поля `username`. Он проверяет, существует ли уже пользователь с таким именем в базе данных. Если имя пользователя уже занято, генерируется ошибка `forms.ValidationError`, которая будет отображена пользователю.
* **Метод `clean_email()`**: Аналогично, этот метод валидирует поле `email`. Он проверяет уникальность email-адреса, предотвращая регистрацию нескольких пользователей с одним и тем же адресом электронной почты.
* **Метод `clean()`**: Этот метод является общей валидацией для всей формы, которая выполняется после проверки отдельных полей. Здесь происходит сравнение полей `password` и `password2`. Если они не совпадают, вызывается `forms.ValidationError`, информируя пользователя о необходимости ввести одинаковые пароли. Метод `super().clean()` вызывается для получения уже очищенных данных из базового класса.

### Форма авторизации пользователя (LoginForm) 🔑

Форма авторизации `LoginForm` используется для входа существующих пользователей в систему. Она запрашивает имя пользователя и пароль, а затем проверяет их подлинность.

```python
# users/forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неверное имя пользователя или пароль.")
            # Сохраняем пользователя в форме для последующего использования во вью
            self.user_cache = user
        return cleaned_data
```

Рассмотрим особенности `LoginForm`:

* **Определение полей**: Форма содержит два поля: `username` и `password`, аналогичные полям в `RegistrationForm`, но без повторного ввода пароля.
* **Метод `clean()`**: Это ключевой метод для `LoginForm`. Он выполняет следующие шаги:
  * Получает введенные `username` и `password` из очищенных данных формы.
  * Использует функцию `authenticate()` из `django.contrib.auth`. Эта функция пытается аутентифицировать пользователя, используя предоставленные учетные данные. Если аутентификация успешна, она возвращает объект пользователя; в противном случае возвращает `None`.
  * Если `authenticate()` возвращает `None`, это означает, что учетные данные неверны, и генерируется `forms.ValidationError` с соответствующим сообщением.
  * **`self.user_cache = user`**: Если аутентификация прошла успешно, объект пользователя сохраняется в атрибуте `user_cache` формы. Это очень удобный подход, так как позволяет получить объект аутентифицированного пользователя непосредственно из формы во вью, избегая повторного поиска пользователя в базе данных.

>[!highlight]
>
>#### Важность `authenticate()` 💡
>
>Функция `authenticate()` не только проверяет учетные данные, но и обрабатывает различные бэкэнды аутентификации, настроенные в вашем проекте Django. Она не выполняет вход пользователя в сессию, а лишь подтверждает его подлинность. Сама процедура входа в сессию будет выполнена во вью с помощью функции `login`.

Эти формы закладывают основу для безопасного и функционального процесса регистрации и авторизации. В следующем разделе мы рассмотрим, как эти формы интегрируются с HTML-шаблонами для создания удобного пользовательского интерфейса.

---

### Шаблоны форм авторизации и регистрации 🖥️

Для обеспечения пользовательского интерфейса для входа и регистрации в Django-приложении используются HTML-шаблоны. Эти шаблоны отвечают за отображение форм, обработку ошибок и навигацию между страницами авторизации и регистрации. В данном случае, шаблоны созданы с использованием фреймворка Bootstrap для стилизации, что делает их адаптивными и визуально привлекательными.

Давайте рассмотрим структуру и ключевые элементы шаблона для входа (`login.html`), а затем отметим особенности шаблона для регистрации, поскольку они имеют много общего.

#### Шаблон для входа (`login.html`) 🔑

```html
{% extends 'base.html' %}

{% block title %}Вход{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title text-center">Вход</h2>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        {% for field in form %}
                            <div class="mb-3">
                                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                                {{ field }}
                                {% if field.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ field.errors.as_text }}
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-dark">Войти</button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center">
                    <small>Нет аккаунта? <a href="{% url 'register' %}">Зарегистрироваться</a></small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Этот шаблон начинается с наследования базового шаблона `base.html` с помощью тега `{% extends 'base.html' %}`. Это позволяет использовать общую структуру сайта (шапку, подвал, стили) и вставлять уникальное содержимое в определённые блоки. В данном случае, содержимое помещается в блок `content`, а заголовок страницы определяется в блоке `title`.

Основное содержимое шаблона центрировано с помощью классов Bootstrap, таких как `container`, `row`, `justify-content-center` и `col-md-6`. Форма авторизации заключена в компонент `card`, который обеспечивает аккуратное визуальное оформление с заголовком (`card-header`), телом (`card-body`) и подвалом (`card-footer`).

Внутри элемента `<form>` используются следующие ключевые элементы Django-шаблонов:

* `{% csrf_token %}`: Этот тег крайне важен для безопасности. Он вставляет скрытое поле с токеном CSRF (Cross-Site Request Forgery), который Django использует для защиты от атак подделки межсайтовых запросов. Без этого тега отправка POST-запросов будет отклонена.

    >[!info]
>
    >#### Защита CSRF 🛡️
>
    >Всегда включайте тег `{% csrf_token %}` в формы, которые отправляют данные методом `POST`. Это обязательное требование безопасности в Django.

* `{% if form.non_field_errors %}`: Этот блок проверяет наличие общих ошибок формы, которые не относятся к конкретному полю (например, "Неверное имя пользователя или пароль" после проверки входа). Если такие ошибки есть, они отображаются в виде предупреждения `alert-danger` от Bootstrap.

* `{% for field in form %}`: Этот цикл итерирует по всем полям, определённым в Django-форме (`LoginForm`). Для каждого поля создается блок `div` с классом `mb-3` (margin-bottom 3), содержащий метку (`label`) и само поле ввода.
  * `{{ field.id_for_label }}`: Генерирует уникальный `id` для поля, который используется атрибутом `for` в теге `<label>`, связывая метку с полем ввода для улучшения доступности.
  * `{{ field.label }}`: Отображает читабельное название поля (например, "Имя пользователя", "Пароль").
  * `{{ field }}`: Отображает сам элемент ввода (`<input>`) с применёнными виджетами и атрибутами из Django-формы.

* `{% if field.errors %}`: Внутри цикла для каждого поля проверяется наличие специфических ошибок (например, "Пользователь с таким именем уже существует"). Если ошибки есть, они отображаются с использованием классов `invalid-feedback d-block` для стилизации Bootstrap.

В нижней части формы находится кнопка `Войти` для отправки данных, а в `card-footer` расположена ссылка на страницу регистрации (`{% url 'register' %}`), предлагающая пользователю создать новый аккаунт, если у него его ещё нет.

#### Шаблон для регистрации (`register.html`) 📝

```html
{% extends 'base.html' %}

{% block title %}Регистрация{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title text-center">Регистрация</h2>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        {% for field in form %}
                            <div class="mb-3">
                                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                                {{ field }}
                                {% if field.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ field.errors.as_text }}
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-dark">Зарегистрироваться</button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center">
                    <small>Уже есть аккаунт? <a href="{% url 'login' %}">Войти</a></small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Шаблон `register.html` практически идентичен шаблону `login.html`. Основные отличия заключаются в:

* Заголовке страницы (`{% block title %}Регистрация{% endblock %}`).
* Тексте заголовка внутри карточки (`<h2 class="card-title text-center">Регистрация</h2>`).
* Тексте кнопки отправки формы (`<button type="submit" class="btn btn-dark">Зарегистрироваться</button>`).
* Тексте и URL-адресе ссылки в подвале карточки, которая теперь ведёт на страницу входа (`<a href="{% url 'login' %}">Войти</a>`).

Оба шаблона демонстрируют эффективное использование Django-форм в сочетании с Bootstrap для создания функциональных и стильных пользовательских интерфейсов. В следующем разделе мы рассмотрим, как эти формы и шаблоны взаимодействуют с представлениями (вьюшками) для обработки запросов пользователя.

---

## Вьюшки ⚙️

После того как мы подготовили формы для регистрации и авторизации, а также настроили соответствующие шаблоны, настало время реализовать логику обработки этих форм во вьюшках. Вьюшки (или представления) — это функции или классы, которые получают HTTP-запросы и возвращают HTTP-ответы, формируя динамическое содержимое веб-страниц. В данном случае они будут отвечать за обработку данных, отправленных пользователем, взаимодействие с базой данных для создания или проверки пользователя, а также за перенаправление пользователя на нужные страницы после успешной операции.

Ниже представлен код вьюшек, которые мы будем использовать для управления процессами регистрации, входа и выхода пользователей.

```python
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, LoginForm

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            auth_login(request, user)
            return redirect("landing")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None:
                auth_login(request, user)
                # Перенаправляем на next, если он есть
                return redirect(request.GET.get("next", "landing"))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

@require_POST # Будут работать только POST-запросы!
def logout(request):
    auth_logout(request)
    return redirect("landing")
```

### Детальные пояснения по вьюшкам 📝

Каждая из этих функций отвечает за определенный этап взаимодействия пользователя с системой аутентификации.

#### Функция `register` 🔑

Функция `register` обрабатывает процесс регистрации нового пользователя.

```python
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            auth_login(request, user)
            return redirect("landing")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})
```

Принцип работы этой вьюшки следующий:

* **Обработка POST-запроса**: Когда пользователь отправляет форму регистрации, запрос приходит методом `POST`. Условие `if request.method == "POST":` проверяет это.
* **Инициализация формы**: Создается экземпляр `RegistrationForm`, заполняемый данными из `request.POST`.
* **Валидация формы**: Метод `form.is_valid()` запускает все проверки, определенные в `RegistrationForm`, включая проверку уникальности имени пользователя и email, а также совпадения паролей.
    >[!info]
>
    >#### Валидация данных 🛡️
>
    >Метод `is_valid()` не только проверяет данные, но и очищает их, делая доступными через `form.cleaned_data`. Это безопасный способ получить данные из формы после успешной валидации.
* **Создание пользователя**: Если форма валидна, новый пользователь создается с помощью `User.objects.create_user()`. Этот метод автоматически хеширует пароль, что является стандартом безопасности. Мы извлекаем `username`, `email` и `password` из `form.cleaned_data`.
* **Автоматический вход**: После успешной регистрации `auth_login(request, user)` немедленно авторизует созданного пользователя в системе, что избавляет его от необходимости входить вручную сразу после регистрации.
* **Перенаправление**: Пользователь перенаправляется на страницу `landing` (главную страницу или страницу по умолчанию), что завершает процесс регистрации.
* **Обработка GET-запроса**: Если запрос не `POST` (т.е. это первый заход на страницу регистрации), создается пустой экземпляр `RegistrationForm`, который затем передается в шаблон для отображения.
* **Отображение шаблона**: Функция `render` используется для отображения шаблона `users/register.html`, передавая в него объект `form` для правильного отображения полей и ошибок.

#### Функция `login` 🚪

Функция `login` отвечает за процесс аутентификации существующих пользователей.

```python
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None:
                auth_login(request, user)
                # Перенаправляем на next, если он есть
                return redirect(request.GET.get("next", "landing"))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})
```

Логика функции `login` похожа на `register`, но имеет свои особенности:

* **Обработка POST-запроса**: Аналогично регистрации, проверяется, что запрос является `POST`.
* **Инициализация формы**: Создается экземпляр `LoginForm`, заполняемый данными из `request.POST`.
* **Валидация формы**: Метод `form.is_valid()` вызывает метод `clean` формы `LoginForm`, который использует `authenticate` для проверки учетных данных пользователя. Если аутентификация прошла успешно, объект пользователя сохраняется в `form.user_cache`.
    >[!highlight]
>
    >#### Кэш пользователя в форме 🧠
>
    >Использование `self.user_cache` в `LoginForm` позволяет передать объект аутентифицированного пользователя из метода `clean` формы во вьюшку, избегая повторной аутентификации.
* **Аутентификация и вход**: Если форма валидна и `user` не равен `None`, вызывается `auth_login(request, user)` для установки сессии пользователя.
* **Перенаправление с `next`**: После успешного входа пользователь перенаправляется. Особое внимание уделяется параметру `next` в URL-адресе (`request.GET.get("next", "landing")`). Это позволяет пользователю после входа вернуться на ту страницу, с которой он был перенаправлен на страницу входа (например, если он пытался получить доступ к защищенному ресурсу). Если параметра `next` нет, пользователь будет перенаправлен на страницу `landing`.
* **Обработка GET-запроса**: При первом посещении страницы входа (GET-запрос) создается пустой `LoginForm`, который передается в шаблон.
* **Отображение шаблона**: Функция `render` отображает шаблон `users/login.html` с переданным объектом формы.

#### Функция `logout` 🚪➡️

Функция `logout` отвечает за выход пользователя из системы.

```python
@require_POST # Будут работать только POST-запросы!
def logout(request):
    auth_logout(request)
    return redirect("landing")
```

Особенности этой функции:

* **Декоратор `@require_POST`**: Этот декоратор гарантирует, что функция `logout` будет обрабатывать только `POST`-запросы. Это важная мера безопасности, предотвращающая случайный выход пользователя при переходе по ссылке (GET-запрос). Выход должен быть инициирован явным действием, например, отправкой формы.
    >[!warning]
>
    >#### Почему `POST` для выхода? 🚫
>
    >Использование `POST` для выхода предотвращает атаки CSRF (Cross-Site Request Forgery) и случайный выход пользователя, например, при индексации страницы поисковыми роботами или при переходе по вредоносной ссылке.
* **Выход из системы**: `auth_logout(request)` уничтожает сессию пользователя, тем самым завершая его текущий сеанс.
* **Перенаправление**: После выхода пользователь перенаправляется на страницу `landing`.

Эти три вьюшки формируют основу функциональности аутентификации в приложении, позволяя пользователям регистрироваться, входить в систему и выходить из неё. В следующей части мы рассмотрим, как эти функции могут быть упрощены с использованием встроенных форм Django.

---

Мы уже настроили формы и вьюшки для регистрации, входа и выхода пользователей. Теперь пришло время интегрировать эти функции в пользовательский интерфейс, чтобы пользователи могли легко взаимодействовать с системой аутентификации. Один из ключевых элементов, который должен динамически отображать статус пользователя, — это навигационное меню.

### Меню навигации: Отображение статуса аутентификации ✨

Для обеспечения удобства пользователя крайне важно, чтобы навигационное меню сайта адаптировалось под его текущее состояние — вошел он в систему или нет. Это позволяет отображать актуальные ссылки (например, "Войти" и "Зарегистрироваться" для неавторизованных пользователей или "Привет, [Имя пользователя]!" и "Выход" для авторизованных).

Рассмотрим код инклюда меню, который использует возможности шаблонизатора Django для создания динамического содержимого:

```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">Барбершоп</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Переключатель навигации">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {% for menu_item in menu %}
          <li class="nav-item">
            <a class="nav-link" href="{{ menu_item.url }}">{{ menu_item.name }}</a>
          </li>
        {% endfor %}
      </ul>
      <ul class="navbar-nav ms-auto">
        {% if user.is_authenticated %}
          <li class="nav-item">
            <span class="nav-link">Привет, {{ user.username }}!</span>
          </li>
          <li class="nav-item">
            <form action="{% url 'logout' %}" method="post" class="d-inline">
              {% csrf_token %}
              <button type="submit" class="nav-link btn btn-link">Выход</button>
            </form>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'login' %}">Войти</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'register' %}">Зарегистрироваться</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

Этот HTML-код представляет собой стандартную Bootstrap-навигационную панель. Основная логика, связанная с аутентификацией, сосредоточена в секции с классом `navbar-nav ms-auto`, которая отвечает за элементы меню, выровненные по правому краю.

В этой части меню используется условный оператор Django-шаблонов `{% if user.is_authenticated %}`. Переменная `user` автоматически доступна в контексте шаблона благодаря `django.contrib.auth.context_processors.auth`, который по умолчанию включен в `TEMPLATES` в `settings.py`. Свойство `is_authenticated` объекта `user` возвращает `True`, если пользователь вошел в систему, и `False` в противном случае.

Если пользователь авторизован, отображается приветствие "Привет, `{{ user.username }}`!" и кнопка "Выход". Кнопка "Выход" реализована как HTML-форма с методом `POST`, которая отправляет запрос на URL-адрес, определенный как `logout` (мы его настраивали ранее в файле `users/urls.py`). Использование `POST` для выхода из системы является хорошей практикой безопасности, поскольку предотвращает случайный выход пользователя при переходе по ссылке или при индексации поисковыми системами.

>[!info]
>
>#### Защита от CSRF 🛡️
>
>Обратите внимание на строку `{% csrf_token %}` внутри формы выхода. Этот тег генерирует скрытое поле формы с токеном Cross-Site Request Forgery (CSRF). Это критически важный элемент безопасности в Django, который защищает ваш сайт от атак подделки межсайтовых запросов. Без него злоумышленник мог бы заставить пользователя выполнить нежелательные действия (например, выйти из системы) без его ведома.

В случае, если пользователь не авторизован (`{% else %}`), меню отображает ссылки "Войти" и "Зарегистрироваться". Эти ссылки используют тег `{% url %}` для динамического построения URL-адресов на основе имен маршрутов, определенных в `users/urls.py` (`login` и `register`). Такой подход гарантирует, что даже при изменении структуры URL-адресов в будущем, ссылки в меню останутся рабочими.

Таким образом, это динамическое меню обеспечивает интуитивно понятное взаимодействие с системой аутентификации, адаптируясь под статус пользователя и предоставляя соответствующие опции.

---

## Вариант с специализированными формами ⚙️

В предыдущих разделах мы рассмотрели базовый подход к созданию форм регистрации и входа, используя стандартный класс `forms.Form`. Однако Django предоставляет более специализированные и мощные инструменты для работы с аутентификацией, которые значительно упрощают разработку и повышают безопасность. Эти инструменты — встроенные формы `UserCreationForm` и `AuthenticationForm`, предназначенные специально для создания пользователей и их аутентификации.

Использование этих форм позволяет нам сократить объем кода, поскольку они уже содержат логику валидации, связанную с пользователями, такую как проверка сложности пароля, подтверждение пароля при регистрации и аутентификация пользователя.

Рассмотрим, как можно адаптировать эти формы для наших нужд, используя следующий код:

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя пользователя"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )
```

### Детальные пояснения по специализированным формам 📝

Начнем с импортов, которые позволяют нам использовать необходимые компоненты Django. Мы импортируем стандартные `forms` для определения полей, `UserCreationForm` и `AuthenticationForm` из модуля `django.contrib.auth.forms`, а также `get_user_model` для получения текущей модели пользователя и `ValidationError` для обработки ошибок валидации.

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
```

Здесь `User = get_user_model()` является стандартной практикой в Django для получения активной модели пользователя, будь то встроенная `User` или пользовательская модель, определенная в проекте. Это обеспечивает гибкость и переносимость кода.

#### Класс `CustomUserCreationForm` 🔐

Этот класс предназначен для регистрации новых пользователей и наследуется от `UserCreationForm`, предоставляемой Django. `UserCreationForm` уже включает в себя поля для имени пользователя (`username`) и двух полей для пароля (`password`, `password2`), а также базовую логику валидации для них, включая проверку совпадения паролей и их сложности.

```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
```

Мы добавляем поле `email`, которое отсутствует в базовой `UserCreationForm`. Это поле является обязательным (`required=True`) и использует виджет `forms.EmailInput` для корректного отображения в HTML-форме. Атрибут `autocomplete="email"` помогает браузерам предлагать автозаполнение для поля электронной почты.

```python
    class Meta:
        model = User
        fields = ("username", "email")
```

Вложенный класс `Meta` используется для настройки поведения формы. Здесь мы указываем, что форма работает с моделью `User` и включает в себя поля `username` и `email`. Поля `password` и `password2` автоматически добавляются из базового класса `UserCreationForm`, поэтому их не нужно явно указывать в `Meta.fields`.

```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
```

Метод `__init__` переопределяется для добавления CSS-класса `form-control` ко всем полям формы. Это удобно для применения стилей Bootstrap или других CSS-фреймворков, обеспечивая единообразный внешний вид полей ввода. Вызов `super().__init__(*args, **kwargs)` гарантирует, что базовая инициализация формы Django будет выполнена корректно.

```python
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
```

Метод `clean_email` является пользовательским валидатором для поля `email`. Он проверяет, существует ли уже пользователь с таким адресом электронной почты в базе данных. Если такой пользователь найден, генерируется ошибка `ValidationError`, которая будет отображена пользователю. Этот подход обеспечивает уникальность email-адресов, предотвращая дублирование аккаунтов.

>[!info]
>
>#### Важные особенности `UserCreationForm` 💡
>
>При использовании `UserCreationForm` для создания пользователя, метод `form.save()` автоматически хеширует пароль и сохраняет нового пользователя в базу данных. Это значительно упрощает процесс регистрации, избавляя от необходимости вручную обрабатывать пароли и вызывать `User.objects.create_user()`.

#### Класс `CustomAuthenticationForm` 🔑

Этот класс предназначен для аутентификации пользователей (входа в систему) и наследуется от `AuthenticationForm`, предоставляемой Django. `AuthenticationForm` включает в себя поля для имени пользователя (`username`) и пароля (`password`), а также встроенную логику для проверки учетных данных с использованием функции `authenticate`.

```python
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя пользователя"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )
```

Как и в случае с `CustomUserCreationForm`, метод `__init__` переопределяется для добавления CSS-класса `form-control` к полям `username` и `password`. Кроме того, здесь добавляются атрибуты `placeholder`, которые отображают текст-подсказку внутри полей ввода, улучшая пользовательский интерфейс. Вызов `super().__init__(*args, **kwargs)` обеспечивает корректную инициализацию базовой формы.

Использование `AuthenticationForm` значительно упрощает логику входа, так как она уже содержит механизм для проверки имени пользователя и пароля, а также для получения объекта пользователя в случае успешной аутентификации.

В следующей части мы рассмотрим, как эти специализированные формы используются во вьюшках для обработки запросов регистрации и входа, а также как они взаимодействуют с шаблонами.

---

### Вьюшки: Сердце Аутентификации 🔑

После того как мы подготовили специализированные формы для регистрации и авторизации, настало время обновить наши вьюшки. Эти функции будут использовать новые формы, чтобы упростить логику обработки запросов, создания пользователей и управления сессиями.

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("landing")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth_login(request, user)
                return redirect(request.GET.get("next", "landing"))
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@require_POST
def logout(request):
    auth_logout(request)
    return redirect("landing")
```

Рассмотрим каждую функцию-вью по отдельности.

#### Функция `register` 📝

Функция `register` отвечает за обработку процесса регистрации нового пользователя. Она значительно упрощается благодаря использованию `CustomUserCreationForm`, которая уже умеет создавать пользователя.

При получении `POST`-запроса (то есть, когда пользователь отправляет форму регистрации), создается экземпляр `CustomUserCreationForm` и передаются данные из `request.POST`. Если форма проходит валидацию (`form.is_valid()` возвращает `True`), то метод `form.save()` автоматически создает нового пользователя в базе данных. После успешного создания пользователя, функция `auth_login(request, user)` из `django.contrib.auth` немедленно авторизует его, создавая сессию. Затем происходит перенаправление на страницу с именем маршрута `landing`.

В случае `GET`-запроса (когда пользователь просто открывает страницу регистрации), создается пустой экземпляр `CustomUserCreationForm`, который затем передается в шаблон `users/register.html` для отображения формы.

>[!info]
>
>#### Упрощение регистрации 🚀
>
>Использование `CustomUserCreationForm` значительно упрощает код вьюшки `register`. Вместо ручного извлечения данных из `form.cleaned_data` и вызова `User.objects.create_user()`, достаточно просто вызвать `form.save()`. Это возможно благодаря тому, что `UserCreationForm` (от которой наследуется наша кастомная форма) уже содержит логику для сохранения пользователя.

#### Функция `login` 🚪

Функция `login` обрабатывает запросы на вход пользователя в систему. Она также использует специализированную форму — `CustomAuthenticationForm`.

Когда приходит `POST`-запрос, создается экземпляр `CustomAuthenticationForm`. Важно отметить, что `AuthenticationForm` (родительская для нашей кастомной формы) требует передачи объекта `request` первым аргументом, а затем данные `request.POST` через именованный аргумент `data`. После создания формы выполняется её валидация. Если данные корректны (`form.is_valid()`), метод `form.get_user()` возвращает объект пользователя, который был успешно аутентифицирован. Затем функция `auth_login(request, user)` авторизует этого пользователя, устанавливая его сессию.

Перенаправление после входа происходит с учетом параметра `next`. Если в URL был передан параметр `next` (например, `/users/login/?next=/profile/`), это означает, что пользователь пытался получить доступ к защищенной странице, был перенаправлен на вход, и после успешной авторизации должен вернуться на исходную страницу. Если параметр `next` отсутствует, пользователь перенаправляется на страницу `landing` по умолчанию.

В случае `GET`-запроса, создается пустой экземпляр `CustomAuthenticationForm`, который передается в шаблон `users/login.html` для отображения формы входа.

>[!highlight]
>
>#### Параметр `next` для удобства пользователя 🧭
>
>Использование параметра `request.GET.get("next", "landing")` является стандартной практикой в Django для улучшения пользовательского опыта. Это позволяет пользователю после успешного входа автоматически вернуться на страницу, с которой он был перенаправлен на форму авторизации, вместо того чтобы всегда попадать на одну и ту же страницу.

#### Функция `logout` ⛔

Функция `logout` отвечает за выход пользователя из системы, завершая его сессию.

Ключевой особенностью этой функции является использование декоратора `@require_POST` из `django.views.decorators.http`. Этот декоратор гарантирует, что данная вьюшка будет обрабатывать **только** `POST`-запросы. Это важная мера безопасности, предотвращающая случайный выход пользователя из системы при переходе по обычной ссылке (`GET`-запрос), что могло бы произойти, например, если поисковый робот или вредоносный скрипт попытается "пройти" по всем ссылкам на сайте.

Внутри функции `auth_logout(request)` из `django.contrib.auth` очищает сессию текущего пользователя, эффективно "разлогинивая" его. После этого пользователь перенаправляется на страницу `landing`.

>[!warning]
>
>#### Важность `@require_POST` для `logout` 🛡️
>
>Применение `@require_POST` для функции выхода (`logout`) критически важно для безопасности. Без него злоумышленник мог бы создать на своём сайте ссылку на ваш `/users/logout/`, и любой пользователь, перешедший по этой ссылке, был бы автоматически разлогинен на вашем сайте, что является примером атаки CSRF (Cross-Site Request Forgery) или просто плохим пользовательским опытом. `POST`-запрос требует явной отправки формы, что предотвращает подобные нежелательные действия.

Эти обновленные вьюшки, работающие в связке с ранее созданными специализированными формами, обеспечивают более чистый, безопасный и идиоматический подход к реализации аутентификации в Django-приложении.
