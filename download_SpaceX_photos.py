import requests
import os


from urllib.parse import urlparse


folder_name = 'images'


if not os.path.exists(folder_name):
    os.makedirs(folder_name)


def get_photos_links_SpaceX():
    launch_of_id = '5eb87d46ffd86e000604b388'
    url = f'https://api.spacexdata.com/v5/launches/{launch_of_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


links_SpaceX = get_photos_links_SpaceX()


def get_file_extension(url):
    path = urlparse(url).path
    result = os.path.splitext(path)
    extension = result[1]
    return extension


def main():
    for i in range(0,len(links_SpaceX)):
        response = requests.get(links_SpaceX[i])
        response.raise_for_status()

        file_path = os.path.join(folder_name, f'photo_{i}.{get_file_extension(links_SpaceX[i])}')

        with open(file_path, 'wb') as file:
            file.write(response.content) 


if __name__ == '__main__':
    main()