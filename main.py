import os
import requests
from dotenv import load_dotenv
import time
from telegram import Bot

DVMN_URL = 'https://dvmn.org/api/long_polling/'


def get_user_reviews(dvmn_token, bot_token, chat_id):
    timestamp = time.time()
    api_url = DVMN_URL
    while True:
        try:
            response = requests.get(
                api_url,
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

                title = result['lesson_title']
                url = result['lesson_url']
                if result['is_negative']:
                    result = (
                        'Работа не принята. Нужно исправить несколько ошибок.'
                    )
                else:
                    result = (
                        'Все хорошо! Можно приступать к следующему уроку!'
                    )

                message = 'Преподаватель проверил работу:' \
                          ' [{}]({}) \n {}'.format(title, url, result)
                bot = Bot(token=bot_token)
                bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='markdown')
            elif status == 'timeout':
                timestamp = reviews['timestamp_to_request']

        except requests.exceptions.HTTPError as err:
            print(f"Возникла ошибка при выполнении HTTP-запроса:\n{err}")
        except requests.exceptions.ConnectionError:
            time.sleep(90)
            continue
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    load_dotenv()
    dvmn_token = os.environ["DVMN_TOKEN"]
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["CHAT_ID"]

    get_user_reviews(dvmn_token, bot_token, chat_id)
