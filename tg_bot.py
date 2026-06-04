import os
import time
import argparse
import telegram

def get_photos(folder):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def open_photo(photo_path):
    """Открывает фото и возвращает файловый объект"""
    return open(photo_path, "rb")

def send_single_photo(bot, chat_id, photo_path):
    """Отправляет одно фото по заданному пути"""
    with open_photo(photo_path) as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)

def send_photos(bot, chat_id, photos):
    """Отправляет список фото (теперь только управляет порядком)"""
    for photo_path in photos:
        send_single_photo(bot, chat_id, photo_path)

def validate_environment():
    """Проверяет наличие необходимых переменных окружения"""
    from dotenv import load_dotenv
    load_dotenv()
    
    BOT_TOKEN = os.environ.get('TG_KEY')
    CHAT_ID = os.environ.get('TG_CHAT_ID')
    
    if not BOT_TOKEN:
        raise ValueError("Ошибка: переменная окружения TG_KEY не установлена")
    if not CHAT_ID:
        raise ValueError("Ошибка: переменная окружения TG_CHAT_ID не установлена")
    
    return BOT_TOKEN, CHAT_ID

def parse_arguments():
    """Разбирает аргументы командной строки"""
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
        nargs='?',  # Делаем аргумент необязательным
        default=4.0,  # Значение по умолчанию - 4 часа
        help="Интервал в часах (по умолчанию: 4 часа)"
    )
    return parser.parse_args()

def run_bot_loop(bot, chat_id, folder, interval_hours):
    """Основной цикл отправки фото"""
    while True:
        photos = get_photos(folder)
        if photos:
            send_photos(bot, chat_id, photos)
        time.sleep(interval_hours * 3600)

def main():
    try:
        BOT_TOKEN, CHAT_ID = validate_environment()
        args = parse_arguments()
        
        bot = telegram.Bot(token=BOT_TOKEN)
        print(f"Запуск бота. Папка: {args.folder}, Интервал: {args.interval} часов")
        run_bot_loop(bot, CHAT_ID, args.folder, args.interval)
        
    except ValueError as e:
        print(e)
        return

if __name__ == "__main__":
    main()
