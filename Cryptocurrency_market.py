import requests
from bs4 import BeautifulSoup
import csv
import time


def get_html(url):
    responce = requests.get(url)
    return responce.text

def write_csv(data):
    with open('crytpo_data.csv', 'a') as file:
        writer = csv.writer(file)
        pass


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table').find('tbody').find_all('tr')
    counter = 0
    for tr in trs:
        tds = tr.find_all('td')
        if counter < 10:
            name = tds[2].find_all('p')[0].text
            symbol = tds[2].find_all('p')[1].text
        else:
            name = tds[2].find('a').find_all('span')[1].text
            symbol = tds[2].find('a').find_all('span')[2].text
        print(name, symbol)
        # print(tds[2].find_all('p')[0].text)
        counter += 1


# sc-1eb5slv-0 iworPT

def main():
    url = 'https://coinmarketcap.com/'
    get_page_data(get_html(url))

if __name__ == '__main__':
    main()
