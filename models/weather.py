from models.base import BaseModel
from helpers import constants


class Weather(BaseModel):
    def __init__(self, data):
        location = data["location"]
        current = data["current"]
        condition = current["condition"]
        icon = str(condition["icon"])\
            .replace("//", "") \
            .replace("64x64", "128x128")

        self.country = location["country"]
        self.city_name = location["name"]
        self.region = location["region"]
        self.date_time = location["localtime"]
        self.last_update = current["last_updated"]
        self.is_day = int(current["is_day"]) == 1
        self.temperature = round(current["temp_c"])
        self.text = condition["text"]
        self.icon_url = f"http://{icon}"
        self.cloud = current["cloud"]

    def info(self):
        return f"""
{self.country}, {self.city_name}, {self.region}
Дата: {self.date_time}
Останнє оновлення: {self.last_update}

Температура: {self.temperature}°
{self.text} {constants.day_emoji if self.is_day else constants.night_emoji}
Хмарність: {self.cloud}% {constants.cloud_emoji}
        """
