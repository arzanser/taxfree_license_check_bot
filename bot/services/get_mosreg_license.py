import base64
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class CarLicense:
    def __init__(self, driver, url) -> None:
        self.driver = driver
        self.url = url
        self.driver.get(self.url)
        self.page_source = self.get_source_page()
    
    def check_status_license(self) -> int:
        soup = bs(self.driver.page_source, "lxml")
        count = 0
        for line in soup.find_all("tr"):
            for td in line.find_all("td"):
                if td.text == "Действующее":
                    return count
            count += 1

        return count

    def get_source_page(self) -> str:
        buttons = self.driver.find_elements(By.CLASS_NAME, "js-popup-open")
        if len(buttons) > 1:
            buttons[self.check_status_license()-1].click()
        else:
            buttons[0].click()
        return self.driver.page_source


    def extract_license_data(self) -> dict:
        result_data = {}
        soup = bs(self.page_source, "lxml")
        for data in soup.find_all("div", {"class": "table-responsive"}):
            for tr in data.find_all("tr"):
                try:
                    key, value = tr.text.split(":")
                    result_data[f"{key}:"] = result_data.get(f"{key}:", value)
                except:
                    continue
        return result_data


class CarierLicense:
    def __init__(self, driver, url, file_path) -> None:
        self.driver = driver
        self.url = url
        self.file_path = file_path
        self.page_source = self.get_source_page()

    def get_source_page(self) -> str:
        self.driver.get(self.url)
        button = self.driver.find_element(By.CLASS_NAME, "js-popup-open")
        button.click()
        return self.driver.page_source

    def get_qr(self) -> None:
        self.driver.get(self.url)
        soup = bs(self.driver.page_source, "lxml")
        for img in soup.find_all("img"):
            if img["alt"] == "QR":
                qr_image = img["src"].split(",")[1]
                with open(self.file_path, "wb") as file:
                    file.write(base64.b64decode(qr_image))

    def extract_license_data(self) -> dict:
        result_data = {}
        soup = bs(self.page_source, "lxml")
        for data in soup.find_all(
            "div", {"class": "table-responsive"}):
            for tr in data.find_all("tr"):
                try:
                    key, value = tr.text.split(":")
                    result_data[f"{key}:"] = result_data.get(f"{key}:", value)
                except:
                    continue
        return result_data