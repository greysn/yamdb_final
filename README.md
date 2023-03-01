Проект даёт возможность управлять данными методом API запросов.

Проект YaMDb собирает отзывы пользователей на произведения.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 


Добавлять произведения, категории и жанры может только администратор.

Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти.

Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
Шаблон наполнения env-файла

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

Запуск приложения в контейнерах

    Сборка образа выполняется из директории infra_sp2/infra

docker-compose up -d --build 

    Выполнение миграций

docker-compose exec web python manage.py migrate

    Сбор статики

docker-compose exec web python manage.py collectstatic --no-input

    Создание суперюзера

docker-compose exec web python manage.py createsuperuser

Документация

http://127.0.0.1/redoc/

Автор
Мельников Сергей