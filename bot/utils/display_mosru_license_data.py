from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bot.config import *
from bot.services.get_mosru_license import CarLicense, CarierLicense
from bot.utils.reduce_to_string import *


def get_car_license(driver, car_number, file_path) -> dict:
    """Получаем данные по лицензии на машину"""
    url = MOSRU_CAR_LICENSE_URL
    try:
        for _ in range(5):
            car_license = CarLicense(driver, url, car_number, file_path)
            license_data = car_license.extract_license_data()
            if license_data != {}:
                return license_data
        return {}
    except:
        return {}


def get_carier_license(driver, car_number, file_path) -> dict:
    """Получаем данные по лицензии на перевозчика"""
    url = MOSRU_CARIER_LICENSE_URL
    try:
        for _ in range(5):
            carier_license = CarierLicense(driver, url, car_number, file_path)
            license_data = carier_license.extract_license_data()
            if license_data != {}:
                return license_data
        return {}
    except:
        return {}


async def print_mosru_license(
        msg, car_number: str, file_path: str) -> None:
    """Выводим данные по лицении"""

    #Подключаем Selenium и настраиваем
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    #Достаем данные по лицензии
    car_license_data = get_car_license(driver, car_number, file_path)
    carier_license_data = get_carier_license(driver, car_number, file_path)
    #Закрываем браузер
    driver.quit()
    #Выводм эти данные
    await msg.answer(
        print_license_data(
            merge_dict_mosru(
                car_license_data, carier_license_data
            )
        )
    )
