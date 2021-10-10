import csv
import requests
from bs4 import BeautifulSoup


def get_html(url):
    my_response = requests.get(url)
    return my_response.text

"""нормализация данных, приводим к цифре"""
def refind(string):
    #1,016 total ratings
    return string.split()[0].replace(',', '')

"""запись словаря в эксель таблицу"""
def write_csv(data):
    with open('plagins.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],
                         data['url'],
                         data['reviews']
                         )) #принимает только 1 элемент -> список, кортеж

def get_data(html):
    soup = BeautifulSoup(html, 'lxml') #экземпляр класса bs
    plugins = soup.find_all('section')[1].find_all('article')

    for plugin in plugins: #перебор плагинов и запись в словарь
        name = plugin.find('h3').text
        url = plugin.find('h3').find('a').get('href')
        rating = refind(plugin.find('span', class_='rating-count').find('a').text)

        data = {'name': name,
                'url': url,
                'reviews': rating
                }

        write_csv(data)


def main():
    url = 'https://wordpress.org/plugins/'
    get_data(get_html(url))


if __name__ == '__main__':
    main()
