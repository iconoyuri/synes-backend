
from globals import DATABASE_URI
from globals import DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD
from py2neo import Graph
from datetime import datetime
from fastapi import UploadFile


graph_driver = lambda username,password: Graph(uri=DATABASE_URI,auth=(username,password))


def save_image(image:UploadFile):
    file_name = str(datetime.timestamp)
    with open(f'{file_name}', 'wb') as f:
        f.write(image.file)
        image.content
    return file_name