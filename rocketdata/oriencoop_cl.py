import requests
import re
import json
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    responce = requests.get(url)
    if responce.ok:
        return responce.text
    return f'{responce.status_code}'  # 200 ##403(Доступ запрещен) ##404(стр не найдена)


def normal_data(data: str) -> str:
    return data.replace('a', '-').replace('.', ':')


def get_html_data(html: str) -> list[dict]:
    return_data = []
    soup = BeautifulSoup(html, 'lxml')
    for all_shops in soup.find_all(class_='sub-menu'):
        for shop in all_shops.find_all('a'):
            shop_url = re.search(r'(/sucursales/*\d*)', str(shop))[0]
            shop_html = get_html(f'https://oriencoop.cl{shop_url}')
            shop_soup_obj = BeautifulSoup(shop_html, 'lxml')
            for shop_info in shop_soup_obj.find_all(class_='s-dato'):
                address = shop_info.find_all('p')[0].find('span').text
                latlon = shop_soup_obj.find_all('iframe')
                latlon_pattern = re.search(r'!2d(-*\d{2}.\d+)!3d(-*\d{2}.\d+)', str(latlon))
                latitude = float(latlon_pattern[1])
                longitude = float(latlon_pattern[2])
                phones = shop_info.find_all('p')[1].find('span').text.replace('-', '')
                working_pattern = r'\d{1,2}.\d{2} a \d{2}.\d{2}'
                working_hours = shop_info.find_all('p')[3].find_all('span')
                working_hours_morning = normal_data(re.search(working_pattern,
                                                              str(working_hours[0]))[0])
                working_hours_afternoon = normal_data(re.search(working_pattern,
                                                                str(working_hours[1]))[0]).replace(' ', '')

                shop_dict = {"address": address,
                             "latlon": [latitude, longitude],
                             "name": "Oriencoop",
                             "phones": [phones, "600 200 0015", "+56712207838"],
                             "working_hours": [f"mon-thu {working_hours_morning} {working_hours_afternoon}",
                                               f"fri {working_hours_morning} {working_hours_afternoon}"]
                             }

                return_data.append(shop_dict)
                print('*', end='')
    print(' Completed')
    return return_data


def get_json(comleted_date: list[dict]) -> None:
    with open("oriencoop_cl.json", "w") as outfile:
        json.dump(comleted_date, outfile, indent=4)
    return None


def main():
    url = 'https://oriencoop.cl/sucursales.htm'
    get_json(get_html_data(get_html(url)))


if __name__ == '__main__':
    main()
