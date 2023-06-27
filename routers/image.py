from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix='/images',tags=['Images']
)

try:
    os.mkdir('images')
except:
    ...

@router.get('/{file_name}',response_class=FileResponse)
def get_image(file_name:str):
    return FileResponse(f"images/{file_name}")