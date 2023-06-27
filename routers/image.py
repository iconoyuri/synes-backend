from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix='/image',tags=['Image']
)

try:
    os.mkdir('images')
except:
    ...

@router.get('/images/{file_name}',response_class=FileResponse)
def get_image(file_name:str):
    print(file_name)
    return FileResponse(f"images/{file_name}")