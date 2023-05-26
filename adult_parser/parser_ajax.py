import requests
import csv
from multiprocessing import Pool
from time import sleep


def get_ajax_text(url):
    sleep(1)
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('website.csv', 'a') as f:
        order = ['name', 'url', 'traffic']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_page_data(text):
    data = text.strip().split('\n')[1:]
    for row in data:
        columns = row.strip().split('\t')
        name = columns[2]
        url = columns[1]
        traffic = columns[3]
        data = {'name': name,
                'url': url,
                'traffic': traffic}
        write_csv(data)


def make_all(url):
    text = get_ajax_text(url)
    get_page_data(text)


def main():
    # 4549
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'
    urls = [url.format(str(i)) for i in range(0, 4549)]
    with Pool(20) as pool:
        pool.map(make_all, urls)

    # response = get_ajax_text(url)
     # for i in range(0, 10):
    #     write_csv(get_ajax_text(url+1))


if __name__ == '__main__':
    main()
