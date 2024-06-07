import time 
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bot.utils.captcha_solver import *

class CarLicense:
    def __init__(self, driver, url, car_number, file_path) -> None:
        self.driver = driver
        self.url = url
        self.car_number = car_number
        self.file_path = file_path
        self.driver.get(self.url)
        self.page_source = self.get_source_page()

    def get_source_page(self) -> str:
        #Вставляем номер машины
        form_control = self.driver.find_element(By.ID, "taxi_form_grz")
        form_control.send_keys(self.car_number)
    
        #Вставляем текст капчи
        form_captcha = self.driver.find_element(By.ID, "taxi_form_captcha")
        solved_captcha = get_solved_captcha(self.driver, self.file_path)
        form_captcha.send_keys(f"{solved_captcha}" + Keys.RETURN)

        time.sleep(2)
        return self.driver.page_source
    
    def extract_license_data(self) -> dict:
        license_data = {}
        soup = bs(self.page_source, "lxml")
        license_check = False
        #Провеяем есть ли лицензия
        for check in soup.find_all("div", {"class": "ajax-change-container"}):
            for line in check.find_all("p"):
                if line.text.strip() != "Такси не найдено":
                    license_check = True

        if license_check  == True:        
            table = soup.find_all("table", {"class": "table w100p"}) 
            for data in table:
                if data.text == table[0].text:
                    for tr in data.find_all("tr"):
                        line = tr.find_all("td")
                        key = line[0].text
                        value = line[1].text
                        license_data[f"{key}"] = license_data.get(f"{key}", value)
        return license_data
    

class CarierLicense:
    def __init__(self, driver, url, car_number, file_path):
        self.driver = driver
        self.url = url
        self.car_number = car_number
        self.file_path = file_path
        self.driver.get(self.url)
        self.page_source = self.get_source_page()

    def get_source_page(self) -> str:
        #Вставляем номер машины
        form_control = self.driver.find_element(By.ID, "carrier_form_grz")
        form_control.send_keys(self.car_number)

        #Вставляем текст капчи
        form_captcha = self.driver.find_element(By.ID, "carrier_form_captcha")
        solved_captcha = get_solved_captcha(self.driver, self.file_path)
        form_captcha.send_keys(f"{solved_captcha}" + Keys.RETURN)

        time.sleep(2)
        return self.driver.page_source

    def extract_license_data(self) -> dict:
        #Извлекаем данные по лицензии
        soup = bs(self.page_source, "lxml")
        license_data = {}
        license_check = False
        #Провеяем есть ли лицензия
        for check in soup.find_all("div", {"class": "ajax-change-container"}):
            for line in check.find_all("p"):
                if line.text.strip() != "Такси не найдено":
                    license_check = True

        if license_check != False:
            table = soup.find_all("table", {"class": "table w100p"})
            for data in table:
                if data.text == table[-1].text:
                    for tr in data.find_all("tr"):
                        line = tr.find_all("td")
                        key = line[0].text
                        value = line[1].text
                        license_data[key] = license_data.get(key, value)

        return license_data
            
