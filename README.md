# Github repository browsing tool

Пример выполнения тестового задания [https://github.com/wemake-services/meta/issues/7](https://github.com/wemake-services/meta/issues/7).  

Приложение представляет собой сервис для отображения пользовательских репозиториев Github.  

Приложение рабоатет по следующему сценарию:
1. Вы входите в свой аккаунт Github;
2. Вы входите в наш сервис с учетной записью Github;
3. Сервис показывает список всех ваших репозиториев, ваш аватар и имя пользователя.

## Демо
[http://github-repos-browser.herokuapp.com/](http://github-repos-browser.herokuapp.com/)

## Установка
Для использования модуля потртребуется предустановленный Python 3.5 (на других версиях не проверялся).  
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).  
В программе используются следующие сторонние библиотеки:
- СherryPy [https://cherrypy.org/](https://cherrypy.org/);
- Jinja2 [http://jinja.pocoo.org/docs/2.10/](http://jinja.pocoo.org/docs/2.10/);
- requests-oauthlib [https://github.com/requests/requests-oauthlib](https://github.com/requests/requests-oauthlib).  

1. Создайте и активируйте виртуально окружение, например:  
```
$ python3 -m venv my_virtual_environment
$ source my_virtual_environment/bin/activate
```
2. Установите сторонние библиотеки  из файла зависимостей:
```
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```

## Настройка и запуск приложения

Зарегистрируйте свое OAuth приложение в [Github](https://github.com/settings/applications/new). После получения Client ID и Client Secret установите их в качестве переменных окружения:  
```
$ export OAUTH_CLIENT_ID=<your client id>
$ export OAUTH_CLIENT_SECRET=<your client secret>
```

Запуск приложения:
```
$ python app.py
```

Приложение будет доступно по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Цели проекта

Код написан в образовательных целях.