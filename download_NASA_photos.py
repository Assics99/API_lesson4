import requests
import os


from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


folder_name = 'images'


if not os.path.exists(folder_name):
    os.makedirs(folder_name)


def get_photos_links_NASA():
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": os.environ['API_KEY'] ,
        "count": 10
    }


links_Nasa = get_photos_links_NASA()


def get_file_extension(url):
    path = urlparse(url).path
    result = os.path.splitext(path)
    extension = result[1]
    return extension


def main():
    for i in range(0,len(link_NASA)):
        response = requests.get(link_NASA[i])
        response.raise_for_status()

        file_path = os.path.join(folder_name, f'photo_{i}.{get_file_extension(link_NASA[i])}')

        with open(file_path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    main()        