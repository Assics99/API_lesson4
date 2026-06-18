import os
import time
import argparse
import telegram
from telegram.error import NetworkError, TimedOut

def get_photos(folder):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def send_single_photo(bot, chat_id, photo_path):
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)

def send_photos(bot, chat_id, photos):
    for photo_path in photos:
        send_single_photo(bot, chat_id, photo_path)

def validate_environment():
    from dotenv import load_dotenv
    load_dotenv()
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token:
        raise ValueError("Ошибка: переменная окружения TELEGRAM_BOT_TOKEN не установлена")
    if not chat_id:
        raise ValueError("Ошибка: переменная окружения TELEGRAM_CHAT_ID не установлена")
    
    return bot_token, chat_id

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Бот для отправки фотографий из указанной папки в Telegram"
    )
    parser.add_argument(
        "folder", 
        help="Папка с фото"
    )
    parser.add_argument(
        "interval", 
        type=float, 
        nargs='?',
        default=4.0,
        help="Интервал в часах (по умолчанию: 4 часа)"
    )
    return parser.parse_args()

def send_photos_with_retry(bot, chat_id, photos, retry_delay=5):
    for photo_path in photos:
        while True:
            try:
                send_single_photo(bot, chat_id, photo_path)
                break
            except (NetworkError, TimedOut) as e:
                print(f"Сетевая ошибка при отправке {photo_path}: {e}")
                print(f"Повторная попытка через {retry_delay} секунд...")
                time.sleep(retry_delay)
            except Exception as e:
                print(f"Неожиданная ошибка при отправке {photo_path}: {e}")
                break

def run_bot_loop(bot, chat_id, folder, interval_hours, retry_delay=5):
    while True:
        try:
            photos = get_photos(folder)
            if photos:
                send_photos_with_retry(bot, chat_id, photos, retry_delay)
        except (NetworkError, TimedOut) as e:
            print(f"Сетевая ошибка в основном цикле: {e}")
            print(f"Повторная попытка через {retry_delay} секунд...")
            time.sleep(retry_delay)
            continue
        except Exception as e:
            print(f"Неожиданная ошибка в основном цикле: {e}")
        
        print(f"Ожидание {interval_hours} часов до следующей отправки...")
        time.sleep(interval_hours * 3600)

def main():
    bot_token, chat_id = validate_environment()
    args = parse_arguments()
    
    bot = telegram.Bot(token=bot_token)
    print(f"Запуск бота. Папка: {args.folder}, Интервал: {args.interval} часов")
    run_bot_loop(bot, chat_id, args.folder, args.interval)

if __name__ == "__main__":
    main()
