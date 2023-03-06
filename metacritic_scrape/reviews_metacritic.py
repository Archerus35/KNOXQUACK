import csv
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime


data_output = []

with open('reviews_urls.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        data_output.append((tuple(row)))


s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'


users_registered = []
ids_available = [i for i in range(10000000)]
users_in_comments = []


def register_user(username):
    user_id = ids_available.pop()
    users_registered.append((user_id, username))

def get_user_id(username):
    for user_id, u in users_registered:
        if username in u: 
            return user_id

def user_is_registered(username):
    for uid, u in users_registered:
        return True if username in u else False
    
def format_date(date):
    months = {
        'Jan' : 1,'Feb' : 2,'Mar' : 3,
        'Apr' : 4,'May' : 5,'Jun' : 6,
        'Jul' : 7,'Aug' : 8,'Sep' : 9,
        'Oct' : 10, 'Nov': 11, 'Dec': 12
    }

    sp_date = date.split()
    sp_date[0] = months[sp_date[0]]
    sp_date[1] = re.sub("[^\d]", '', sp_date[1])
    sp_date = list(map(lambda d: int(d), sp_date))
    new_date = datetime.datetime(sp_date[-1], sp_date[0], sp_date[1])
    date_formatted = '{}-{}-{}'.format(new_date.day, new_date.month, new_date.year)
    return date_formatted    



review_data = []
count = 0
for game_id, url in data_output:
    print(game_id)
    print(url)

    r = s.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    review_cards = soup.find_all('div', class_='review_content')


    score_class = re.compile('metascore_w user medium game .*')
    for review in range(len(review_cards)):
        prevention = len(review_cards) - 3
        if review < prevention:
            user_wrap = review_cards[review].find('div', class_='name')
            username = user_wrap.find('a')
            if username:
                username = username.text
            else:
                username = user_wrap.find('span').text
            review_date = review_cards[review].find('div', class_='date').text
            score = review_cards[review].find('div', class_=score_class).text

            username = username.lower()

            if not user_is_registered(username):
                register_user(username)
            
            user_id = get_user_id(username)

            user_data = {
                "username": username,
                "review_date": format_date(review_date),
                "score": int(score),
                "game_id": int(game_id),
                "user_id" : user_id
            }

            review_data.append(user_data)

            
print(review_data)


with open('reviews_data.json', 'w') as outfile:
    json.dump(review_data, outfile)

with open('users_data.csv', 'w') as usersfile:
    csv_users = csv.writer(usersfile)
    for row in users_registered:
        csv_users.writerow(row)
