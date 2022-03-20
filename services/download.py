import requests
import config


def fetch_image(url):
    image_data = requests.get(url).content

    with open(config.weather_image_path, "wb") as file:
        file.write(image_data)

    return open(config.weather_image_path, "rb")
