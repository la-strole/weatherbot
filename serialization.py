from datetime import datetime, timedelta

from pydantic import BaseModel, validator


class ValidDay(BaseModel):
    day: int

    @validator('day')
    def validate_day(cls, key):
        now = datetime.now()
        if key >= now.day:
            if key - now.day <= 5:
                return key
            else:
                raise ValueError(f"day error ({key}). "
                                 f"Can make forcast for 5 days from now.")
        else:
            delta = now + timedelta(days=5)
            if key <= delta.day and delta.month > now.month:
                return key
            else:
                raise ValueError(f"day error ({key}). "
                                 f"Can make forcast for 5 days from now.")


class ValidCityInstance(BaseModel):
    city: str
    state: str
    country: str
    lon: float
    lat: float
