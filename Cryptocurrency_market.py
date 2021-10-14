import requests
from bs4 import BeautifulSoup
import csv
from datetime import date


def get_html(url):
    responce = requests.get(url)
    return responce.text

def replace_string(str):
    return str[1:].replace(',', '') #нормализация формата строки

def write_csv(data): #newline для того чтобы небыло пустой строки
    with open(f'crytpo_data {date.today()}.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')  #разделитель для разбиения элементов по ячейкам(по умолчанию ,)
        writer.writerow([data['Name'],
                         data['Symbol'],
                         data['Url'],
                         data['Price']])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table').find('tbody').find_all('tr')
    counter = 0
    for tr in trs:
        tds = tr.find_all('td')
        if counter < 10: #первые 10 эл. имеют другую структуру
            name = tds[2].find_all('p')[0].text
            symbol = tds[2].find_all('p')[1].text
        else:
            name = tds[2].find('a').find_all('span')[1].text
            symbol = tds[2].find('a').find_all('span')[2].text
        url = 'https://coinmarketcap.com' + tds[2].find_all('a')[0].get('href')
        price = replace_string(tds[3].text)
        counter += 1
        data = {
            'Name': name,
            'Symbol': symbol,
            'Url': url,
            'Price': price} #создание словара для csv файла

        write_csv(data)

def main():
    url = 'https://coinmarketcap.com/'
    get_page_data(get_html(url))

if __name__ == '__main__':
    main()
