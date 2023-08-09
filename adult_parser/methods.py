from selenium import webdriver  # seleniumwire from difficult proxy connect
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from loguru import logger

import time

ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={ua.chrome}")
options.add_argument("--proxy-server=138.128.91.65:8000")

URL = 'https://n5m.ru/usagent.html'
# URL = 'https://habr.com/ru/search/'
driver = webdriver.Chrome(options=options)

try:
    driver.get(url=URL)
    search = driver.find_element(By.NAME, 'q')
    search.clear()
    search.send_keys()
    time.sleep(10)
except Exception as er:
    logger.debug(f'{er}')
finally:
    driver.close()
    driver.quit()
