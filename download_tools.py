import os
import requests
from urllib.parse import urlparse

def get_file_extension(url):
    path = urlparse(url).path
    result = os.path.splitext(path)
    extension = result[1]
    return extension

def save_image_from_url(url, folder, index, prefix='photo'):
    os.makedirs(folder, exist_ok=True)
    
    response = requests.get(url)
    response.raise_for_status()
    
    extension = get_file_extension(url)
    if not extension:
        extension = '.jpg'
    
    file_path = os.path.join(folder, f'{prefix}_{index}{extension}')
    
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    return file_path
