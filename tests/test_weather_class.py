from datetime import datetime

import weather


class TestWeatherClass:

    def setup_class(cls):
        cls.weather = weather

    def test_city_geocoding(self):
        city = 'Moscow'

        city_list: list = self.weather.get_geocoding(city)
        for row in city_list:
            if row.country == 'RU' and row.state == 'Moscow':
                assert row.lat == 55.7504461
                assert row.lon == 37.6174943
                break
        else:
            raise ValueError

    def test_current_weather(self):
        # multiple cities
        city = 'Moscow'

        city_list: list = self.weather.get_geocoding(city)
        assert len(city_list) == 5
        for row in city_list:
            if row.country == 'RU' and row.state == 'Moscow':
                state = 'Moscow'
                country = 'RU'
                geocoding_list = self.weather.get_geocoding(
                    city, state, country
                )
                assert geocoding_list
                assert isinstance(geocoding_list, list)
                assert len(geocoding_list) == 1
                assert geocoding_list[0].lat == 55.7504461
                assert geocoding_list[0].lon == 37.6174943
                break
        else:
            raise ValueError

        # Single city
        city = 'Erevan'
        geocoding = weather.get_geocoding(city)
        current_weather: str = self.weather.get_current_weather_api(
            geocoding[0].lon,
            geocoding[0].lat
        )
        assert isinstance(current_weather, str)
        assert current_weather.startswith('<b>Погода')

    def test_weather_forcast(self):

        # multiple cities
        city = 'Moscow'
        day = datetime.today().day + 2
        city_list: list = self.weather.get_geocoding(city)
        assert len(city_list) == 5
        for row in city_list:
            if row.country == 'RU' and row.state == 'Moscow':
                state = 'Moscow'
                country = 'RU'
                geocoding_list = self.weather.get_geocoding(
                    city, state, country
                )
                assert geocoding_list
                assert isinstance(geocoding_list, list)
                assert len(geocoding_list) == 1
                assert geocoding_list[0].lat == 55.7504461
                assert geocoding_list[0].lon == 37.6174943
                break
        else:
            raise ValueError

        # Single city
        city = 'Erevan'
        geocoding = weather.get_geocoding(city)
        forcast = self.weather.get_weather_forcast_day_api(
            lon=geocoding[0].lon,
            lat=geocoding[0].lat
        )
        forcast_weather = forcast[day]

        assert isinstance(forcast_weather, str)
        assert forcast_weather.startswith('<b>Погода в г. Ереван')
