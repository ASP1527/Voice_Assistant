import requests
from bs4 import BeautifulSoup


def get_weather():
    page = requests.get('https://www.bbc.co.uk/weather/2643743')
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    info = soup.find_all(class_='wr-value--temperature--c')
    # print(info)
    high_today = info[0].get_text()
    low_today = info[1].get_text()
    print(high_today)
    print(low_today)


get_weather()
