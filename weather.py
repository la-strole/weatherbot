# https://home.openweathermap.org/
# https://openweathermap.org/api/one-call-3
import logging
import os
from datetime import datetime
from typing import Dict, Optional

import requests


class weather:

    def __init__(self):

        # Add logger
        self.logger_weather = logging.getLogger('weather')
        f_handler = logging.FileHandler('log.txt')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger_weather.addHandler(f_handler)
        self.logger_weather.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))

        self.token = os.environ.get('OPENWEATHER_TOKEN')

    def get_geocoding(self, city: str) -> Optional[Dict[str, str]]:
        """
        Get latitude and longitude for city.
        :param city: City name.
        :return: {'lat': str, 'lon': str}
        """

        if self.token:
            url = f'https://api.openweathermap.org/geo/1.0/direct?' \
                  f'q={city}&limit=2&appid={self.token}'
            try:
                response = requests.get(url).json()
                result = {'lat': response[0].get('lat'),
                          'lon': response[0].get('lon')
                          }
            except Exception as e:
                self.logger_weather.exception(f"Can not get geocoding "
                                              f"for city {city}."
                                              f" Exception: {e}.")
                return None

            return result
        else:
            self.logger_weather.error("Can not find openweather token.")
            return None

    def get_current_weather(self,
                            city: str) -> Optional[str]:

        geocoding = self.get_geocoding(city)

        if geocoding:

            url = f"https://api.openweathermap.org/data/2.5/weather?" \
                  f"lat={geocoding.get('lat')}&" \
                  f"lon={geocoding.get('lon')}&" \
                  f"lang=ru&" \
                  f"units=metric&" \
                  f"appid={self.token}"
            try:
                response = requests.get(url).json()
                item = {'weather': response['weather'][0]['description']}
                item.update(response['main'])
                item.update(response['wind'])
                item.update(response['sys'])
                sunrise = datetime.fromtimestamp(item["sunrise"]).strftime("%H:%M")
                sunset = datetime.fromtimestamp(item["sunset"]).strftime("%H:%M")
                result = f"Погода в г. {city} ({response['sys']['country']}):\n"
                result = ''.join((result, f'{item["weather"]}, '
                                          f'{int(item["temp"])}\u00B0, '
                                          f'ощущается {int(item["feels_like"])}\u00B0, '
                                          f'{item["humidity"]}%, '
                                          f'ветер {item["speed"]} м/с\n'
                                          f'Восход: {sunrise}, Закат: {sunset}'))
            except Exception as e:
                self.logger_weather.exception(f"Can not get current weather "
                                              f"for {city}. Extension: {e}.")
                return None
            return result
        else:
            self.logger_weather.error(f"Can not get geocoding for '{city}'")
            return None

    def get_weather_forcast_day(self,
                                city: str,
                                day: str) -> Optional[str]:
        """
        https://openweathermap.org/forecast5
        """
        geocoding = self.get_geocoding(city)

        if geocoding and self.token:
            url = f"https://api.openweathermap.org/data/2.5/forecast?" \
                  f"lat={geocoding.get('lat')}&" \
                  f"lon={geocoding.get('lon')}&" \
                  f"lang=ru&" \
                  f"units=metric&" \
                  f"appid={self.token}"
            try:

                # Validate day.
                now = datetime.now()
                datetime(year=now.year, month=now.month, day=int(day))

                response = requests.get(url).json()
                day_weather = [row for row in response['list']
                               if datetime.fromtimestamp(row['dt']).day == int(day)]

                if not day_weather:
                    return "Погода доступна на 6 дней вперед"

                result = f'Погода в г. {city} ({response["city"]["country"]}) на {day} число\n'
                for item in day_weather:
                    dt = datetime.fromtimestamp(item["dt"])
                    result = '\n'.join((result,
                                        f'{dt.hour}:00 {item["weather"][0]["description"]}, '
                                        f'{int(item["main"]["temp"])}\u00B0 '
                                        f'{item["main"]["humidity"]}%, '
                                        f'ветер {item["wind"]["speed"]} м/с, '
                                        f'порывы {item["wind"]["gust"]} м/с'))
                sunrise = datetime.fromtimestamp(response["city"]["sunrise"]).strftime("%H:%M")
                sunset = datetime.fromtimestamp(response["city"]["sunset"]).strftime("%H:%M")
                result = '\n'.join((result, f"Восход: {sunrise} Закат: {sunset}"))
                return result

            except Exception as e:
                self.logger_weather.exception(
                    f"Can not get weather forcast for {city}. Extension: {e}.")
                return None
        else:
            self.logger_weather.error(f"Can not get geocoding for '{city}' "
                                      f"or there are not token for openweather")
            return None
