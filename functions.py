
from globals import DATABASE_URI
from globals import DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD
from py2neo import Graph
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from mimetypes import guess_extension

# from PIL import Image
# from os import getcwd


graph_driver = lambda credentials: Graph(uri=DATABASE_URI,auth=(DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD))
# graph_driver = lambda credentials: Graph(uri=DATABASE_URI,auth=(credentials['email'],credentials['password']))


def save_image(image:UploadFile):
    file_name = str(datetime.now().timestamp()).replace('.','')
    file_name = f'images/image_{file_name}{guess_extension(image.content_type)}'
    with open(file_name, 'wb') as f:
        f.write(image.file.read())
    return file_name

def encode_password(password) -> str:
    from passlib.context import CryptContext    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_email(email):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Invalid or not existing email"
        )
    

# PATH_FILES = getcwd() + "/"
# def resize_image(filename: str):

#     sizes = [{
#         "width": 500,
#         "height": 500
#     }]

#     for size in sizes:
#         size_defined = size['width'], size['height']

#         image = Image.open(PATH_FILES + filename, mode="r")
#         image.thumbnail(size_defined)
#         image.save(PATH_FILES + str(size['height']) + "_" + filename)
