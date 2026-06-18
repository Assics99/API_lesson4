# Космический Телеграм

Проект для автоматизации сбора фотографий космоса и их публикации в Telegram-канале.

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
   `venv\Scripts\activate`
3. Установите зависимости:
   `pip install -r requirements.txt`

3. Проверьте, что все библиотеки установились без ошибок:
   `pip list`

## Настройка API-ключей

Для работы скриптов потребуется ключ NASA API. Его необходимо сохранить в переменные окружения.

### NASA API Key

Этот ключ нужен для загрузки фотографий с серверов NASA.

1. Перейдите на сайт NASA API: <https://api.nasa.gov/>
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

Для безопасного хранения ключа его нужно поместить в переменные окружения. Создайте в корне проекта файл `.env`:

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

Пример запуска скрипта:

```bash
python download_NASA_photos.py
```

Скрипт не выводит сообщения в консоль. Фотографии сохраняются в папку `images/`

### Проверка результата

Чтобы убедиться, что скрипт сработал, выполните:

```bash
ls images/
```

Вывод должен быть примерно таким:
```text
photo_0.jpg  photo_1.png  photo_2.jpg  photo_3.jpg  photo_4.jpg
photo_5.jpg  photo_6.jpg  photo_7.jpg  photo_8.jpg  photo_9.jpg
```

### Структура после запуска

После успешного выполнения скрипта в папке проекта появится:

```text
ваш_проект/
├── images/
│   ├── photo_0.jpg
│   ├── photo_1.png
│   ├── photo_2.jpg
│   └── ...
├── main.py
├── .env
└── requirements.txt
```

### Возможные ошибки при запуске

Ошибка: `ModuleNotFoundError: No module named 'requests'`
Решение: Запустите `pip install -r requirements.txt`

Ошибка: `KeyError: 'NASA_API_KEY'`
Решение: Проверьте наличие `API_KEY=ваш_ключ` в файле `.env`

Ошибка: `requests.exceptions.HTTPError: 403`
Решение: Неверный API ключ, получите новый на `https://api.nasa.gov/`

Ошибка: `requests.exceptions.ConnectionError`
Решение: Проверьте интернет-соединение

## Подробный запуск

Для запуска скрипта выполните команду:
```bash
python download_NASA_photos.py
```

### Что делает скрипт

1. Загружает 10 фотографий из `NASA Astronomy Picture of the Day (APOD)` (APOD)
2. Сохраняет их в папку `images/`
3. Автоматически определяет расширение файла (jpg/png и т.д.)

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков `dvmn.org`: [dvmn.org](https://dvmn.org/)
