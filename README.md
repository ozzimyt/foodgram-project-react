![workflow](https://github.com/ozzimyt/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
 
## Foodgram - продуктовый помощник

### Стек технологий

![python version](https://img.shields.io/badge/Python-3.7-green)
![django version](https://img.shields.io/badge/Django-3.2-green)
![djangorestframework version](https://img.shields.io/badge/DRF-3.12-green)
![djoser version](https://img.shields.io/badge/Djoser-2.1.0-green)
![docker version](https://img.shields.io/badge/Docker-3-green)

### О проекте:

"Foodgram - Продуктовый помощник": сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Проект доступен по [адресу](http://51.250.84.194)

<details>
<summary><h2>Локальный деплой</h2></summary>

### *Клонируйте репозиторий:*
```
https://github.com/ozzimyt/foodgram-project-react
```

### *Установите и активируйте виртуальное окружение:*
Win:
```
python -m venv venv
. venv/Scripts/activate
```

Mac/linux:
```
python3 -m venv venv
source venv/bin/activate
```

### *Установите зависимости из файла requirements.txt:*
```
pip install -r requirements.txt
```

### *Перейдите в директорию с файлом manage.py, создайте и примените миграции:*
Win
```
cd backend/
python manage.py makemigrations
python manage.py migrate
```

Mac/Linux
```
cd backend/
python3 manage.py makemigrations
python3 manage.py migrate
```

### *Создайте суперпользователя :*
Win
```
python manage.py createsuperuser
```

Mac/linux
```
python3 manage.py createsuperuser
```

### *Запустите сервер:*
Win
```
python manage.py runserver
```

Mac/linux
```
python3 manage.py runserver
```

### *Запуск в Docker*

В папке **infra** создайте файл **.env** и заполните его в соответствии с нижеуказанным:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your
DEBUG=False         # Или True для возможности отображение DEBUG-информации
ALLOWED_HOSTS='*'
DEBUG_SQLITE=True   # Или False для выбора PostgreSQL
```
далее в папке **infra** выполнить команды:
```
docker compose up -d --build
```

После создания и запуска контйнеров зайти в контейнер с бэкэндом и выполнить команды:  
```
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --no-input
docker compose exec backend python manage.py json_to_db.py
docker compose exec backend python manage.py createsuperuser
```

</details>


<details>
<summary><h2>Деплой на удаленном сервере</h2></summary>

раздел в разработке

```curl -SL https://github.com/docker/compose/releases/download/v2.14.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose```

</details>

## Документация к API   

Для открытия документации локально, запустите сервер и перейдите по ссылке:
[http://localhost/api/docs/](http://localhost/api/docs/) 

Для открытия документации на удаленном сервере: [REDOC](http://51.250.84.194/api/docs/)

## Контакты

- [GitHub](https://github.com/ozzimyt)
- [Telegram](https://t.me/Aleksandr_Zimin)
