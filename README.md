# Космический Телеграм

Проект для автоматизации сбора фотографий космоса (NASA APOD, NASA EPIC, SpaceX) и их публикации в Telegram-канале.

## Как установить

### Предварительные требования
- Python 3.6 или выше.
- Установленный менеджер пакетов pip.

### Установка зависимостей
1. Создайте виртуальное окружение:
```bash
python -m venv venv
```
2. Активируйте его:
```bash
venv\Scripts\activate
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Проверьте, что все библиотеки установились без ошибок:
```bash
pip list
```

## Настройка API-ключей

Для работы скриптов потребуется ключ NASA API. Его необходимо сохранить в переменные окружения.

### NASA API Key
Этот ключ нужен для загрузки фотографий с серверов NASA.
1. Перейдите на сайт NASA API: https://api.nasa.gov/
2. Нажмите Generate API Key.
3. Заполните форму (укажите имя и email) и нажмите Signup.
4. Скопируйте полученный ключ.

### Telegram Bot Token
Токен нужен для публикации фотографий в Telegram-канале.
1. Напишите в Telegram @BotFather
2. Отправьте команду /newbot
3. Придумайте имя и username для бота (username должен заканчиваться на bot)
4. Скопируйте полученный токен (например, 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz)

### Telegram Chat ID
ID чата или канала, куда бот будет отправлять фотографии.
- Для канала: добавьте бота в администраторы канала, затем перешлите любое сообщение из канала в @userinfobot — вы увидите ID с минусом (например, -1001234567890)
- Для личного чата: напишите @userinfobot и получите свой ID

## Настройка переменных окружения
Для безопасного хранения ключей поместите их в переменные окружения. Создайте в корне проекта файл `.env`:
```env
NASA_API_KEY=ваш_ключ_от_NASA
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
TELEGRAM_CHAT_ID=@ваш_канал_или_id_чата
```
Примечание: убедитесь, что файл .env добавлен в `.gitignore`, чтобы случайно не опубликовать секретные данные на GitHub.

### Проверка переменных окружения
Запустите в консоли (временно, для проверки):
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('NASA_API_KEY:', bool(os.getenv('NASA_API_KEY'))); print('TELEGRAM_BOT_TOKEN:', bool(os.getenv('TELEGRAM_BOT_TOKEN'))); print('TELEGRAM_CHAT_ID:', bool(os.getenv('TELEGRAM_CHAT_ID')))"
```
Вывод должен быть:
```text
NASA_API_KEY: True
TELEGRAM_BOT_TOKEN: True
TELEGRAM_CHAT_ID: True
```

## Быстрый запуск

### Загрузка фотографий NASA APOD
Загружает 10 фотографий из Astronomy Picture of the Day:
```bash
python download_NASA_photos.py
```
Скрипт не выводит сообщений в консоль. Фотографии сохраняются в папку `images/`

### Загрузка фотографий NASA EPIC
Загружает снимки Земли с камеры EPIC:
```bash
python download_EPIC_photos.py
```

### Загрузка фотографий SpaceX
Загружает последние снимки запусков SpaceX:
```bash
python download_SpaceX_photos.py
```

### Проверка загруженных фото
Чтобы убедиться, что скрипты загрузки сработали:
```bash
ls images/
```
Вывод должен быть примерно таким:
```text
photo_0.jpg  photo_1.png  photo_2.jpg  photo_3.jpg  photo_4.jpg
photo_5.jpg  photo_6.jpg  photo_7.jpg  photo_8.jpg  photo_9.jpg
```

### Публикация в Telegram (однократная отправка)
Для отправки всех фотографий из папки `images/` в Telegram-канал:
```bash
python tg_bot.py images/
```
Пример вывода в консоли:
```text
Запуск бота. Папка: images/, Интервал: 4.0 часов
Отправлено: images/photo_0.jpg
Отправлено: images/photo_1.png
Отправлено: images/photo_2.jpg
Ожидание 4.0 часов до следующей отправки...
```

### Публикация в Telegram (с периодичностью)
Для отправки фото каждые N часов:
```bash
python tg_bot.py images/ 24
```
Это отправит все фото из папки `images/` и будет повторять отправку каждые 24 часа.
Пример вывода:
```text
Запуск бота. Папка: images/, Интервал: 24.0 часов
Отправлено: images/photo_0.jpg
Отправлено: images/photo_1.png
Отправлено: images/photo_2.jpg
Ожидание 24.0 часов до следующей отправки...
```
Если фотографий в папке нет:
```text
Запуск бота. Папка: images/, Интервал: 4.0 часов
Ожидание 4.0 часов до следующей отправки...
```

## Структура проекта
После успешного выполнения скриптов в папке проекта появится:
```text
ваш_проект/
├── images/
│   ├── photo_0.jpg
│   ├── photo_1.png
│   ├── photo_2.jpg
│   └── ...
├── download_EPIC_photos.py
├── download_NASA_photos.py
├── download_SpaceX_photos.py
├── download_tools.py
├── tg_bot.py
├── .env
├── .gitignore
└── requirements.txt
```

## Возможные ошибки при запуске
| Ошибка | Решение |
|--------|---------|
| `ModuleNotFoundError: No module named 'requests'` | Запустите `pip install -r requirements.txt` |
| `KeyError: 'NASA_API_KEY'` | Проверьте наличие `NASA_API_KEY=ваш_ключ` в файле `.env` |
| `requests.exceptions.HTTPError: 403` | Неверный API ключ, получите новый на https://api.nasa.gov/ |
| `requests.exceptions.ConnectionError` | Проверьте интернет-соединение |
| `ValueError: переменная окружения TELEGRAM_BOT_TOKEN не установлена` | Добавьте `TELEGRAM_BOT_TOKEN` в файл `.env` |
| `ValueError: переменная окружения TELEGRAM_CHAT_ID не установлена` | Добавьте `TELEGRAM_CHAT_ID` в файл `.env` |
| `telegram.error.Unauthorized` | Неверный токен бота, проверьте TELEGRAM_BOT_TOKEN в .env |
| `telegram.error.ChatNotFound` | Неверный CHAT_ID, проверьте TELEGRAM_CHAT_ID в .env |
| `RuntimeWarning: coroutine 'Bot.send_photo' was never awaited` | В `requirements.txt` должна быть версия `python-telegram-bot==13.7` или ниже. Удалите старую версию и установите правильную: `pip uninstall python-telegram-bot && pip install python-telegram-bot==13.7` |
| `Сетевая ошибка при отправке` | Бот автоматически повторит попытку через 5 секунд |

## Подробный запуск

### download_NASA_photos.py
```bash
python download_NASA_photos.py
```
Что делает:
- Загружает 10 фотографий из NASA Astronomy Picture of the Day (APOD)
- Сохраняет их в папку `images/`
- Автоматически определяет расширение файла

### download_EPIC_photos.py
```bash
python download_EPIC_photos.py
```
Что делает:
- Загружает последние снимки Земли с камеры EPIC (Earth Polychromatic Imaging Camera)
- Сохраняет их в папку `images/`

### download_SpaceX_photos.py
```bash
python download_SpaceX_photos.py
```
Что делает:
- Загружает фотографии с последних запусков SpaceX из публичного API
- Сохраняет их в папку `images/`

### download_tools.py
Вспомогательный модуль с общими функциями:
- Скачивание файлов по URL
- Создание папки `images/` при необходимости
- Другие утилиты для работы с изображениями

### tg_bot.py
Запуск с интервалом по умолчанию (4 часа):
```bash
python tg_bot.py images/
```
Запуск с пользовательским интервалом (например, 24 часа):
```bash
python tg_bot.py images/ 24
```
Аргументы:
- `folder` (обязательный) — путь к папке с фотографиями
- `interval` (опционально) — интервал между отправками в часах (по умолчанию: 4)

Что делает:
1. Сканирует указанную папку на наличие изображений (поддерживаются: jpg, jpeg, png, webp)
2. Отправляет все найденные фото в Telegram-канал
3. При сетевых ошибках автоматически повторяет попытку через 5 секунд
4. После отправки всех фото ждет указанный интервал и повторяет цикл

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков `dvmn.org`: [dvmn.org](https://dvmn.org/)
