<h1 align="center">LibraryAPI</h1>

Апи для библиотеки

## Использование

Установка зависимостей

```shell
pip install -r requirements.txt
```

Создание бд

```shell
docker run --name library_postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres   
```

Накат миграций и загрузка данных

```shell
python manage.py migrate
python manage.py loaddata data.json
```

<!--- Для выгрузки данных: python -Xutf8 manage.py dumpdata -o data.json --->

Запуск

```shell
python manage.py runserver
```
> **Note**
> Для остановки нажмите <kbd>Ctrl</kbd> + <kbd>C</kbd>