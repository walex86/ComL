import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# https://v1.ru/

client = MongoClient()
db = client.news_parser
news_coll = db.news

def getHtml(url):
    r = requests.get(url)
    return r.text

def getNews(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.findAll('a', class_='matter')
    newTexts = ""
    for i in range(len(news)):
        Name = news[i].find('div', class_='title').text
        Link = 'https://novostivolgograda.ru' + news[i].get('href')
        # newTexts = news[i].find('div', class_='lead').text
        Date = news[i].find('div', class_='meta').text.replace("Общество", "")
        verify = news_coll.find_one({'Name news': Name})

        if not(str(verify) == 'None'):
            for new in news_coll.find():
                if new['Name news'] == Name:
                    continue
        else:
            soup2 = BeautifulSoup(getHtml(Link), 'lxml')
            blocks = soup2.findAll('div', class_='paragraph')
            for k in range(len(blocks)):
                texts = blocks[k].findAll('p')
                for r in range(len(texts)):
                    newTexts += texts[r].text + '\n'
            Text = newTexts
            newTexts = ""
            Date = Date.replace("Происшествия", "")
            Date = Date.replace("Город", "")

            news_doc = {
                "Name news": Name,
                "Date news": Date,
                "Link news": Link,
                "Text news": Text,

            }
            news_coll.insert_one(news_doc)

url = "https://novostivolgograda.ru/news"

getNews(getHtml(url))





