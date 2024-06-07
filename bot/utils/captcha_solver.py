import base64
from bs4 import BeautifulSoup as bs
from twocaptcha import TwoCaptcha 

from bot.config import *


def get_captcha_image(driver, file_path):
    page_source = driver.page_source
    soup = bs(page_source, "lxml")
    for data in soup.find_all(
        "div", 
        {"class": "container container_center cont_a"}):

        captcha = data.find_all("img")
        for att in captcha:
            if "captcha_image" in att["class"]:
                captcha_image = att["src"].split(",")[1]
                with open(file_path, "wb") as file:
                    file.write(base64.b64decode(captcha_image))    

                    
def captcha_solver(file_path) -> str:
    solver = TwoCaptcha(CAPTCHA_TOKEN)
    captcha_text = solver.normal(file_path)
    return captcha_text["code"]           


def get_solved_captcha(driver, file_path):
    get_captcha_image(driver, file_path)
    try:
        return captcha_solver(file_path)
    except:
        return "Failed"