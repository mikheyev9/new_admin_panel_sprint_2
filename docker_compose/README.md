# README: Запуск Docker Compose для приложения


1. ## Подготовка файлов и окружения

	__Перейдите в папку проекта:__

			cd docker_compose/simple_project

	__Создайте файл .env:__

	_Используйте шаблон .env.demo как основу:_

			cp .env.demo .env

	__Подготовьте дамп базы данных:__

	_Убедитесь, что файл с дампом базы данных существует по пути:_

			ls -l docker_compose/simple_project/database_dump.sql

2. ## Подготовка директорий на сервере(хосте)
	С*оздаются директории для дальнейшего монтирования с хост-машины непосредственно в контейнер.*
	
	Сделай файл исполняемым:

		chmod +x prepare_volumes.sh

	Запусти скрипт:

		./prepare_volumes.sh
		
3. ## Запуск проекта

__Выполните следующую команду для запуска контейнеров:__

        docker compose up --build

__Важно: Выполняйте эту команду из папки, где находится docker-compose.yml, то есть:__

        docker_compose/simple_project

Дождитесь, пока все сервисы будут запущены.

----------------------

# Проектное задание: Docker-compose

Приступим к улучшению сервиса в области DevOps. Настройте запуск всех компонентов системы — Django, Nginx и Postgresql — с использованием docker-compose.

Для упрощения выполнения задания мы подготовили проект, где настроена работа связки Django + uWSGI + Nginx + Docker. Вы его найдете в своем репозитории в папке `docker_compose/simple_project`.

Сама заготовка уже показывает админку. Однако статика не собирается, миграций нет, конфиги Nginx, uWSGI и Docker, возможно, придётся подправить.

Если вы считаете, что всё нужно сделать по-другому, смело меняйте структуру проекта.

**Перед сдачей проекта на ревью, убедитесь, что выполнены все нижеперечисленные шаги:**

- Отредактируйте, при необходимости, файл `docker_compose/simple_project/app/Dockerfile` для Django. В нем, как минимум, можно добавить сбор статики перед запуском контейнера `python manage.py collectstatic --no-input`. Так же можно продумать создание суперпользователи или даже применение миграций.
- Для настройки Nginx можно пользоваться наработками из этой темы, но ревьюеры будут запускать ваше решение. Перед сдачей проекта убедитесь, что всё работает правильно.
- Уберите версию Nginx из заголовков. Версии любого ПО лучше скрывать от посторонних глаз, чтобы вашу админку случайно не взломали. Найдите необходимую настройку в официальной документации и проверьте, что она работает корректно. Убедиться в этом можно с помощью «Инструментов разработчика» в браузере.
- Отдавайте статические файлы Django через Nginx, чтобы не нагружать сервис дополнительными запросами. Перепишите `location` таким образом, чтобы запросы на `/admin` шли без поиска статического контента. То есть, минуя директиву `try_files $uri @backend;`.
- Обратите внимание на следующее: сбор статики происходит в контейнере с Django приложением, а отдавать ее будет Nginx. Это значит, что Nginx должен каким-то образом получить доступ к этим файлам. Мы вам рекомендуем использовать секцию `volumes` для совместного доступа обоих сервисов к этим файлам.
- В `docker-compose.yml` обратите внимание на инструкцию `- ./database_dump.sql:/docker-entrypoint-initdb.d/init.sql` в сервисе `theatre-db`. Таким образом мы заливаем дамп базы данных в postgres. Это необходимо для наглядности, дабы в административной панели не было пусто. Вы можете убрать эту строку, если хотите создать пустую админку. 
- Важно! Сервис `theatre-db` в текущем виде работать не будет. Это база данных PostgreSQL и полное ее описание остается за вами.
- Проверьте себя. После запуска `docker compose up -d` приложение должно быть доступно в браузере по адресу `http://localhost/admin/`, для входа используйте логин `admin` и пароль `123123` (если вы заливаете database_dump.sql в базу данных, в противном случае, вам необходимо создать суперпользователя самостоятельно). Результат должен выглядеть следующим образом:

![image](django_example.png)

Если ваш результат выглядит так же, поздравляем, вы справились 🎉

**Подсказки и советы:**

- Теории должно быть достаточно для понимания принципов конфигурирования. Если у вас появятся какие-то вопросы по параметрам, ищите ответы [в официальной документации](https://nginx.org/ru/){target="_blank"}.
- Для выполнения задачи про `/admin` нужно посмотреть порядок поиска `location`.
- Для работы со статикой нужно подумать, как залить данные в файловую систему контейнера с Nginx.
- Для задания дана базовая структура, которой можно пользоваться.
- При настройке docker-compose важно проверять пути до папок. Большинство проблем связанно именно с этим.

