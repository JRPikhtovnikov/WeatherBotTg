import requests
from bs4 import BeautifulSoup

url = 'https://m.dzen.ru/news?issue_tld=ru'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

news_items = soup.find_all('a', {'class': 'card-feed__link'})

for news_item in news_items:
    title = news_item.find('h3', {'class': 'card-feed__title'}).text.strip()
    description = news_item.find('div', {'class': 'card-feed__description'}).text.strip()
    date = news_item.find('time', {'class': 'card-feed__time'}).text.strip()
    link = news_item.get('href')

    print(f'Title: {title}')
    print(f'Description: {description}')
    print(f'Date: {date}')
    print(f'Link: {link}')
    print('---------------------')
