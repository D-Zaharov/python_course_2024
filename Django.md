### Конспект по Django

#### Что такое Django

Django — это высокоуровневый веб-фреймворк на языке Python, который позволяет быстро и легко создавать мощные веб-приложения. Он был разработан для упрощения процесса создания сложных веб-приложений, предоставляя разработчикам все необходимые инструменты «из коробки».

#### Установка Django

Для установки Django используйте команду:

```bash
pip install django
```

#### Создание проекта Django

Для создания нового проекта Django выполните следующую команду:

```bash
django-admin startproject myproject
```

Это создаст структуру проекта со следующими файлами и директориями:

```
myproject/
    manage.py
    myproject/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

##### Описание файлов

- `manage.py`: Утилита командной строки для взаимодействия с проектом Django. С его помощью можно запускать сервер, миграции и другие команды.
- `myproject/`: Внутренняя директория проекта, которая содержит настройки и конфигурацию проекта.
  - `__init__.py`: Пустой файл, который делает директорию пакетом Python.
  - `settings.py`: Файл конфигурации, содержащий все настройки проекта.
  - `urls.py`: Файл маршрутизации URL, который связывает URL-адреса с их обработчиками.
  - `asgi.py`: Конфигурация для асинхронного сервера ASGI.
  - `wsgi.py`: Конфигурация для синхронного сервера WSGI.

#### Запуск проекта

Для запуска сервера разработки используйте команду:

```bash
python manage.py runserver
```

После этого сервер будет доступен по адресу `http://127.0.0.1:8000/`.

#### Создание приложения Django

В рамках проекта можно создать одно или несколько приложений. Для создания нового приложения выполните команду:

```bash
python manage.py startapp myapp
```

Это создаст структуру приложения со следующими файлами и директориями:

```
myapp/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
    migrations/
        __init__.py
```

##### Описание файлов

- `__init__.py`: Пустой файл, который делает директорию пакетом Python.
- `admin.py`: Конфигурация административной панели Django.
- `apps.py`: Конфигурация приложения.
- `models.py`: Определение моделей базы данных.
- `tests.py`: Тесты для приложения.
- `views.py`: Определение представлений (контроллеров).
- `migrations/`: Директория для хранения миграций базы данных.

#### Настройка маршрутизации URL

Для маршрутизации URL необходимо добавить маршруты в файл `urls.py` вашего приложения и проекта.

Пример `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

Пример `myapp/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

#### Шаблонизатор Django

Django использует мощный шаблонизатор для рендеринга HTML-шаблонов.

Пример шаблона `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My App</title>
</head>
<body>
    <h1>Welcome to My App</h1>
    <p>Hello, {{ name }}!</p>
</body>
</html>
```

Пример представления `views.py`, которое рендерит шаблон:

```python
from django.shortcuts import render

def index(request):
    context = {
        'name': 'World'
    }
    return render(request, 'index.html', context)
```

Для использования шаблонов необходимо создать директорию `templates` внутри вашего приложения и поместить туда шаблоны.

#### Модели и миграции

Django ORM позволяет определять модели и автоматически генерировать SQL для создания таблиц в базе данных.

Пример модели в `models.py`:

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
```

После определения модели нужно создать и применить миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Административная панель

Django поставляется с мощной административной панелью, которая позволяет управлять данными через веб-интерфейс.

Для регистрации модели в админке добавьте её в `admin.py`:

```python
from django.contrib import admin
from .models import User

admin.site.register(User)
```

Теперь модель `User` будет доступна в административной панели по адресу `http://127.0.0.1:8000/admin/`.

#### Запуск проекта на практике

1. Создайте проект:

```bash
django-admin startproject myproject
cd myproject
```

2. Создайте приложение:

```bash
python manage.py startapp myapp
```

3. Зарегистрируйте приложение в `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'myapp',
]
```

4. Создайте модель в `myapp/models.py`:

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
```

5. Создайте и примените миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Создайте представление в `myapp/views.py`:

```python
from django.shortcuts import render

def index(request):
    context = {
        'name': 'World'
    }
    return render(request, 'index.html', context)
```

7. Настройте маршрутизацию в `myapp/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

8. Настройте маршрутизацию в `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

9. Создайте шаблон `myapp/templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My App</title>
</head>
<body>
    <h1>Welcome to My App</h1>
    <p>Hello, {{ name }}!</p>
</body>
</html>
```

10. Запустите сервер разработки:

```bash
python manage.py runserver
```

Теперь вы можете перейти по адресу `http://127.0.0.1:8000/` и увидеть ваше приложение.