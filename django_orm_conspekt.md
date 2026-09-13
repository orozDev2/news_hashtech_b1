# Django ORM: QuerySet и лукапы — подробный конспект

Разбор построен на твоих моделях: `Category`, `Tag`, `NewsLinks`, `NewsImage`, `News`.
Напомню связи между ними:

- `News.category` — `ForeignKey` на `Category` (один-ко-многим: у категории много новостей)
- `News.tags` — `ManyToManyField` на `Tag` (многие-ко-многим)
- `News.images` (related_name у `NewsImage.news`) — `ForeignKey`, одна новость — много изображений
- `News.link` (related_name у `NewsLinks.news`) — `OneToOneField`, одна новость — одна запись ссылок

Все примеры пиши в Django shell (`python manage.py shell`) или в отдельном скрипте — так удобнее экспериментировать.

---

## 1. Что такое QuerySet

`QuerySet` — это **список объектов из базы данных**, который Django не грузит сразу, а только когда он реально нужен (лениво, *lazy evaluation*).

```python
qs = News.objects.all()  # запрос в БД ЕЩЁ НЕ отправлен
print(qs)  # а вот тут — отправлен, потому что мы пытаемся вывести результат
```

`objects` — это менеджер модели, через него всегда начинается любой запрос: `Модель.objects.метод()`.

QuerySet можно **склеивать в цепочку** — каждый метод фильтрации возвращает новый QuerySet, к которому можно применить следующий метод:

```python
News.objects.filter(category__name='Спорт').exclude(views=0).order_by('-date')
```

---

## 2. Базовые методы QuerySet

### `all()`

Возвращает все объекты модели.

```python
News.objects.all()
# <QuerySet [<News: Открытие нового парка>, <News: Курс доллара вырос>, ...]>
```

### `get()`

Возвращает **ровно один объект**. Если найдено 0 или больше 1 — будет исключение.

```python
news = News.objects.get(pk=1)
category = Category.objects.get(name='Политика')
```

⚠️ Важные исключения:

```python
News.objects.get(id=9999)
# News.DoesNotExist: News matching query does not exist.

News.objects.get(category=category)
# News.MultipleObjectsReturned — если новостей с такой категорией несколько
```

Вывод: `get()` используй только тогда, когда точно уверен, что объект один (например, поиск по `id` или `slug`).

### `filter()`

Возвращает QuerySet со **всеми** объектами, подходящими под условие. Может вернуть 0, 1 или много объектов — и это не ошибка.

```python
News.objects.filter(category__name='Спорт')
News.objects.filter(views__gt=100, author='Айгуль')
```

### `exclude()`

Работает как `filter()`, но **наоборот** — возвращает всё, что **не** подходит под условие.

```python
# все новости, кроме новостей автора "Админ"
News.objects.exclude(author='Админ')

# все новости, где категория НЕ "Реклама" и просмотров больше 0
News.objects.exclude(category__name='Реклама').exclude(views=0)
```

### `first()` и `last()`

Возвращают один объект — первый или последний в QuerySet (с учётом сортировки, заданной в `Meta.ordering` или в `.order_by()`).

```python
News.objects.first()  # самая "первая" по ordering новость
News.objects.last()   # самая "последняя"
```

Важно: у `News` в `Meta` задано `ordering = ('-date', '-updated_at')`, значит:

```python
News.objects.first()
# вернёт САМУЮ СВЕЖУЮ новость (т.к. сортировка идёт по убыванию даты)
```

Если `ordering` не задан — Django не гарантирует порядок, и `first()`/`last()` могут возвращать непредсказуемые результаты. Лучше явно указывать `.order_by()`.

В отличие от `get()`, `first()` и `last()` **не кидают исключение**, если объектов нет — просто вернут `None`.

```python
result = News.objects.filter(author='Несуществующий').first()
print(result)  # None
```

### `order_by()`

Сортировка. Знак `-` перед полем — сортировка по убыванию.

```python
News.objects.order_by('title')            # по алфавиту А→Я
News.objects.order_by('-views')           # сначала самые просматриваемые
News.objects.order_by('category', '-date')  # сначала по категории, потом внутри неё — по дате (новые сверху)
```

### `count()`

Возвращает **число** объектов — быстрее, чем `len(queryset)`, т.к. Django делает `SELECT COUNT(*)` на уровне БД, не загружая сами объекты.

```python
News.objects.count()                       # всего новостей
News.objects.filter(category__name='Спорт').count()  # сколько новостей в категории "Спорт"
```

---

## 3. Лукапы (field lookups) для фильтрации

Синтаксис лукапа: `поле__лукап=значение`. Если лукап не указан — по умолчанию используется `exact`.

### `exact` / `iexact` — точное совпадение

```python
News.objects.filter(title__exact='Открытие нового парка')
# то же самое, что и:
News.objects.filter(title='Открытие нового парка')

News.objects.filter(title__iexact='открытие нового парка')
# найдёт и "Открытие нового парка", и "ОТКРЫТИЕ НОВОГО ПАРКА" — регистр не важен
```

### `contains` / `icontains` — содержит подстроку

```python
News.objects.filter(title__contains='парк')     # регистрозависимо: "Открытие парка" ✅, "ПАРК" ❌
News.objects.filter(title__icontains='парк')    # регистронезависимо: найдёт оба варианта
```

Это твой основной инструмент для поиска по сайту (например, поле поиска новостей).

### `gt`, `gte`, `lt`, `lte` — сравнения

`gt` — greater than (>), `gte` — greater than or equal (>=), `lt` — less than (<), `lte` — less than or equal (<=).

```python
News.objects.filter(views__gt=1000)     # просмотров больше 1000
News.objects.filter(views__gte=1000)    # 1000 и больше
News.objects.filter(views__lt=10)       # меньше 10 просмотров
News.objects.filter(views__lte=10)      # 10 и меньше

# работают и с датами
from django.utils import timezone
News.objects.filter(date__gte=timezone.now() - timezone.timedelta(days=7))  # новости за последнюю неделю
```

### `in` — вхождение в список

```python
News.objects.filter(category__name__in=['Спорт', 'Политика', 'Экономика'])
News.objects.filter(id__in=[1, 5, 9])
```

Полезно, когда список значений формируется динамически (например, из формы или другого запроса).

### `startswith` / `endswith` (и `istartswith` / `iendswith`)

```python
News.objects.filter(title__startswith='Курс')    # заголовок начинается с "Курс"
News.objects.filter(author__endswith='ов')       # фамилия автора заканчивается на "ов"
News.objects.filter(title__istartswith='курс')   # то же самое, но без учёта регистра
```

### `isnull` — проверка на NULL

```python
News.objects.filter(category__isnull=True)   # новости без категории (у тебя category — null=True)
News.objects.filter(image__isnull=False)     # новости, у которых ЕСТЬ картинка
News.objects.filter(link__whatsapp__isnull=True)  # у которых не заполнен whatsapp в ссылках
```

⚠️ Частая ошибка новичков: `isnull=True` — это НЕ то же самое, что `''` (пустая строка). Для `blank=True` текстовых полей может понадобиться отдельно проверять `''`.

### Лукапы для дат: `date`, `year`, `month`, `day`, `time`

У `News.date` тип `DateTimeField`, поэтому доступны все эти лукапы:

```python
import datetime

News.objects.filter(date__year=2026)              # все новости 2026 года
News.objects.filter(date__month=9)                 # все новости за сентябрь (любого года)
News.objects.filter(date__day=9)                    # все новости, опубликованные 9-го числа
News.objects.filter(date__date=datetime.date(2026, 9, 9))  # новости конкретно за 9 сентября 2026

News.objects.filter(date__year=2026, date__month=9)  # можно комбинировать: сентябрь 2026
```

`time` — работает так же, но для времени (часы:минуты:секунды):

```python
News.objects.filter(date__time__gte=datetime.time(9, 0))   # опубликованы после 9:00 утра
```

Также есть более "мелкие" лукапы, если понадобятся: `date__hour`, `date__minute`, `date__second`, `date__week_day` (день недели, 1=воскресенье).

---

## 4. Работа со связанными моделями (`__`)

Двойное подчёркивание `__` — это способ "пройти" через связь (`ForeignKey`, `ManyToMany`, `OneToOne`) прямо в запросе, без дополнительных `JOIN`-ов вручную.

### Через `ForeignKey` (News → Category)

```python
# все новости категории с именем "Спорт"
News.objects.filter(category__name='Спорт')

# новости, у которых название категории содержит "спорт" (без учёта регистра)
News.objects.filter(category__name__icontains='спорт')

# обратная связь: все новости конкретной категории (через related_name='news')
category = Category.objects.get(name='Спорт')
category.news.all()
```

### Через `ManyToManyField` (News ↔ Tag)

```python
# новости с тегом "экология"
News.objects.filter(tags__name='экология')

# новости с тегами "экология" ИЛИ "экономика" (может задублировать новость, если у неё оба тега сразу — см. distinct() ниже)
News.objects.filter(tags__name__in=['экология', 'экономика']).distinct()

# обратная связь: все теги конкретной новости
news = News.objects.first()
news.tags.all()

# все новости конкретного тега
tag = Tag.objects.get(name='экология')
tag.news.all()
```

⚠️ `distinct()` часто нужен именно с `ManyToMany`-фильтрами: если новость подходит под условие несколько раз (например, содержит сразу два тега из списка), она попадёт в результат несколько раз — `distinct()` уберёт дубли.

### Через `OneToOneField` (News → NewsLinks)

```python
# новости, у которых заполнен telegram в ссылках
News.objects.filter(link__telegram__isnull=False)

# обратный доступ (через related_name='link')
news = News.objects.get(pk=1)
news.link.telegram   # прямое обращение к полю связанной модели
```

### Через обратный `ForeignKey` (News → NewsImage)

```python
# новости, у которых есть хотя бы одно изображение в галерее
News.objects.filter(images__isnull=False).distinct()

# сколько изображений у конкретной новости
news.images.count()
```

---

## 5. Комплексные примеры (цепочки методов + лукапы + связи)

**Пример 1.** Топ-5 самых просматриваемых новостей в категории "Политика" за последний месяц:

```python
News.objects.filter(
    category__name='Политика',
    date__gte=timezone.now() - timezone.timedelta(days=30)
).order_by('-views')[:5]
```

**Пример 2.** Все новости с тегом "выборы", у которых заполнен instagram в ссылках, отсортированные по дате:

```python
News.objects.filter(
    tags__name__iexact='выборы',
    link__instagram__isnull=False
).order_by('-date').distinct()
```

**Пример 3.** Новости без категории или без изображения (кандидаты на "доработку" в админке):

```python
News.objects.filter(category__isnull=True) | News.objects.filter(image__isnull=True)
# объединение двух QuerySet через |
```

**Пример 4.** Заголовки, начинающиеся на "Курс" и опубликованные в 2026 году, но не автора "Админ":

```python
News.objects.filter(
    title__istartswith='курс',
    date__year=2026
).exclude(author='Админ')
```

**Пример 5.** Последняя добавленная новость в каждой категории (более продвинутый пример, для общего понимания — пока можно просто прочитать):

```python
for category in Category.objects.all():
    last_news = category.news.order_by('-date').first()
    print(category.name, '->', last_news)
```

**Пример 6.** Количество новостей по категориям (без агрегации `annotate`, просто через `count()` в цикле — упрощённый вариант для новичка):

```python
for category in Category.objects.all():
    print(category.name, category.news.count())
```

> Когда освоишь эту тему — следующий логичный шаг: `annotate()` и `aggregate()` (например, `Category.objects.annotate(news_count=Count('news'))`), это делает то же самое, но одним запросом к БД вместо цикла. Но это уже отдельная большая тема — пока рано.

---

## 6. Частые ошибки новичков

1. **Путать `get()` и `filter().first()`.** `get()` кидает исключение, если объектов 0 или больше 1. Если не уверен, что объект точно один — используй `filter(...).first()`.
2. **Забывать `distinct()` при фильтрации по `ManyToMany` или обратным `ForeignKey`** — получаются дубли в результате.
3. **Путать `isnull=True` с проверкой на пустую строку `''`.** Это разные вещи для текстовых полей.
4. **Забывать, что QuerySet ленивый** — запрос в БД не уходит, пока не начнёшь реально использовать данные (`print`, `for`, `list()`, `len()` и т.д.). Из-за этого иногда неожиданно выполняется больше запросов к БД, чем кажется.
5. **`order_by()` без учёта `Meta.ordering`** — если у модели уже задан `ordering` в `Meta` (как у `News`), а тебе нужен другой порядок, всегда указывай `.order_by()` явно — он перекрывает `Meta.ordering`.

---

## 7. Что дальше

После того как эти методы и лукапы станут привычными, следующие темы для изучения (по возрастанию сложности):
- `Q` объекты — сложные условия с `OR`/`AND`/`NOT`
- `annotate()` и `aggregate()` — агрегация (`Count`, `Sum`, `Avg`)
- `select_related()` и `prefetch_related()` — оптимизация запросов при работе со связями (очень важно на практике!)
- `values()` и `values_list()` — получение не объектов, а словарей/кортежей
- `bulk_create()`, `bulk_update()` — массовые операции
