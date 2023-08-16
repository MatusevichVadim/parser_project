import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")

data = {}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'market.yandex.ru',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': f'{ua.chrome}',
}

for key, value in headers.items():
    options.add_argument(f'{key}: {value}')


def normalise_data(lvl_2_3: list[str], urls: list[str]) -> dict[str, dict]:
    norm_data = {}

    for item in lvl_2_3:
        item = item.split('\n')
        norm_data[item[0]] = {}
        for i, j in zip(item[1:-1], urls):
            norm_data[item[0]][i] = {'https://market.yandex.ru' + j: {}}

    return norm_data


def get_html(url, params=None):
    user_agent = UserAgent()
    headers = {
        'User-agent': user_agent.chrome,
        'Bfcache-Opt-In': 'unload'
    }
    responce = requests.get(url, headers=headers, params=params)

    if responce.status_code == 200:
        return responce.text
    else:
        print(responce.status_code)
        return None


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


def write_csv(data):
    pass


def main():
    url = "https://market.yandex.ru/"
    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)

    try:
        driver.get(url=url)
        # driver.fullscreen_window()
        time.sleep(15)
        driver.find_element(By.XPATH, "//div[@data-apiary-widget-name='@light/NavigationMenu']").click()
        time.sleep(5)

        # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
        #     By.CLASS_NAME, '_3krX4')))
        for area_lvl_1 in driver.find_elements(By.CLASS_NAME, '_3krX4')[:2]:
            menu_1_name = area_lvl_1.text
            menu_1_value = driver.find_element(By.LINK_TEXT, menu_1_name)
            actions.move_to_element(menu_1_value).perform()
            logger.debug(f"{menu_1_name = }")
            time.sleep(1)

            btns_more = area_lvl_1.find_elements(By.XPATH, "//span[@class='_20WYq _1wg9X _2l6b4 _1gCbc']")

            for btn in btns_more:
                if btn.text == 'Ещё':
                    btn.click()
                    time.sleep(0.5)

            lvl_2_3 = area_lvl_1.find_elements(By.XPATH, "//div[@class='_1dWFG']")
            all_url = area_lvl_1.find_elements(By.XPATH, "//a[@class='egKyN _1mqvV _1wg9X']")

            wripper = normalise_data(
                [i.text for i in lvl_2_3],
                [i.get_dom_attribute('href') for i in all_url]
            )

            logger.debug(f'{wripper = }')
            data[menu_1_name] = {**wripper}
            time.sleep(2)

        for i in data.values():
            for j in i.values():
                for k in j.values():
                    counter = 0
                    driver.get(url=k)
                    while True:
                        try:
                            driver.find_element(By.XPATH, "//div[@class='_3e9Bd']").click()
                        except:
                            logger.debug(f'Товары закончились')
                        finally:
                            last_page = driver.find_element(By.XPATH, "//div[@class='Xe4rX _18sEx _3-NJO']").text
                            driver.find_element(By.XPATH, "//input[@aria-label='в виде сетки']").click()
                            goods_in_last_page = len(driver.find_elements(By.XPATH,
                                                                          "//div[@class='_2im8- _2S9MU _2jRxX']"))
                            all_goods = int(last_page) * 32 + int(goods_in_last_page)



    except Exception as er:
        logger.error(er)
    finally:
        driver.close()
        driver.quit()
        logger.complete()


if __name__ == '__main__':
    main()
