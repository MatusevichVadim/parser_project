import requests
from bs4 import BeautifulSoup

"""Сделали запрос и вернули всю html страничку"""
def get_html(url):
    my_response = requests.get(url)
    return my_response.text

"""из html странички спарсили с помощью .find список со всеми p в div и 
проитерировали убирая все теги с помощью метода .text вернув строку с текстом"""
def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ful_text = soup.find('div').find_all('p')
    book = ''
    for i in ful_text:
        book += i.text + ' \n'
    return book

"""Взяли ссылку пропустили через 2 функции и вывели строку с текстом"""
def main():
    url = 'https://www.litmir.me/br/?b=20560&p=1'
    print(get_data(get_html(url)))


if __name__ == '__main__':
    main()
