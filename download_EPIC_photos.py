import os
from datetime import datetime
import requests
from download_tools import save_image_from_url  # импортируем общую функцию

FOLDER_NAME = 'images'

def get_epic_images(api_key, count=10):
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    images = []
    for item in data[:count]:
        image_name = item["image"]
        date_str = item["date"]
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date = dt.strftime('%Y-%m-%d')
        year, month, day = date.split("-")
        image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/jpg/{image_name}.jpg"
        images.append(image_url)
    return images

def download_epic_images(api_key, folder=FOLDER_NAME, count=10):
    epic_links = get_epic_images(api_key, count)
    
    for index, link in enumerate(epic_links):
        print(f"Скачиваю {index + 1} из {len(epic_links)}: {link}")
        save_image_from_url(link, folder, index, prefix='epic_photo')  # используем общую функцию
    
    print(f"Готово! Скачано {len(epic_links)} EPIC фото в папку '{folder}'")
    return len(epic_links)

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        print("Ошибка: переменная окружения NASA_API_KEY не установлена")
        return
    
    try:
        download_epic_images(api_key=api_key, folder=FOLDER_NAME, count=10)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
