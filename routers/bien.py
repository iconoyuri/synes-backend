from fastapi import APIRouter, UploadFile
from schemas import Bien, BienData
from typing import List

router = APIRouter(
    prefix='/bien',tags=['Bien']
)


@router.get('/all', response_model=List[Bien])
def get_biens():
    ...


@router.get('/{id}', response_model=Bien)
def get_bien(id:str):
    ...


@router.post('/')
def post_bien(bien:BienData):
    ...


@router.put('/{id}')
def modify_bien(id:str, bien:BienData):
    ...


@router.delete('/{id}')
def delete_bien(id:str):
    ...


@router.post('/photos')
def upload_bien_photo(photos:List[UploadFile]):
    ...

