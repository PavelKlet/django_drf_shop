
## Что из себя представляет проект
Интернет-магазин, front представляет собой подключаемое django-приложение. Берет на себя всё, что связано с отображением страниц, а обращение 
за данными происходит по API, который я реализовал в ходе выполнения проекта.

## Контракт для API
Названия роутов и ожидаемую структуру ответа от API endpoints можно найти в `front/swagger/swagger.yaml`.

## Подключение пакета
1. Cобрать пакет: в директории front выполнить команду python setup.py sdist
2. Установить полученный пакет в виртуальное окружение: `pip install frontend-X.Y.tar.gz`. X и Y - числа, они могут изменяться в зависимости от текущей версии пакета.

# Запуск проектаЖЖЦЦЦЦ
1. Установить все зависимости из [requirements.txt](megano/requirements.txt)
2. Создать файл .env где прописать данные из env.template.

* При запуске проекта через runserver нужно установить библиотеку python-dotenv, импортировать и вызвать в settings load_dotenv, в .env указать 1 для DEBUG,
POSTGRES_HOST в этом случае будет равен localhost, либо прописать данные напрямую в settings


* Для запуска через docker необходимо сбилдить и запустить контейнеры командой docker-compose up, nginx прослушивает 80 порт, поэтому запуск проекта производится на нём по доступному адресу, например 127.0.0.1,
POSTGRES_HOST в этом случае будет равен db

Если запустить сервер разработки: `python manage.py runserver`, то по адресу `127.0.0.1:8000` должна открыться стартовая страница интернет-магазина:
![image](megano/front/root-page.png)

Тестовые данные можно загрузить из директории fixtures командой: python manage.py loaddata fixtures/db.json

Логин и пароль админа: admin 123

# Детали подключаемого приложения `frontend`
Приложение служит только для отрисовки шаблонов из `templates/frontend`, поэтому в `urls.py` напрямую 
используются `TemplateView` из стандартной поставки Django.


