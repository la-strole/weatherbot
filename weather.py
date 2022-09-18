# https://home.openweathermap.org/
# https://openweathermap.org/api/one-call-3
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import requests

import settings
from serialization import ValidCityInstance

# Add logger
logger_weather = logging.getLogger('weather')
f_handler = logging.FileHandler('log.txt')
f_format = logging.Formatter('%(asctime)s - %(name)s - '
                             '%(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger_weather.addHandler(f_handler)
logger_weather.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))

token = settings.OPEN_WEATHER_TOKEN
assert token


def get_geocoding(city: str,
                  state='',
                  country_code=''
                  ) -> Optional[List[ValidCityInstance]]:
    """
    Get latitude and longitude for city.
    https://openweathermap.org/api/geocoding-api
    :param country_code: ISO 3166 country code
    :param state: State
    :param city: City name.
    :return: {'lat': str, 'lon': str}
    """

    if token:
        url = f'https://api.openweathermap.org/geo/1.0/direct?' \
              f'q={city},{state},{country_code}&' \
              f'limit=5&' \
              f'appid={token}'
        try:
            response = requests.get(url)
            assert response.status_code == 200
            result = response.json()
        except Exception as e:
            logger_weather.exception(f"get_geocoding: Can not get geocoding "
                                     f"for city {city}."
                                     f" Exception: {e}.")
            return None
        logger_weather.debug(f"get_geocoding: Return geocoding "
                             f"for city {city}")
        city_list: List[ValidCityInstance] = []

        for row in result:

            if len(city_list) == 0 or \
                    not any([(item.state == row.get('state') and
                              item.country == row.get('country'))
                             for item in city_list]):
                valid_city = ValidCityInstance(
                    city=city,
                    state=row.get('state', 'Не удалось найти'),
                    country=row.get('country',
                                    'Не удалось найти'),
                    lat=row.get('lat'),
                    lon=row.get('lon')
                )

                city_list.append(valid_city)

        return city_list
    else:
        logger_weather.error("get_geocoding: Can not find openweather token.")
        return None


def get_current_weather_api(lon: float,
                            lat: float
                            ) -> str:
    """
    https://openweathermap.org/current
    :param lon: longitude
    :param lat: latitude
    :return: string with current weather for given coordinates,
    None if there are errors.
    """
    if token:

        url = f"https://api.openweathermap.org/data/2.5/weather?" \
              f"lat={lat}&" \
              f"lon={lon}&" \
              f"lang=ru&" \
              f"units=metric&" \
              f"appid={token}"

        try:
            response = requests.get(url).json()
            item = {'weather': response['weather'][0]['description'],
                    'timezone': response['timezone']}
            item.update(response['main'])
            item.update(response['wind'])
            item.update(response['sys'])
            sunrise = datetime.utcfromtimestamp(
                item["sunrise"] +
                item['timezone']).strftime("%H:%M")
            sunset = datetime.utcfromtimestamp(
                item["sunset"] +
                item['timezone']).strftime("%H:%M")
            result = f'<b>Погода в городе {response["name"]} ' \
                     f'({response["sys"]["country"]}):</b>\n' \
                     f'{item["weather"].capitalize()}, ' \
                     f'{int(item["temp"])}\u00B0,\n' \
                     f'Ощущается {int(item["feels_like"])}\u00B0,\n' \
                     f'Влажность {item["humidity"]}%,\n' \
                     f'Ветер {item["speed"]} м/с\n' \
                     f'Восход: {sunrise}, ' \
                     f'Закат: {sunset}'

        except Exception as e:
            logger_weather.exception(f"get_current_weather_api: "
                                     f"Can not get current weather "
                                     f"Extension: {e}.")
            return "Не удалось найти прогноз погоды. " \
                   "Попробуйте позже, пожалуйста."

        logger_weather.debug("get_current_weather_api: "
                             "Return current weather")
        return result

    else:
        logger_weather.error("get_current_weather_api:"
                             "No open weather token exist.")
        return "Не удалось найти прогноз погоды. Попробуйте позже, пожалуйста."


def get_weather_forcast_day_api(lon: float,
                                lat: float
                                ) -> Optional[Dict[int, str]]:
    """
    https://openweathermap.org/forecast5
    :param lon: longitude: float
    :param lat: latitude: float
    :return: Forcast string for the day or None if there are errors.
    """

    if token:

        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"lat={lat}&" \
              f"lon={lon}&" \
              f"lang=ru&" \
              f"units=metric&" \
              f"appid={token}"

        try:

            response = requests.get(url)
            assert response.status_code == 200
            response = response.json()

            result: Dict[int, str] = {}

            timezone = response['city']['timezone']
            city_name: str = response["city"]["name"]
            country_name: str = response["city"]["country"]
            sunrise: str = datetime.utcfromtimestamp(
                response["city"]["sunrise"] +
                timezone).strftime("%H:%M")
            sunset: str = datetime.utcfromtimestamp(
                response["city"]["sunset"] +
                timezone).strftime("%H:%M")
            # city_lon: float = response["city"]["coord"]["lon"]
            # city_lat: float = response["city"]["coord"]["lat"]

            for hour_forcast in response["list"]:
                day: int = datetime.utcfromtimestamp(hour_forcast['dt']).day
                dt: datetime = datetime.utcfromtimestamp(
                    hour_forcast["dt"] + timezone)
                temp = hour_forcast["main"]["temp"]
                feels_like = hour_forcast["main"]["feels_like"]
                atm_pressure = hour_forcast["main"]["grnd_level"]
                humidity = hour_forcast["main"]["humidity"]
                weather_description = hour_forcast["weather"][0]["description"]
                wind_speed = hour_forcast["wind"]["speed"]
                wind_gust = hour_forcast["wind"]["gust"]
                prob_precipitation: float = hour_forcast["pop"]

                hour_string: str = f"<b>{dt.hour}:00</b>:\n" \
                                   f"    {weather_description}, " \
                                   f"{round(temp)}\u00B0\n" \
                                   f"    (ощущается как " \
                                   f"{round(feels_like)}\u00B0)\n" \
                                   f"    влажность {humidity}%\n" \
                                   f"    атмосферное давление " \
                                   f"{atm_pressure}hPa,\n" \
                                   f"    ветер {round(wind_speed)} м/с" \
                                   f" (порывы до {round(wind_gust)}м/с).\n" \
                                   f"    Вероятность осадков " \
                                   f"{round(prob_precipitation * 100)}%\n"

                if day in result:
                    result[day] = ''.join((result[day], hour_string))

                else:
                    result[day] = ''.join((f"<b>Погода в "
                                           f"г. {city_name.capitalize()} "
                                           f"({country_name})\n"
                                           # f"(lon={city_lon},
                                           # lat={city_lat})\n"
                                           f"на {day} число:</b>\n",
                                           f"Восход: {sunrise}, "
                                           f"Закат: {sunset}\n",
                                           hour_string))

            return result

        except Exception as e:
            logger_weather.exception(
                f"get_weather_forcast_day_api:"
                f"Can not get weather forcast. Extension: {e}.")
            return None
    else:
        logger_weather.error("get_weather_forcast_day_api:"
                             "Can not find token.")
        return None
