def get_ranking():
    import requests

    from datetime import datetime
    from zoneinfo import ZoneInfo

    jst = ZoneInfo("Asia/Tokyo")
    jst_now = datetime.now(jst)

    formatted_time = jst_now.strftime("%Y-%m-%d %H:%M:%S %Z")
    print(formatted_time)

    url = "https://game.nogikoi.jp/love50472/reward/rank_list/69/2?_=1749267997789"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23049PCD8G Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/136.0.7103.125 Mobile Safari/537.36 Android nkpj05",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-JS-VERSION": "202506061608",
        "sec-ch-ua-platform": '"Android"',
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="136", "Android WebView";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://game.nogikoi.jp/?1749267997555",
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    cookies = {
        "u_id": "c67d6bcf-c8d3-4aa2-93ee-e5080d1fa3e0",
        "fuel_csrf_token": "bac32e4c77d5a581ffe71f7fc2fed4241475e08b8b2684d8d3362f0a50b5f2e19bf11931e44f41dca0f95a2c3912779cb790147e38434bc12bd47e28ceaeda67",
    }

    response = requests.get(url, headers=headers, cookies=cookies)

    print(response.status_code)
    print(response.json())  # if the response is JSON

    import json

    with open("sample.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)

    result = ""
    for item in response.json().get("list", []):
        temp = f"Rank: {item.get('rank'):02d}, Score: {item.get('score')}, Name: {item.get('name')}"
        print(temp)
        result += temp + "\n"
    result += formatted_time

    import os
    import time
    import requests

    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

    def send_telegram_message(
        text, chat_id=TELEGRAM_CHAT_ID, bot_token=TELEGRAM_BOT_TOKEN
    ):
        while True:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": text,
                }

                response = requests.post(url, json=payload)
                response_body = response.json()
                if "error_code" not in response_body:
                    time.sleep(5)
                    return
                else:
                    print(response_body)
                    time.sleep(5)
                    return
            except Exception as e:
                print(e)
                time.sleep(5)
                pass

    send_telegram_message(
        result, chat_id=TELEGRAM_CHAT_ID, bot_token=TELEGRAM_BOT_TOKEN
    )
    print("Message sent to Telegram successfully.")


if __name__ == "__main__":
    import time

    while True:
        try:
            get_ranking()
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)
