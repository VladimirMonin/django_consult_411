# Lesson 67. Django Auth Ч2. Регистрация, логин, логаут на классовых инструментах

## Class LogoutView

### Подготовка шаблона

Ранее мы делали элемент меню - форма замаскированная под кнопку для Logout.

```html
<li class="nav-item">
<form action="{% url 'logout' %}" method="post" class="d-inline">
    {% csrf_token %}
    <button type="submit" class="nav-link btn btn-link">Выход</button>
</form>
</li>
```

На функциональной вью работал бы и метод `GET`. Но вот на классовой вью - нет. Пришлось бы делать сложную перенастройку класса. Да и это возможно не очень безопасно.

Поэтому мы сразу подготовили себе почву для работы с классовой вью в будущем.

Теперь мы можем безболезненно перейти на классовую вью с наследованием от `LogoutView`.

### Переход на классовую вью

```python
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

```

# TODO какие атрибуты и методы тут как правило указывают \ переопределяют \ расришряют

## Авторизация на специальных классовых инструментах Django

Для авторизации у Django есть классовые вью и класс формы. Это `LoginView` и `AuthenticationForm`.В Django для авторизации пользователей можно использовать как функциональные, так и классовые вьюхи. Рассмотрим, как это можно сделать с использованием классовых вьюх и классовых форм.

Можно даже так. Но я бы не стал так делать....

```python
# urls.py

from django.urls import path
from django.contrib.auth.views import LoginView
# AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm


urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=AuthenticationForm), name='login'),
]
```

### Кастомная форма `CustomAuthenticationForm` с добавлением BS5

```python
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
```


### Кастомный класс `CustomLoginView`

```python

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'  # Убедитесь, что у вас есть этот шаблон
    success_url = '/'

    # Для messages можно расширить is_valid
```

### Приоритеты перенаправления

#TODO Расписать детально каждый вариант в подзаголовках 4 уровня
1. `next` параметр в URL (например, `?next=/some-url`) - специлизированные вью отрабатывают этот параметр автоматически
2. `success_url` атрибут в классе вью (например, `success_url = '/some-url'`)
3. `get_success_url` метод в классе вью (например, `def get_success_url(self): return '/some-url'`) например для динамического определения маршрута в зависимости от каких либо параметров (например группы пользователя)
4. Специальные константы в `settings.py` для авторизации, логаута и регистрации?

```python
# settings.py

# Маршруты для авторизации
LOGIN_URL = reverse_lazy("login")

# Стандартные переадресации для авторизации, логаута
LOGIN_REDIRECT_URL = reverse_lazy("landing")
LOGOUT_REDIRECT_URL = reverse_lazy("landing")
```