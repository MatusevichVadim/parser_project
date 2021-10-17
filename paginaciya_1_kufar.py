import requests
from bs4 import BeautifulSoup
import csv
from datetime import date


def get_html(url):
    responce = requests.get(url)
    if responce.ok: #200 ##403(Доступ запрещен) ##404(стр не найдена)
        return responce.text
    print(responce.status_code)

def write_csv(data):
    with open(f'kufar_veliki_{date.today()}.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([data['name'],
                         data['condition'],
                         data['price'],
                         data['place']])

def norm_data(string):
    return string.strip().split(',')[-1]


def get_html_data(html):
    soup = BeautifulSoup(html, 'lxml')
    for velosiped in soup.find_all('article'):
        name = velosiped.find('h3').text
        condition = norm_data(velosiped.find('div', class_='kf-EpoX-88dd1').text)
        price = velosiped.find('span', class_='kf-ECRu-9ea5f').text
        place = velosiped.find('span', class_='kf-EfzH-7a26d').text

        data = {'name': name,
                'condition': condition,
                'price': price,
                'place': place}

        write_csv(data)

def main():
    url = 'https://www.kufar.by/l/velosipedy'
    get_html_data(get_html(url))


if __name__ == '__main__':
    main()
