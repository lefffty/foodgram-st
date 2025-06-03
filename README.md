Находясь в папке infra, выполните команду docker-compose up. При выполнении этой команды контейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.

По адресу http://localhost изучите фронтенд веб-приложения, а по адресу http://localhost/api/docs/ — спецификацию API.

Проект выполнил студент Шерепа Павел:
  - Профиль на GitHub: https://github.com/lefffty
  - Телеграм: https://t.me/leffffty

# Запуск проекта

Скопируйте проект к себе на компьютер, открыв терминал Git Bash в нужной для вас папке:

```
https://github.com/lefffty/foodgram-st.git
```

Создайте в директории проекта foodgram файл с расширением .env и заполните его следующими данными:

```
POSTGRES_DB = 'food'
POSTGRES_USER = 'food'
POSTGRES_PASSWORD = 'foodgram'
DB_HOST = 'localhost'
DB_PORT = '5432'
DJANGO_SECRET_KEY = 'django-insecure-0rwfqpsco*gn8fr303i%8^ei@#q^nca7#5o!-b=omtakoq8ku_'
```

Перейдите в терминале Git Bash в папку infra и выполните следующую команду, которая соберет Docker-контейнер данного проекта:

```
cd foodgram/infra
docker compose up
```

В процессе сборки Docker-контейнера будут выполнены миграции для Django с помощью следующей команды: 
```
CMD ["sh", "-c", "cp -r all_static/. /collected_static/static/ && python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:8000 backend.wsgi"]
```
То есть вручную миграции применять не нужно.

После успешного создания Docker-контейнера создайте еще один терминал Git Bash, перейдите в нем в папку infra и выполните следующую команду, которая загрузит фикстуры в проект:

```
docker-compose exec backend python manage.py loaddata fixtures/data.json
```

Перейдите на сайт по следующему адресу:

```
https://localhost:8000/recipes
```

Проверьте, что работает документация, админка и Api по следующим путям.

Админка:

```
https://localhost:8000/admin/
```

Для доступа в админку воспользуйтесь данными пользователя **sepriko**:

- **Почта**: serpiko@example.com
- **Пароль**: user_3456

API:

```
https://localhost:8000/api/users/
```

Документация:

```
http://localhost:8000/api/docs/
```

# Дополнительная информация

Учетные данные для входа других пользователей:

- пользователь **lefty**:
  - почта: lefty@example.com
  - пароль: user_1234
- пользователь **tony_montana**:
  - почта: tony@example.com
  - пароль: user_5678
