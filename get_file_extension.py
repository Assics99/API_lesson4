import os
from urllib.parse import urlparse


def get_file_extension(url):
    path = urlparse(url).path
    result = os.path.splitext(path)
    extension = result[1]
    return extension