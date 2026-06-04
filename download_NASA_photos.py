import requests
import os
from urllib.parse import urlparse

folder_name = 'images'

def get_photos_links_NASA(api_key):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": 10
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

def download_image(url, folder, index):
    response = requests.get(url)
    response.raise_for_status()
    
    extension = get_file_extension(url)
    if not extension:
        extension = '.jpg'
    
    file_path = os.path.join(folder, f'photo_{index}{extension}')
    
    with open(file_path, 'wb') as file:
        file.write(response.content)

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('API_KEY')
    if not api_key:
        print("Ошибка: переменная окружения API_KEY не установлена")
        return
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    try:
        links_nasa = get_photos_links_NASA(api_key)
        
        for i, link in enumerate(links_nasa):
            print(f"Скачиваю {i+1} из {len(links_nasa)}: {link}")
            download_image(link, folder_name, i)
        
        print(f"Готово! Скачано {len(links_nasa)} фото в папку '{folder_name}'")
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == '__main__':
    main()
