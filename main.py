import os
import requests
from dotenv import load_dotenv
from pprint import pprint
import  time

def get_user_reviews(dvmn_token):
    # url = 'https://dvmn.org/api/user_reviews/'
    timestamp = time.time()
    url = 'https://dvmn.org/api/long_polling/'
    while True:
      try:
        response = requests.get(
          url,
          headers={'Authorization': f'Token {dvmn_token}'},
          params={'timestamp': timestamp},
          timeout=60
        )
        response.raise_for_status()
        reviews = response.json()
        pprint(reviews)

      except requests.exceptions.HTTPError as err:
        print(f"Возникла ошибка при выполнении HTTP-запроса:\n{err}")
      except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        continue


if __name__ == '__main__':
  load_dotenv()
  dvmn_token = os.environ["DVMN_TOKEN"]
  get_user_reviews(dvmn_token)


