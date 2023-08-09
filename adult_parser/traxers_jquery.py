import requests
import csv
from bs4 import BeautifulSoup


def get_html(url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}
    r = requests.get(url, headers=header)
    return r.text



def write_csv(data):
    with open('testimonials.csv', 'a') as f:
        order = []
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def main():
    url = 'https://catertrax.com/traxers/page/1/'

    i = 0
    # while True:
    #     try:
    #
    #         i += 1
    #     except:
    #         break


if __name__ == '__main__':
    main()
