import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CAPTCHA_TOKEN = os.getenv("CAPTCHA_TOKEN")

MOSREG_CAR_LICENSE_URL = "https://mtdi.mosreg.ru/taxi-cars?licenseNumber=&inn=&name=&gosNumber={}&region=ALL"
MOSREG_CARIER_LICENSE_URL = "https://mtdi.mosreg.ru/taxi-permits?licenseNumber=&inn={}&name=&region=ALL"
MOSRU_CAR_LICENSE_URL = "https://transport.mos.ru/auto/reestr_taxi"
MOSRU_CARIER_LICENSE_URL = "https://transport.mos.ru/auto/reestr_carrier"
FGIS_URL = "https://sicmt.ru/fgis-taksi?type=car&filters%5BregNumTS%5D={}&filters%5BlicenseNumber%5D="
QR_FILE_PATH = "/Users/arzanser/Code/taxfree/taxfree_license_check_bot/bot/images/{}-qr.png"
CAPTCHA_FILE_PATH = "/Users/arzanser/Code/taxfree/taxfree_license_check_bot/bot/images/{}-captcha.png"

