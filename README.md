
# Telegram weather bot @laweatherbot

Позволяет получить текущую погоду и прогноз на пять дней вперед. 





## Автор

- [@la-strole](https://github.com/la-strole)


## Badges
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Demo

https://youtu.be/dTqsToz7FMY


## Environment Variables

`OPENWEATHER_TOKEN` - токен для openweather (https://openweathermap.org/api)

`BOT_TOKEN` - токен для telegram api (https://core.telegram.org/bots)

`LOG_LEVEL (optional)`

## Features

- Использование Inline Button для быстрого получения прогноза на соседние дни
- Кэширование запроса - уменьшение нагрузки на сервер



## Установка

```bash
  make install
```
    
## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)

## Запуск через docker 

1. Скопировать docker image с docker hub - `docker pull eugeneparkhom/weatherbot`
2. CLI command: `docker run -d --env-file <path_to_env_file> --rm eugeneparkhom/weatherbot make --file /home/Makefile run`
   где:
   -d - detached mode
   --rm - удалять контейнер после остановки
   <path_to_env_file> - путь к файлу с токенами на host.
   Файл вида:
   `OPENWEATHER_TOKEN=xxxxxxxxxxxxxxxxxxxxx` - токен для openweather (https://openweathermap.org/api)
   `BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx` - токен для telegram api (https://core.telegram.org/bots)
   `LOG_LEVEL=WARNING` (DEBUG) (optional)`

## Локальный запуск

Зарегистрироваться на https://openweathermap.org/ и получить бесплатный токен.

Клонировать

```bash
  git clone https://github.com/la-strole/weatherbot.git
```

Перейти в проект

```bash
  cd weatherbot
```

Установить зависимости

```bash
  make install
```

Запуск сервера

```bash
  make run
```


## Screenshots

<img src="https://drive.google.com/uc?export=view&id=1f07wZE_qntmysjWNGGn7J3UedUDwL5s6" width=50% height=50%>
<img src="https://drive.google.com/uc?export=view&id=1RJQd-yfJBQ6ywOblrH6QobGxOkBAsRMR" width=50% height=50%>
<img src="https://drive.google.com/uc?export=view&id=1EH7PHUSzrzBoX304i2GZtpQ57UdWcM3E" width=50% height=50%>

## Running Tests

```bash
  make test
```


## Documentation
Примеры запросов:
- `погода новосибирск`
- `Погода Новосибирск 20`


В основе - API проекта openweather (https://openweathermap.org/api).

1. По названию города с помощью Geocoding API (https://openweathermap.org/api/geocoding-api) 
   получаем список городов с координатами.
2. Определяем единственный ли город соответствует нашему заросу.
    1. Если да - возвращаем либо текуцщую погоду (https://openweathermap.org/current), 
   либо прогноз на число (https://openweathermap.org/forecast5). 
   При этом получаем прогноз на пять дней и кэшируем его в переменной 
   `/handlers/__init__.py: forcast_history`.
    2. Если городов несколько (API возвращает максимум 5) - то спросим пользователя какой он
   имел в виду, предложив список из кнопок Inline Buttons с названиями страны и области.
3. Сообщения с прогнозом содержат две кнопки типа Inline Buttons, нажатие на которые позволяет
   листать прогноз вперед и назад в пределах пяти дней. 
