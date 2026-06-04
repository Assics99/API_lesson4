import os
import time
import argparse
import telegram

def get_photos(folder):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def send_photos(bot, photos, chat_id):
    for photo_path in photos:
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    BOT_TOKEN = os.environ.get('TG_KEY')
    CHAT_ID = os.environ.get('TG_CHAT_ID')
    
    # Проверяем наличие необходимых переменных окружения
    if not BOT_TOKEN:
        print("Ошибка: переменная окружения TG_KEY не установлена")
        return
    if not CHAT_ID:
        print("Ошибка: переменная окружения TG_CHAT_ID не установлена")
        return
    
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Папка с фото")
    parser.add_argument("interval", type=float, help="Интервал в часах")
    args = parser.parse_args()

    bot = telegram.Bot(token=BOT_TOKEN)

    while True:
        photos = get_photos(args.folder)
        if photos:
            send_photos(bot, photos, CHAT_ID)
        time.sleep(args.interval * 3600)

if __name__ == "__main__":
    main()
