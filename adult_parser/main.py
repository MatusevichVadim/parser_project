import requests
import csv
from bs4 import BeautifulSoup
from peewee import *

# db = PostgresqlDatabase(database='~', user='~', password='~', host='~')
db = SqliteDatabase('sqlite.db')

class Coin(Model):
    name = CharField()
    short_name = CharField()
    url = TextField()
    price = CharField()

    class Meta:
        database = db


def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


def main():
    db.connect()
    db.create_tables([Coin])

    with open('../crytpo_data 2021-10-14.csv', 'r') as f:
        order = ['name', 'short_name', 'url', 'price']
        reader = list(csv.reader(f, delimiter=';'))

        # for index, row in enumerate(reader):
        #     reader[index] = dict(zip(order, row))
        #     coin = Coin(name=row[0], short_name=row[1], url=row[2], price=row[3])
        #     coin.save()
        with db.atomic():  # транзакции
            # for row in reader:
            #     Coin.create(name=row[0], short_name=row[1], url=row[2], price=row[3])
            for index in range(0, len(reader), 100):
                Coin.insert_many(reader[index:index+100]).execute()

    # url = 'http'
    # html = get_html(url)
    # get_data(html)
    # # print(html_data)


if __name__ == '__main__':
    main()
