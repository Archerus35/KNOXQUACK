import requests
from bs4 import BeautifulSoup
import re
import csv 
import json
import datetime
import os

def clean_gameid(game_id):
    game_id = re.sub("[^\d]", '', game_id)
    return int(game_id)

def format_date(date):
    months = {
        'January' : 1,'February' : 2,'March' : 3,
        'April' : 4,'May' : 5,'June' : 6,
        'July' : 7,'August' : 8,'September' : 9,
        'October' : 10, 'November': 11, 'December': 12
    }

    sp_date = date.split()
    sp_date[0] = months[sp_date[0]]
    sp_date[1] = re.sub("[^\d]", '', sp_date[1])
    sp_date = list(map(lambda d: int(d), sp_date))
    new_date = datetime.datetime(sp_date[-1], sp_date[0], sp_date[1])
    date_formatted = '{}-{}-{}'.format(new_date.day, new_date.month, new_date.year)
    return date_formatted    


s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
url_base = 'https://www.metacritic.com/browse/games/release-date/available/pc/metascore'
urls = [f'{url_base}?page={i}' for i in range(1, 11)]
urls.insert(0, url_base)

reviews_urls = []

titles = []
game_count = 1

for url in urls:
    r = s.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')


    tables = soup.find_all('table', class_='clamp-list')

    game_info = soup.find_all('td', class_='clamp-summary-wrap') 

    game_image_wrappers = soup.find_all('td', class_='clamp-image-wrap')

    print(len(game_image_wrappers))
    print(len(game_info))

    score_class = re.compile('metascore_w large game .*')

    url_count = 0
    print(f'Urls Fetched: {url_count}/{len(urls)}')


    for g in range(len(game_info)):
        game_id_container = game_info[g].find('span', class_='title numbered').text
        game_id = clean_gameid(game_id_container)
        title = game_info[g].find('h3').text
        description = game_info[g].find('div', class_='summary').text
        score = game_info[g].find('div', class_=score_class).text
        date_clamp = game_info[g].find('div', class_='clamp-details')
        date = date_clamp.find_all('span')
        date = date[-1].text
        img = game_image_wrappers[g].find('img')
        img_url = img.get('src')
        review_anchor = game_info[g].find('a', class_='title')
        review_url = review_anchor.get('href')
        game_data = {
            "game_id" : game_id,
            "title" : title,
            "description" : description.strip(),
            "score" : int(score),
            "date" : format_date(date),
            "img_url" : img_url
        }
        review_full_url = 'https://www.metacritic.com' + review_url + '/user-reviews'
        reviews_urls.append((game_id, review_full_url))
        titles.append(game_data)
        url_count += 1
        os.system('cls' if os.name == 'nt' else 'clear')

with open('reviews_urls.csv', 'w') as outfile: 
    csv_out = csv.writer(outfile)
    for row in reviews_urls:
        csv_out.writerow(row)

with open('games.json', 'w') as jsonfile:
    json.dump(titles, jsonfile)



print(urls)