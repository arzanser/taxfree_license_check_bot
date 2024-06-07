import os

from aiogram.types import FSInputFile
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bot.config import *
from bot.text import MESSAGES
from bot.services.get_mosreg_license import (CarierLicense, CarLicense)
from bot.utils.reduce_to_string import *


def get_car_license(driver, car_number: str) -> dict:
    """Получаем данные по лицензии на машину"""
    url = MOSREG_CAR_LICENSE_URL.format(car_number.strip())
    try:
        car_license = CarLicense(driver, url)
        return car_license.extract_license_data()
    except:
        return MESSAGES["ERROR_CAR_LICENSE"]


def get_carier_license(driver, inn_number: str, file_path: str) -> dict:
    """Получаем данные по лицензии на перевозчика"""
    url = MOSREG_CARIER_LICENSE_URL.format(inn_number.strip())
    try:
        carier_license = CarierLicense(driver, url, file_path)
        carier_license.get_qr()
        return carier_license.extract_license_data()
    except:
        return MESSAGES["CARIER_CARIER_LICENSE"]

async def print_qr(msg, file_path) -> None:
    """Выводим QR лицензии"""
    qr_image = FSInputFile(file_path)
    await msg.answer_photo(qr_image)
    os.remove(file_path)


async def print_mosreg_license(
        msg, car_number: str, file_path: str) -> None:
    """Выводим данные по лицензии"""

    #Подключаем Selenium и настраиваем
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    #Получаем данные по лицении
    car_license_data = get_car_license(driver, car_number)
    try:
        inn_number = car_license_data["ИНН:"]
        carier_license_data = get_carier_license(
            driver, inn_number, file_path
        )
        #Печатаем QR
        await print_qr(msg, file_path)
    except:
        carier_license_data = MESSAGES["ERROR_CARIER_LICENSE"]

    #Выводим данные по лицензии
    await msg.answer(
        print_license_data(
            merge_dict_mosreg(
                car_license_data, carier_license_data
            )
        )
    )
    driver.quit()
