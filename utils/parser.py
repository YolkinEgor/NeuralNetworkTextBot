from bs4 import BeautifulSoup
import requests

response = requests.get('https://ahart.ru/strashilki.php')
page = response.content
soup = BeautifulSoup(page, 'lxml')
urls = soup.findAll('a')[14:-6]

for url in urls:
    response = requests.get('https://ahart.ru/' + url.get('href'))
    page = response.content

    soup = BeautifulSoup(page, 'lxml')
    text = soup.findAll('div', class_='content three_quarter first')[0].text
    print(text[:-170])
