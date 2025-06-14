====================================================================
Урок 56 (3 ч): Many-to-Many, расширение модели

Новые сущности

Service, поля: name, price, duration

Master.services  – M2M

Order.services   – M2M blank=True

Цели

• Проектировать и мигрировать M2M

• Управлять связями add/remove/set/clear

• Фильтровать по M2M, проверять «мастер оказывает услугу»

Структура

00-15  Актуализация, ответы по ДЗ

15-40  Теория 1: ManyToManyField, through, blank, null

40-75  Практика 1: создать Service + M2M поля, миграции, admin

75-90  Перерыв

90-110 Теория 2: M2M API, through-model анонс

110-140 Практика 2: shell_plus — выборки, массовое add; доработка шаблона landing с prefetch_related

140-155 Теория 3: Order.services blank=True, валидация «мастер ↔ услуга»

155-175 Практика 3: функция master_provides_service, метод provides() в модели

175-180 Итоги, домашнее: дописать шаблоны, 5 M2M-запросов, подготовить вопросы к формам/валидации

Доп. рекомендации преподавателю

• Live-coding в shell_plus, команды в чат

• Демонстрировать on_delete различия

• При наличии – показать Django-Debug-Toolbar

• Админка: filter_horizontal для M2M


