import requests
import os
from urllib.parse import urlparse

FOLDER_NAME = 'images'

def get_photos_links_spacex(launch_id='5eb87d46ffd86e000604b388'):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']

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

def download_spacex_images(launch_id='5eb87d46ffd86e000604b388', folder=FOLDER_NAME):
    os.makedirs(folder, exist_ok=True)
    
    spacex_links = get_photos_links_spacex(launch_id)
    
    for i, link in enumerate(spacex_links):
        print(f"Скачиваю {i+1} из {len(spacex_links)}: {link}")
        save_image_from_url(link, folder, i, prefix='spacex_photo')
    
    print(f"Готово! Скачано {len(spacex_links)} фото в папку '{folder}'")
    return len(spacex_links)

def main():
    try:
        download_spacex_images()
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
    except KeyError as e:
        print(f"Ошибка в структуре данных API: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == '__main__':
    main()
