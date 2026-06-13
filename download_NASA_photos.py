import os
import requests
from download_tools import save_image_from_url

FOLDER_NAME = 'images'

def get_photos_links_nasa(api_key, count=10):
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    links = []
    for item in data:
        if item.get('media_type') == 'image':
            image_url = item.get('hdurl') or item.get('url')
            if image_url:
                links.append(image_url)
    return links

def download_nasa_images(api_key, folder=FOLDER_NAME, count=10):
    nasa_links = get_photos_links_nasa(api_key, count)
    
    for i, link in enumerate(nasa_links):
        print(f"Скачиваю {i+1} из {len(nasa_links)}: {link}")
        save_image_from_url(link, folder, i, prefix='nasa_photo')
    
    print(f"Готово! Скачано {len(nasa_links)} фото в папку '{folder}'")
    return len(nasa_links)

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        print("Ошибка: переменная окружения NASA_API_KEY не установлена")
        return
    
    try:
        download_nasa_images(api_key=api_key, folder=FOLDER_NAME, count=10)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
