# pip instal
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
KEYWORD = os.getenv("KEYWORD")

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

headers = {
    "Authorization": f"Bearer {X_BEARER_TOKEN}"
}

last_tweet_id = None


def search_latest_tweet():
    params = {
        "query": KEYWORD,
        "max_results": 10,
        "tweet.fields": "created_at,author_id"
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params)
    data = response.json()

    if "data" not in data:
        return None

    return data["data"][0]  # 最新的一条


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)


def main():
    global last_tweet_id

    print("Am i star?T:", KEYWORD)

    while True:
        try:
            tweet = search_latest_tweet()

            if tweet:
                tweet_id = tweet["id"]

                if last_tweet_id is None:
                    last_tweet_id = tweet_id

                if tweet_id != last_tweet_id:
                    text = f"*New: {KEYWORD}\nTweet ID: {tweet_id}\n Say: {tweet['text']}\n Yea: https://x.com/i/web/status/{tweet_id}"
                    send_telegram_message(text)
                    last_tweet_id = tweet_id
                    print("✌")

        except Exception as e:
            print("😔:", e)
          
        time.sleep(60)  # 每 60 秒检查一次
      
if __name__ == "__main__":
    main()
