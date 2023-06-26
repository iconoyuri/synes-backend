
from globals import DATABASE_URI
from globals import DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD
from py2neo import Graph
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from email_validator import validate_email, EmailNotValidError
# from PIL import Image
# from os import getcwd


graph_driver = lambda username,password: Graph(uri=DATABASE_URI,auth=(username,password))


def save_image(image:UploadFile):
    file_name = str(datetime.timestamp)
    with open(f'{file_name}', 'wb') as f:
        f.write(image.file)
        image.content
    return file_name

default_driver = graph_driver(DATABASE_DEFAULT_USERNAME, DATABASE_DEFAULT_PASSWORD)

def encode_password(password) -> str:
    from passlib.context import CryptContext    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password

def parse_credentials(credentials:str):
    email = credentials[0:credentials.index('\\\\')]
    password = credentials[credentials.index('\\\\')+2:]

    return {'email':email,'password':password}


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
