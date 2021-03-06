import requests
import pytz
import datetime

def load_attempts():
    api_url = 'https://devman.org/api/challenges/solution_attempts/'
    response = requests.get(api_url, params={'page': 1})
    pages = response.json()['number_of_pages']
    for page in range(2, pages+1):
        for record in response.json()['records']:
            yield record
        response = requests.get(api_url, params={'page': page})

def get_midnighters(records):
    for record in records:
        date_time = get_datetime(record['timestamp'], record['timezone'])
        if date_time and date_time.hour in range(1,5):
            yield record['username'], date_time

def get_datetime(timestamp, tz):
    if timestamp is None or tz is None:
        return None
    return datetime.datetime.fromtimestamp(timestamp, pytz.timezone(tz))

if __name__ == '__main__':
    for username, date_time in get_midnighters(load_attempts()):
        print(
            'User "{0}" sends challenge {1} at {2}'.format(
                username,
                date_time.strftime('%d-%m-%Y'),
                date_time.strftime('%H:%M %Z')
            )
        )
