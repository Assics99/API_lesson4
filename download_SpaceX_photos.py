import requests
from download_tools import save_image_from_url  # импортируем общую функцию

FOLDER_NAME = 'images'

def get_photos_links_spacex(launch_id='5eb87d46ffd86e000604b388'):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']

def download_spacex_images(launch_id='5eb87d46ffd86e000604b388', folder=FOLDER_NAME):
    spacex_links = get_photos_links_spacex(launch_id)
    
    for i, link in enumerate(spacex_links):
        print(f"Скачиваю {i+1} из {len(spacex_links)}: {link}")
        save_image_from_url(link, folder, i, prefix='spacex_photo')  # используем общую функцию
    
    print(f"Готово! Скачано {len(spacex_links)} фото в папку '{folder}'")
    return len(spacex_links)

def main():
    try:
        download_spacex_images()
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
