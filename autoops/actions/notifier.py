import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[TELEGRAM] not sent: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is missing")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        }, timeout=(5, 10))
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            print("[TELEGRAM] invalid response from Telegram API")
            return False
        if not payload.get("ok"):
            print("[TELEGRAM] rejected:", payload.get("description", "unknown API error"))
            return False
        print("[TELEGRAM] message delivered")
        return True

    except requests.RequestException as exc:
        print(f"[TELEGRAM] request failed ({type(exc).__name__})")
    except ValueError:
        print("[TELEGRAM] invalid response from Telegram API")
    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Send one AutoOps Telegram test message")
    parser.add_argument("--test", action="store_true", help="send one test message to the configured chat")
    args = parser.parse_args()
    if not args.test:
        parser.error("use --test to send one test message")

    delivered = send_telegram("AutoOps Telegram test: message delivery is working.")
    return 0 if delivered else 1


if __name__ == "__main__":
    raise SystemExit(main())

