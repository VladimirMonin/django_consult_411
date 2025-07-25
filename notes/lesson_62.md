## Кастомизация Админпанели Django 🎨

Админпанель Django — это мощный инструмент для управления данными вашего проекта, но её стандартный вид может показаться слишком простым. Кастомизация позволяет не только улучшить внешний вид, сделав его более современным и соответствующим вашему бренду, но и повысить удобство использования для администраторов. Это особенно важно в 2025 году, когда ожидания от пользовательских интерфейсов значительно выросли.

### Обзор вариантов 🛠️

На рынке существует несколько готовых решений для стилизации админпанели Django. Мы рассмотрим два популярных варианта, которые предлагают различные подходы к кастомизации.

**Django Volt** — это бесплатный и настраиваемый шаблон, основанный на `Bootstrap 5`. Он предлагает чистый и элегантный дизайн, а также простую интеграцию в ваш проект. Среди его ключевых особенностей — современный дизайн на основе `Bootstrap 5`, открытый исходный код и включение различных UI-компонентов, таких как чарты и виджеты. Важно отметить, что `Django Volt` полностью совместим с `Django 5.x`.

**Django Jazzmin** — это ещё одна популярная тема, которая придает админке более профессиональный и корпоративный вид, основываясь на `AdminLTE 3` и `Bootstrap 4`. `Django Jazzmin` предлагает большое количество опций для кастомизации, удобное боковое меню и различные цветовые схемы. Сообщество активно поддерживает этот пакет, и его совместимость с `Django 5.x` постоянно обновляется.

При выборе библиотеки всегда рекомендуется проверять их официальные страницы на `GitHub` или `PyPI` для получения самой актуальной информации о последних обновлениях, документации и статусе поддержки текущих версий Django.

### Установка и настройка Django Jazzmin 🚀

Для нашего курса мы будем использовать `Django Jazzmin`, так как он предоставляет обширные возможности для кастомизации, что позволит нам глубже погрузиться в процесс настройки админпанели.

Первым шагом является установка пакета. Мы будем использовать `Poetry` для управления зависимостями проекта. Откройте терминал в корневой директории вашего проекта и выполните следующую команду:

```bash
poetry add django-jazzmin
```

После успешной установки пакета необходимо добавить `jazzmin` в список установленных приложений вашего проекта. Откройте файл `settings.py` и внесите изменения в список `INSTALLED_APPS`, разместив `jazzmin` в самом начале:

```python
# settings.py

INSTALLED_APPS = [
    'jazzmin', # Добавляем Jazzmin в начало списка
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ... другие ваши приложения
]
```

>[!info]
>
>#### Важность порядка 💡
>
>Размещение `jazzmin` в начале списка `INSTALLED_APPS` гарантирует, что его шаблоны и статические файлы будут загружены раньше, чем стандартные шаблоны Django, что позволит ему корректно переопределить внешний вид админпанели.

После добавления `jazzmin` в `INSTALLED_APPS` вам потребуется выполнить миграции базы данных, чтобы убедиться, что все необходимые изменения применены:

```bash
python manage.py migrate
```

Теперь, если вы запустите сервер разработки (`python manage.py runserver`) и перейдете в админпанель (`/admin/`), вы увидите, что её внешний вид изменился. В следующих разделах мы подробно рассмотрим, как настроить `Django Jazzmin` под ваши нужды, изменяя цвета, логотипы, ссылки и многое другое.

### Встроенная система пользователей и разрешений в Django 🔐

Продолжая тему админпанели, важно понимать, как Django управляет доступом к данным. Встроенная система пользователей и разрешений — это мощный механизм, который позволяет гибко контролировать, кто и что может делать в вашем приложении. Это основа безопасности и разграничения ролей, будь то администратор, редактор или обычный пользователь.

Django поставляется с модулем `django.contrib.auth`, который предоставляет все необходимые инструменты для работы с пользователями, группами и разрешениями. Вам не нужно изобретать велосипед для базовой аутентификации и авторизации.

#### Пользователи и Группы 👥

В Django каждый, кто взаимодействует с системой, является `пользователем`. Пользователи могут быть как обычными посетителями сайта, так и администраторами, работающими в админпанели. Каждый пользователь имеет уникальное имя, пароль и может быть связан с различными разрешениями.

Для упрощения управления разрешениями Django предлагает концепцию `групп`. Группа — это набор пользователей, которым назначены одинаковые разрешения. Например, вы можете создать группу "Редакторы", дать ей разрешения на изменение статей, а затем просто добавлять новых редакторов в эту группу, вместо того чтобы назначать разрешения каждому по отдельности. Это значительно упрощает администрирование больших проектов.

![django_permissions.png](./images/django_permissions.png)

#### Разрешения и CRUD-операции 📝

Самое интересное начинается с разрешений. Django автоматически создает набор разрешений для каждой модели, которую вы регистрируете в админпанели. Эти разрешения соответствуют основным операциям с данными, известным как CRUD:

* **C**reate (создание)
* **R**ead (чтение)
* **U**pdate (обновление)
* **D**elete (удаление)

Для каждой модели Django генерирует четыре стандартных разрешения:

* `add_<model_name>`: Разрешение на создание новых объектов модели.
* `change_<model_name>`: Разрешение на изменение существующих объектов модели.
* `delete_<model_name>`: Разрешение на удаление объектов модели.
* `view_<model_name>`: Разрешение на просмотр объектов модели.

Например, если у вас есть модель `Review` (Отзыв), Django автоматически создаст разрешения `add_review`, `change_review`, `delete_review` и `view_review`.

На изображении, которое мы рассматривали ранее, вы можете увидеть, как эти разрешения отображаются в админпанели при настройке прав для пользователя или группы.

Здесь видно, что для приложения "Арбуз" и модели "Отзыв" доступны следующие права:

* `Can add review` (соответствует `add = create`)
* `Can change review` (соответствует `change = update`)
* `Can delete review` (соответствует `delete = delete`)
* `Can view review` (соответствует `view = read`)

>[!highlight]
>
>#### Важность `view` разрешения 👁️
>
>Начиная с Django 2.1, было добавлено разрешение `view_<model_name>`. Это позволяет более гранулированно контролировать доступ: пользователь может видеть список объектов, но не иметь возможности их изменять или удалять. Это очень полезно для создания ролей, которым нужен только доступ для чтения.

Эти разрешения могут быть назначены как отдельным пользователям, так и целым группам. Когда пользователь пытается выполнить какое-либо действие в админпанели (или даже в вашем собственном коде), Django проверяет, есть ли у него соответствующее разрешение. Если разрешения нет, доступ будет запрещен.

В следующих разделах мы углубимся в то, как создавать пользователей и группы, назначать им разрешения, а также как использовать эти разрешения в ваших собственных представлениях и шаблонах для создания по-настоящему безопасных и управляемых приложений.

### Знакомство с Django Signals 🚦

В процессе разработки приложений на Django часто возникает необходимость выполнять определённые действия в ответ на события, происходящие в системе. Например, отправить уведомление после сохранения объекта в базе данных или обновить связанные данные после его удаления. Для решения таких задач в Django существует мощный механизм, называемый `Signals` (Сигналы).

#### Что это такое? 📡

`Django Signals` — это система, которая позволяет различным частям вашего приложения получать уведомления о происходящих событиях и реагировать на них. Это своего рода "издательско-подписная" модель: когда происходит определённое событие (например, сохранение модели), оно "издаёт" сигнал, а другие части кода, которые "подписаны" на этот сигнал, могут "получить" его и выполнить свою логику.

#### Для чего они используются? 🎯

Основное назначение сигналов — это обеспечение слабой связанности (decoupling) между компонентами вашего приложения. Вместо того чтобы жёстко встраивать логику в методы моделей или представлений, вы можете вынести её в отдельные функции, которые будут реагировать на сигналы. Это делает код более модульным, читаемым и лёгким для поддержки.

Представьте, что у вас есть модель `Order` (Заказ), как в нашем примере. Когда статус заказа меняется на "Выполнена", вам может потребоваться отправить клиенту SMS, обновить статистику мастера (`Master`) и записать это событие в лог. Без сигналов вам пришлось бы вставлять всю эту логику непосредственно в метод сохранения заказа или в представление, обрабатывающее его изменение. С сигналами же вы можете создать отдельные функции для каждого из этих действий и "подписать" их на сигнал, который отправляется после сохранения заказа.

#### Централизованная точка входа для разных событий в приложении 🌐

Сигналы выступают как централизованная точка, через которую проходят уведомления о важных событиях в приложении. Это позволяет вам легко добавлять новую функциональность, реагирующую на существующие события, без изменения уже написанного кода. Если в будущем вам понадобится добавить ещё одно действие при изменении статуса заказа, вы просто создадите новую функцию-обработчик и подключите её к соответствующему сигналу, не затрагивая логику модели `Order`.

#### Какие вещи можно отслеживать? 🔍

Django предоставляет набор встроенных сигналов, которые охватывают большинство распространённых событий, связанных с моделями и запросами:

* **Сигналы модели**: Эти сигналы срабатывают до или после операций с объектами моделей.
  * `pre_save` и `post_save`: Срабатывают до и после сохранения объекта модели. Например, вы можете использовать `post_save` для модели `Order`, чтобы отправить уведомление, когда заказ был создан или обновлён. Или для модели `Review`, чтобы пересчитать средний рейтинг `Master` после добавления нового отзыва.
  * `pre_delete` и `post_delete`: Срабатывают до и после удаления объекта модели. Это может быть полезно, например, для очистки связанных файлов или данных перед удалением `Master` или `Service`.
  * `m2m_changed`: Срабатывает при изменении связей "многие ко многим" (`ManyToManyField`). В наших моделях это актуально для связи `Master` с `Service` или `Order` с `Service`. Вы можете отслеживать, когда мастеру добавляется новая услуга или когда в заказ добавляются или удаляются услуги.
* **Сигналы запросов**:
  * `request_started` и `request_finished`: Срабатывают в начале и конце обработки каждого HTTP-запроса.
* **Сигналы базы данных**:
  * `pre_init` и `post_init`: Срабатывают до и после инициализации объекта модели.

>[!info]
>
>#### Пользовательские сигналы ⚙️
>
>Помимо встроенных, вы также можете создавать свои собственные сигналы для любых событий, специфичных для вашего приложения. Это даёт полную гибкость в организации взаимодействия между различными частями вашей системы.

В следующем разделе мы рассмотрим, как на практике подключать функции-обработчики к этим сигналам и использовать их для добавления функциональности в наше приложение.

## Большая сводная таблица со всеми вариантами сигналов 📊

Как мы уже выяснили, сигналы — это мощный инструмент для создания слабосвязанной архитектуры. Чтобы систематизировать знания, давайте рассмотрим основные встроенные сигналы Django в виде сводной таблицы. Мы разделим их по группам и приведем примеры, как их можно было бы применить в нашем приложении для салона красоты.

| Группа сигналов | Сигнал | Описание | Пример использования в нашем приложении |
| :--- | :--- | :--- | :--- |
| **Сигналы моделей** | `pre_init` | Отправляется в начале метода `__init__` модели. | Установить какое-то временное значение для поля объекта `Order` перед его полной инициализацией. |
| (`django.db.models.signals`) | `post_init` | Отправляется в конце метода `__init__` модели. | Логировать факт загрузки конкретного объекта `Master` из базы данных для отладки. |
| | `pre_save` | Отправляется перед вызовом метода `save()` модели. | Перед сохранением `Order`, проверить доступность `Master` на выбранное время. |
| | `post_save` | Отправляется после вызова метода `save()` модели. | После сохранения нового `Review`, пересчитать средний рейтинг для связанного `Master`. |
| | `pre_delete` | Отправляется перед вызовом метода `delete()` модели. | Перед удалением `Service`, проверить, не входит ли она в активные `Order`, и, возможно, запретить удаление. |
| | `post_delete` | Отправляется после вызова метода `delete()` модели. | После удаления `Master`, отправить email-уведомление администратору. |
| | `m2m_changed` | Отправляется при изменении `ManyToManyField`. | Когда к `Master` добавляется новая `Service`, отправить ему уведомление об обновлении его профиля. |
| **Сигналы запросов** | `request_started` | Отправляется, когда Django начинает обрабатывать HTTP-запрос. | Запускать таймер для измерения общего времени обработки запроса. |
| (`django.core.signals`) | `request_finished` | Отправляется, когда Django завершает обработку HTTP-запроса. | Останавливать таймер и логировать общее время обработки запроса для мониторинга производительности. |
| | `got_request_exception` | Отправляется при возникновении исключения во время обработки запроса. | Отправить детальную информацию об ошибке в систему мониторинга (например, Sentry) для быстрой реакции. |
| **Сигналы управления** | `pre_migrate` | Отправляется перед запуском команды `migrate`. | Сделать резервную копию базы данных перед применением миграций. |
| (`django.core.management.signals`) | `post_migrate` | Отправляется после выполнения команды `migrate`. | Автоматически создать группы пользователей по умолчанию (`Администраторы`, `Мастера`) после миграции. |
| **Сигналы тестов** | `setting_changed` | Отправляется, когда значение настройки изменяется в тестах. | При изменении настройки `TIME_ZONE` в тестах, очистить кеш, который зависит от часового пояса. |
| (`django.test.signals`) | `template_rendered` | Отправляется, когда тестовый рендерер отрисовывает шаблон. | В тестах проверять, что в контекст шаблона для страницы `Order` передаются правильные данные. |
| **Сигналы базы данных** | `connection_created` | Отправляется после установки соединения с базой данных. | Установить специфичные для сессии параметры соединения, например, уровень изоляции транзакций. |

>[!warning]
>
>#### Осторожность с сигналами ⚠️
>
>Сигналы — это мощный, но и потенциально опасный инструмент. Старайтесь не размещать в обработчиках сигналов сложную бизнес-логику. Это может сделать поведение системы непредсказуемым и трудным для отладки, так как логика оказывается "спрятанной" от основного потока выполнения кода (например, от методов модели или представлений). Для простых задач, вроде отправки уведомлений или очистки кеша, они подходят идеально.

### Мы будем делать модерацию отзывов 🛡️

Пользовательские отзывы (`Review`) — это ценный источник обратной связи, но они также могут стать площадкой для спама, оскорблений или публикации нежелательного контента. Чтобы поддерживать здоровую атмосферу на нашем сайте и снизить нагрузку на администраторов, мы внедрим автоматическую модерацию контента с помощью искусственного интеллекта. Для этой задачи мы воспользуемся возможностями платформы Mistral AI.

Первым делом необходимо установить официальную библиотеку для взаимодействия с API Mistral. Если вы используете `poetry` для управления зависимостями, команда будет выглядеть так:

```bash
poetry add mistralai
```

Для работы с API нам потребуется ключ, который можно бесплатно получить на официальном сайте Mistral после регистрации. Подробную информацию о возможностях модерации можно найти в [официальной документации](https://docs.mistral.ai/capabilities/guardrailing/).

>[!info]
>
>#### Безопасность ключей API 🔑
>
>Никогда не храните секретные ключи, пароли или другие чувствительные данные прямо в коде или в системе контроля версий (Git). Файл `.env` специально для этого и игнорируется Git (через `.gitignore`), а `.env.example` служит шаблоном, который показывает, какие переменные окружения нужны для работы проекта.

Полученный ключ следует добавить в файл `.env` в корне вашего проекта:

`MISTRAL_API_KEY='Ваш_секретный_ключ'`

Не забудьте также обновить файл `.env.example`, чтобы другие разработчики знали о необходимости этой переменной окружения, но оставьте значение пустым:

`MISTRAL_API_KEY=`

Теперь настроим чувствительность нашей системы модерации. Mistral AI проверяет текст по нескольким категориям. Мы можем задать для каждой из них пороговое значение от 0 до 1. Чем ниже значение, тем строже будет проверка. Добавим в файл `settings.py` нашего проекта словарь с этими настройками:

```python
# settings.py

# ... другие настройки

MISTRAL_MODERATIONS_GRADES = {
    "hate_and_discrimination": 0.1,  # ненависть и дискриминация
    "sexual": 0.1,  # сексуальный
    "violence_and_threats": 0.1,  # насилие и угрозы
    "dangerous_and_criminal_content": 0.1,  # опасный и криминальный контент
    "selfharm": 0.1,  # самоповреждение
    "health": 0.1,  # здоровье
    "financial": 0.1,  # финансовый
    "law": 0.1,  # закон
    "pii": 0.1,  # личная информация (personally identifiable information)
}
```

Итак, мы подготовили необходимую базу: установили библиотеку, настроили безопасный доступ к API и определили параметры модерации. В следующем разделе мы напишем код, который будет использовать эти настройки для автоматической проверки текста отзывов.

**Exploring Content Moderation**

### Логика модерации контента 🔍

После того как мы подготовили окружение, самое время написать код, который будет выполнять основную работу — отправлять текст отзыва на проверку в Mistral AI и принимать решение о его "токсичности". Для этого мы создадим отдельный модуль в нашем проекте. Хорошей практикой является создание общего приложения, например, `core`, для хранения такой вспомогательной логики, которая может быть использована в разных частях проекта. Итак, мы создали файл `core/mistral.py`.

Вот полный код этого модуля, который мы затем детально разберем.

```python
# core/mistral.py

# импорт из настроек MISTRAL_MODERATIONS_GRADES
from barbershop.settings import MISTRAL_MODERATIONS_GRADES
import os
from dotenv import load_dotenv
from mistralai import Mistral
from pprint import pprint


load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def is_bad_review(
    review_text: str,
    api_key: str = MISTRAL_API_KEY,
    grades: dict = MISTRAL_MODERATIONS_GRADES,
) -> bool:
    # Создаем клиента Mistral с переданным API ключом
    client = Mistral(api_key=api_key)

    # Формируем запрос
    response = client.classifiers.moderate_chat(
        model="mistral-moderation-latest",
        inputs=[{"role": "user", "content": review_text}],
    )
    # Вытаскиваем данные с оценкой
    result = response.results[0].category_scores

    # Округляем значения до двух знаков после запятой для удобства отладки
    result = {key: round(value, 2) for key, value in result.items()}

    pprint(result) # Используем для отладки, чтобы видеть оценки

    # Словарь под результаты проверки
    checked_result = {}

    for key, value in result.items():
        if key in grades:
            checked_result[key] = value >= grades[key]

    # Если одно из значений True, то отзыв не проходит модерацию
    return any(checked_result.values())


if __name__ == "__main__":
    print(
        is_bad_review("Классно подстригли. Меня зовут Семен, номер телефона +79111111111")
    )
```

#### Как это работает: пошаговый разбор

1. **Импорты и настройка**. В самом начале мы импортируем необходимые компоненты:
    * `MISTRAL_MODERATIONS_GRADES`: наш словарь с порогами чувствительности из `settings.py`.
    * `os`, `load_dotenv`: стандартные инструменты для работы с переменными окружения. Функция `load_dotenv()` загружает переменные из файла `.env`.
    * `Mistral`: основной класс из библиотеки `mistralai` для создания клиента API.
    * `pprint`: модуль для "красивой" печати сложных структур данных, полезен для отладки.

2. **Загрузка API ключа**. Строки `load_dotenv()` и `MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")` считывают наш секретный ключ из файла `.env` и сохраняют его в переменную.

3. **Функция `is_bad_review`**. Это ядро нашего модуля.
    * **Сигнатура функции**: она принимает текст отзыва (`review_text`) и возвращает булево значение (`True`, если отзыв "плохой", и `False`, если "хороший"). Параметры `api_key` и `grades` имеют значения по умолчанию, что делает функцию удобной для использования.
    * **Создание клиента**: `client = Mistral(api_key=api_key)` инициализирует клиент для взаимодействия с API Mistral, используя наш ключ.
    * **Запрос к API**: `client.classifiers.moderate_chat(...)` — это вызов метода модерации. Мы передаем ему модель (`mistral-moderation-latest`) и сам текст в виде списка словарей.
    * **Обработка ответа**: API возвращает сложный объект. Нас интересует поле `category_scores`, которое содержит словарь с оценками по каждой категории (например, `'pii': 0.95`, `'sexual': 0.01` и т.д.). Мы извлекаем этот словарь.
    * **Отладка**: `pprint(result)` выводит в консоль полученные оценки. Это очень удобно на этапе разработки, чтобы понимать, как модель реагирует на разные тексты. В продакшене эту строку можно будет убрать.

>[!highlight]
>
>#### Ключевая логика проверки
>
>Самое важное происходит в цикле `for` и строке с `return`:
>
>1. Мы итерируемся по оценкам, полученным от Mistral (`result`).
>2. Для каждой категории мы сравниваем полученную оценку (`value`) с нашим пороговым значением из `settings.py` (`grades[key]`). Например, если для категории `pii` (личная информация) мы получили оценку `0.95`, а наш порог `0.1`, то сравнение `0.95 >= 0.1` вернет `True`.
>3. Результаты всех сравнений (`True` или `False`) сохраняются в словарь `checked_result`.
>4. Функция `any(checked_result.values())` возвращает `True`, если **хотя бы одно** из значений в словаре `checked_result` равно `True`. Это означает, что текст превысил порог хотя бы по одной категории и, следовательно, считается "плохим".

4. **Блок `if __name__ == "__main__"`**. Этот стандартный для Python блок позволяет запустить файл как самостоятельный скрипт для тестирования. В нашем примере мы проверяем фразу, содержащую личные данные (имя и телефон). Ожидается, что модель присвоит высокую оценку по категории `pii`, и функция вернет `True`.

### Обновление модели 📝

Теперь, когда у нас есть функция для проверки текста, нам нужно место, где мы будем хранить результат этой проверки. Простого флага "опубликован / не опубликован" (`is_published`) уже недостаточно. Нам нужен полноценный статус, который будет отслеживать состояние модерации каждого отзыва. Для этого мы обновим нашу модель `Review`.

Мы добавим новое поле `ai_checked_status`, которое будет хранить один из нескольких возможных статусов. Это позволит нам точно знать, был ли отзыв проверен, находится ли он в процессе, отклонен или еще даже не поступал на проверку.

Вот как будет выглядеть обновленная модель `reviews/models.py`:

```python
class Review(models.Model):

    RATING_CHOICES = [
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    ]

    AI_CHOICES = [
        ("ai_checked_true", "Проверено ИИ"),
        ("ai_cancelled", "Отменено ИИ"),
        ("ai_checked_in_progress", "В процессе проверки"),
        ("ai_checked_false", "Не проверено"),
    ]

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Имя клиента"
    )
    master = models.ForeignKey(
        Master, on_delete=models.SET_NULL, null=True, verbose_name="Мастер"
    )
    photo = models.ImageField(
        upload_to="reviews/", blank=True, null=True, verbose_name="Фотография"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка", choices=RATING_CHOICES, default=5
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    ai_checked_status = models.CharField(
        max_length=30,
        choices=AI_CHOICES,
        default="ai_checked_false",
        verbose_name="Статус ИИ",
    )
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
```

Ключевое изменение здесь — добавление поля `ai_checked_status`.

>[!info]
>
>#### Как работает `choices` в Django?
>
>Параметр `choices` — это удобный способ создать выпадающий список в админке Django и ограничить возможные значения для поля. Он принимает список кортежей. В каждом кортеже:
>
>* Первый элемент (`"ai_checked_true"`) — это значение, которое хранится в базе данных.
>* Второй элемент (`"Проверено ИИ"`) — это человекочитаемое название, которое отображается пользователю.
>
>Это позволяет хранить в базе данных короткие и эффективные строковые идентификаторы, а в интерфейсе показывать понятные описания.

После внесения изменений в модель необходимо сообщить Django об этих изменениях и применить их к базе данных. Это делается с помощью двух команд:

```bash
# Создаем файл миграции
poetry run python manage.py makemigrations

# Применяем миграцию к базе данных
poetry run python manage.py migrate
```

Теперь наша база данных готова к хранению статусов модерации. В следующем шаге мы свяжем нашу функцию `is_bad_review` с процессом сохранения отзыва, чтобы проверка запускалась автоматически.

### Логика сигнала 🚦

Мы подготовили модель для хранения статусов и функцию для проверки. Но как запустить эту проверку автоматически каждый раз, когда пользователь оставляет новый отзыв? Мы же не хотим вручную вызывать наш скрипт. Здесь на помощь приходят **сигналы Django**.

Сигнал — это механизм, который позволяет одним частям приложения получать уведомления о действиях, происходящих в других частях. В нашем случае мы хотим "услышать" событие сохранения нового отзыва в базу данных и в ответ запустить нашу функцию модерации. Для этого мы будем использовать сигнал `post_save`.

Вот код, который мы разместим в новом файле `reviews/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from core.mistral import is_bad_review


@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    # Created - это флаг, который показывает, что запись была создана
    if created:
        # Меняем статус на ai_checked_in_progress
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save()

        # Отправляем на проверку
        review_text = instance.text
        if is_bad_review(review_text):
            instance.ai_checked_status = "ai_cancelled"
        else:
            instance.ai_checked_status = "ai_checked_true"
```

#### Как это работает

Давайте разберем, как работает этот механизм.

1. **Декоратор `@receiver`**: Это "подписчик" на события. Мы говорим Django: "Когда произойдет событие `post_save` от модели `Review`, вызови, пожалуйста, функцию `check_review`".
    * `post_save`: Сигнал, который отправляется *после* того, как метод `save()` модели был успешно выполнен.
    * `sender=Review`: Мы указываем, что нас интересуют события сохранения только от модели `Review`.

2. **Аргументы функции**:
    * `instance`: Это самый важный для нас аргумент. Он содержит конкретный объект модели, который был только что сохранен. В нашем случае — это новый отзыв.
    * `created`: Это булев флаг. Он равен `True`, если объект был создан впервые, и `False`, если объект был обновлен.

3. **Проверка `if created:`**: Это ключевая проверка. Мы хотим запускать модерацию только для **новых** отзывов. Без этой проверки наш код срабатывал бы каждый раз при любом изменении отзыва (например, когда администратор меняет его статус вручную), что привело бы к лишним запросам к API и ненужной работе.

4. **Процесс модерации**:
    * Сначала мы меняем статус отзыва на `"ai_checked_in_progress"` и сразу же сохраняем его. Это хорошая практика: если проверка займет несколько секунд, в системе уже будет видно, что отзыв находится в обработке.
    * Затем мы вызываем нашу функцию `is_bad_review()`, передавая ей текст отзыва (`instance.text`).
    * В зависимости от результата (`True` или `False`) мы присваиваем полю `ai_checked_status` финальное значение: `"ai_cancelled"` (отклонено) или `"ai_checked_true"` (проверено и одобрено).

>[!warning]
>
>#### Важный момент: финальное сохранение
>
>В приведенном коде есть логическая ошибка, которую часто допускают новички. После присвоения финального статуса (`ai_cancelled` или `ai_checked_true`) **не происходит сохранения в базу данных**. Изменение остается только в памяти объекта `instance`. Чтобы исправить это, нужно добавить еще один вызов `instance.save()` в конце блока `if`. Без этого статус отзыва навсегда останется `"ai_checked_in_progress"`.

#### Как подключать сигналы

Чтобы Django узнал о нашем файле `signals.py` и начал его использовать, недостаточно просто создать файл. Рекомендуемый способ — зарегистрировать сигналы в конфигурации приложения.

1. Убедитесь, что у вас есть файл `reviews/apps.py`. В нем нужно переопределить метод `ready()`.

    ```python
    # reviews/apps.py
    from django.apps import AppConfig

    class ReviewsConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'reviews'

        def ready(self):
            import reviews.signals  # noqa
    ```

2. Далее, в файле `reviews/__init__.py` нужно указать путь к этой конфигурации.

    ```python
    # reviews/__init__.py
    default_app_config = 'reviews.apps.ReviewsConfig'
    ```

После этих действий Django при запуске будет знать, что для приложения `reviews` нужно выполнить код из метода `ready()`, который, в свою очередь, импортирует наши сигналы и зарегистрирует их в системе.
