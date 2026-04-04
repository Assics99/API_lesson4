import os
import time
import argparse
import telegram

BOT_TOKEN = os.environ['TG_KEY']
CHAT_ID = "@space_photos88"

def get_photos(folder):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def send_photos(bot, photos):
    for photo_path in photos:
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=CHAT_ID, photo=photo)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Папка с фото")
    parser.add_argument("interval", type=float, help="Интервал в часах")
    args = parser.parse_args()

    bot = telegram.Bot(token=BOT_TOKEN)

    while True:
        photos = get_photos(args.folder)
        if photos:
            send_photos(bot, photos)
        time.sleep(args.interval * 3600)

if __name__ == "__main__":
    main()
