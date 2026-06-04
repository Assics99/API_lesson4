import requests
import os
from urllib.parse import urlparse

folder_name = 'images'

def get_epic_images(api_key, count=10):
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {
        "api_key": api_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    images = []
    for i in data[:count]:
        image_name = i["image"]
        date = i["date"].split(" ")[0]
        year, month, day = date.split("-")
        image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/jpg/{image_name}.jpg"
        images.append(image_url)
    return images

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
    
    file_path = os.path.join(folder, f'epic_photo_{index}{extension}')
    
    with open(file_path, 'wb') as file:
        file.write(response.content)

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('API_KEY')
    if not api_key:
        print("Ошибка: переменная окружения API_KEY не установлена")
        return
    
    # Создаём папку, если её нет
    os.makedirs(folder_name, exist_ok=True)
    
    try:
        epic_links = get_epic_images(api_key)
        
        for i, link in enumerate(epic_links):
            print(f"Скачиваю {i+1} из {len(epic_links)}: {link}")
            download_image(link, folder_name, i)
        
        print(f"Готово! Скачано {len(epic_links)} EPIC фото в папку '{folder_name}'")
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
    except KeyError as e:
        print(f"Ошибка в структуре данных API: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == '__main__':
    main()
