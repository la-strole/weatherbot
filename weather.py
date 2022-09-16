# https://home.openweathermap.org/
# https://openweathermap.org/api/one-call-3
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Union

import requests

from serialization import ValidDay

# Add logger
logger_weather = logging.getLogger('weather')
f_handler = logging.FileHandler('log.txt')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger_weather.addHandler(f_handler)
logger_weather.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))

token = os.environ.get('OPENWEATHER_TOKEN')


def get_geocoding(city: str, state='', country_code='') \
        -> Optional[List[Dict[str, str]]]:
    """
    Get latitude and longitude for city.
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
            logger_weather.exception(f"Can not get geocoding "
                                     f"for city {city}."
                                     f" Exception: {e}.")
            return None

        return result
    else:
        logger_weather.error("Can not find openweather token.")
        return None


def get_current_weather(city: str,
                        state='',
                        country_code='') -> Optional[Union[str, List[dict]]]:
    geocoding_list = get_geocoding(city, state, country_code)

    if geocoding_list and token:
        # If exists only one city with this name.
        if len(geocoding_list) == 1:
            geocoding = geocoding_list[0]
            url = f"https://api.openweathermap.org/data/2.5/weather?" \
                  f"lat={geocoding.get('lat')}&" \
                  f"lon={geocoding.get('lon')}&" \
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
                sunrise = datetime.utcfromtimestamp(item["sunrise"] +
                                                    item['timezone']).strftime("%H:%M")
                sunset = datetime.utcfromtimestamp(item["sunset"] +
                                                   item['timezone']).strftime("%H:%M")
                result = f"Погода в г. {city.capitalize()} ({response['sys']['country']}):\n"
                result = ''.join((result, f'{item["weather"]}, '
                                          f'{int(item["temp"])}\u00B0, '
                                          f'ощущается {int(item["feels_like"])}\u00B0, '
                                          f'{item["humidity"]}%, '
                                          f'ветер {item["speed"]} м/с\n'
                                          f'Восход: {sunrise}, Закат: {sunset}'))
            except Exception as e:
                logger_weather.exception(f"Can not get current weather "
                                         f"for {city}. Extension: {e}.")
                return None
            return result
        # If there are multiple cities with this name
        else:
            city_list = [{'state': row.get('state'), 'country': row.get('country')}
                         for row in geocoding_list]
            return city_list
    else:
        logger_weather.error(f"Can not get geocoding for '{city}'")
        return None


def get_weather_forcast_day(city: str,
                            day: int,
                            state='',
                            country_code='',
                            ) -> Optional[Union[str, List[dict]]]:
    """
    https://openweathermap.org/forecast5
    """
    geocoding_list = get_geocoding(city, state, country_code)

    if geocoding_list and token:

        # If there is only one city with this name

        if len(geocoding_list) == 1:
            geocoding = geocoding_list[0]
            url = f"https://api.openweathermap.org/data/2.5/forecast?" \
                  f"lat={geocoding.get('lat')}&" \
                  f"lon={geocoding.get('lon')}&" \
                  f"lang=ru&" \
                  f"units=metric&" \
                  f"appid={token}"
            try:

                # Validate day.
                valid_day = ValidDay(day=day).day

                response = requests.get(url)
                assert response.status_code == 200
                response = response.json()
                timezone = response['city']['timezone']
                day_weather = [row for row in response['list']
                               if datetime.fromtimestamp(row['dt']).day == valid_day]

                if not day_weather:
                    return "Погода доступна на 5 дней вперед"

                result = f'Погода в г. {city.capitalize()} ({response["city"]["country"]}) на {day} число\n'
                for item in day_weather:
                    dt = datetime.utcfromtimestamp(item["dt"] + timezone)
                    result = '\n'.join((result,
                                        f'{dt.hour}:00 {item["weather"][0]["description"]}, '
                                        f'{int(item["main"]["temp"])}\u00B0 '
                                        f'{item["main"]["humidity"]}%, '
                                        f'ветер {item["wind"]["speed"]} м/с, '
                                        f'порывы {item["wind"]["gust"]} м/с'))
                sunrise = datetime.utcfromtimestamp(response["city"]["sunrise"] +
                                                    timezone).strftime("%H:%M")
                sunset = datetime.utcfromtimestamp(response["city"]["sunset"] +
                                                   timezone).strftime("%H:%M")
                result = '\n'.join((result, f"Восход: {sunrise} Закат: {sunset}"))
                return result

            except Exception as e:
                logger_weather.exception(
                    f"Can not get weather forcast for {city}. Extension: {e}.")
                return None
        # If there are many cities with this name.
        else:
            city_list = [{'state': row.get('state'), 'country': row.get('country')}
                         for row in geocoding_list]
            return city_list
    else:
        logger_weather.error(f"Can not get geocoding for '{city}' "
                             f"or there are not token for openweather")
        return None
