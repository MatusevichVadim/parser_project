import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)

def main():
    url = 'http://wordpress.org/'
    html = get_html(url)
    get_data(html)
    # print(html_data)


if __name__ == '__main__':
    main()
