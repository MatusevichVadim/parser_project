import requests
import csv


def get_ajax_text(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('website.csv', 'a') as f:
        order = ['name', 'url', 'traffic']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def main():
    for i in range(0, 20):
        url = f'https://www.liveinternet.ru/rating/ru//today.tsv?page={i}'
        response = get_ajax_text(url)
        data = response.strip().split('\n')[1:]
        for row in data:
            columns = row.strip().split('\t')
            name = columns[2]
            url = columns[1]
            traffic = columns[3]
            data = {
                'name': name,
                'url': url,
                'traffic': traffic
            }
            write_csv(data)

    # for i in range(0, 10):
    #     write_csv(get_ajax_text(url+1))


if __name__ == '__main__':
    main()
