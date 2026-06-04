import requests
import os
from urllib.parse import urlparse
from datetime import datetime

FOLDER_NAME = 'images'

def get_photos_links_nasa(api_key, count=10):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": count
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    links = []
    for item in data:
        if 'url' in item:
            links.append(item['url'])
    return links

def get_file_extension(url):
    path = urlparse(url).path
    result = os.path.splitext(path)
    extension = result[1]
    return extension

def save_image_from_url(url, folder, index, prefix='photo'):
    response = requests.get(url)
    response.raise_for_status()
    
    extension = get_file_extension(url)
    if not extension:
        extension = '.jpg'
    
    file_path = os.path.join(folder, f'{prefix}_{index}{extension}')
    
    with open(file_path, 'wb') as file:
        file.write(response.content)

def download_nasa_images(api_key, folder=FOLDER_NAME, count=10):
    os.makedirs(folder, exist_ok=True)
    
    nasa_links = get_photos_links_nasa(api_key, count)
    
    for i, link in enumerate(nasa_links):
        print(f"Скачиваю {i+1} из {len(nasa_links)}: {link}")
        save_image_from_url(link, folder, i, prefix='nasa_photo')
    
    print(f"Готово! Скачано {len(nasa_links)} фото в папку '{folder}'")
    return len(nasa_links)

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('API_KEY')
    if not api_key:
        print("Ошибка: переменная окружения API_KEY не установлена")
        return
    
    try:
        download_nasa_images(api_key=api_key, folder=FOLDER_NAME, count=10)
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == '__main__':
    main()
