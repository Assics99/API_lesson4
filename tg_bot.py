import os
import time
import argparse
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import NetworkError, TimedOut, TelegramError

def get_photos(folder):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    try:
        files = os.listdir(folder)
    except OSError as e:
        raise OSError(f"Не удалось прочитать папку {folder}: {e}")
    
    return [os.path.join(folder, f) for f in files if f.lower().endswith(exts)]

def send_single_photo(bot, chat_id, photo_path):
    try:
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
    except OSError as e:
        raise OSError(f"Не удалось открыть файл {photo_path}: {e}")

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
            except TelegramError as e:
                print(f"Ошибка Telegram при отправке {photo_path}: {e}")
                break
            except OSError as e:
                print(f"Ошибка файловой системы при отправке {photo_path}: {e}")
                break

def validate_environment():
    try:
        load_dotenv()
    except Exception:
        pass
    
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
    args = parser.parse_args()
    
    if args.interval <= 0:
        raise ValueError("Интервал должен быть положительным числом")
    
    return args

def run_bot_loop(bot, chat_id, folder, interval_hours, retry_delay=5):
    while True:
        try:
            photos = get_photos(folder)
            if photos:
                print(f"Найдено {len(photos)} фотографий. Начинаю отправку...")
                send_photos_with_retry(bot, chat_id, photos, retry_delay)
                print(f"Отправка завершена. Ожидание {interval_hours} часов...")
            else:
                print(f"В папке {folder} не найдено фотографий")
        except (NetworkError, TimedOut) as e:
            print(f"Сетевая ошибка в основном цикле: {e}")
            print(f"Повторная попытка через {retry_delay} секунд...")
            time.sleep(retry_delay)
            continue
        except TelegramError as e:
            print(f"Ошибка Telegram в основном цикле: {e}")
            print("Остановка программы...")
            break
        except OSError as e:
            print(f"Ошибка файловой системы в основном цикле: {e}")
            print("Остановка программы...")
            break
        
        time.sleep(interval_hours * 3600)

def main():
    try:
        bot_token, chat_id = validate_environment()
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")
        return
    
    try:
        args = parse_arguments()
    except ValueError as e:
        print(f"Ошибка аргументов: {e}")
        return
    
    try:
        bot = Bot(token=bot_token)
    except TelegramError as e:
        print(f"Ошибка создания бота: {e}")
        return
    
    print(f"Запуск бота. Папка: {args.folder}, Интервал: {args.interval} часов")
    
    try:
        run_bot_loop(bot, chat_id, args.folder, args.interval)
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
