import requests
import os


from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


folder_name = 'images'


if not os.path.exists(folder_name):
    os.makedirs(folder_name)


def get_epic_images():
    count = 10
    url = "https://api.nasa.gov/EPIC/api/natural?api_key="
    params = {
        "api_key": os.environ['API_KEY'],
    }
    response = requests.get(url)
    data = response.json()
    images = []
    for i in data[:count]:
        image_name = i["image"]
        date = i["date"].split(" ")[0]
        year, month, day = date.split("-")
        image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/jpg/{image_name}.jpg"
        images.append(image_url)
    return images


links_EPIC = get_photos_links_EPIC()


def get_file_extension(url):
    path = urlparse(url).path
    result = os.path.splitext(path)
    extension = result[1]
    return extension


def main():
    for i in range(0,len(links_EPIC)):
        response = requests.get(links_EPIC[i])
        response.raise_for_status()

        file_path = os.path.join(folder_name, f'photo_{i}.{get_file_extension(links_EPIC[i])}')

        with open(file_path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    main()