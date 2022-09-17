import os
from datetime import datetime

import weather


class TestWeatherClass:

    def setup_class(cls):
       cls.weather = weather

    def test_city_geocoding(self):
        city = 'Moscow'

        city_list: list = self.weather.get_geocoding(city)
        for row in city_list:
            if row.get('country') == 'RU' and row.get('state') == 'Moscow':
                assert row.get('lat') == 55.7504461
                assert row.get('lon') == 37.6174943
                break
        else:
            raise ValueError

    def test_current_weather(self):
        # multiple cities
        city = 'Moscow'

        city_list: list = self.weather.get_current_weather(city)
        assert len(city_list) == 5
        for row in city_list:
            if row.get('country') == 'RU' and row.get('state') == 'Moscow':
                state = 'Moscow'
                country = 'RU'
                geocoding_list = self.weather.get_geocoding(city, state, country)
                assert geocoding_list
                assert isinstance(geocoding_list, list)
                assert len(geocoding_list) == 1
                assert geocoding_list[0].get('lat') == 55.7504461
                assert geocoding_list[0].get('lon') == 37.6174943
                break
        else:
            raise ValueError

        # Single city
        city = 'Erevan'

        current_weather: str = self.weather.get_current_weather(city)
        assert isinstance(current_weather, str)
        assert current_weather.startswith('Погода')

    def test_weather_forcast(self):

        # multiple cities
        city = 'Moscow'

        city_list: list = self.weather.get_current_weather(city)
        assert len(city_list) == 5
        for row in city_list:
            if row.get('country') == 'RU' and row.get('state') == 'Moscow':
                state = 'Moscow'
                country = 'RU'
                geocoding_list = self.weather.get_geocoding(city, state, country)
                assert geocoding_list
                assert isinstance(geocoding_list, list)
                assert len(geocoding_list) == 1
                assert geocoding_list[0].get('lat') == 55.7504461
                assert geocoding_list[0].get('lon') == 37.6174943
                break
        else:
            raise ValueError

        # Single city
        city = 'Erevan'

        forcast_weather: str = self.weather.get_weather_forcast_day(city,
                                                                    datetime.now().day + 1)
        assert isinstance(forcast_weather, str)
        assert forcast_weather.startswith(f'Погода в г. {city.capitalize()}')

        # Single city wrong date
        city = 'Erevan'

        forcast_weather: str = self.weather.get_weather_forcast_day(city,
                                                                    datetime.now().day - 1)
        assert not forcast_weather
