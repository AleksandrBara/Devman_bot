import os
import requests
from dotenv import load_dotenv
from pprint import pprint
import  time
from telegram import Bot

DVMN_URL = 'https://dvmn.org/api/long_polling/'

def get_user_reviews(dvmn_token, bot_token, chat_id):
    # url = 'https://dvmn.org/api/user_reviews/'
    timestamp = time.time()
    url = DVMN_URL
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

        status = reviews.get('status')
        if status == 'found':
          timestamp = reviews['last_attempt_timestamp']
          result = reviews.get("new_attempts")[0]
          message = 'Работа проверена'

          bot = Bot(token=bot_token)
          bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="markdown")
        elif status == 'timeout':
          timestamp = reviews['timestamp_to_request']

      except requests.exceptions.HTTPError as err:
        print(f"Возникла ошибка при выполнении HTTP-запроса:\n{err}")
      except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        continue


if __name__ == '__main__':
  load_dotenv()
  dvmn_token = os.environ["DVMN_TOKEN"]
  bot_token = os.environ["BOT_TOKEN"]
  chat_id = os.environ["CHAT_ID"]

  get_user_reviews(dvmn_token, bot_token, chat_id)


