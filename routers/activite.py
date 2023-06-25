from fastapi import APIRouter, UploadFile
from schemas import Activite, ActiviteData
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix='/activite',tags=['Activite']
)


@router.get('/all', response_model=LimitOffsetPage[Activite])
def get_activites():
    return paginate([])
    ...


@router.get('/{id}', response_model=Activite)
def get_activite(id:str):
    ...


@router.post('/')
def post_activite(activite:ActiviteData):
    ...


@router.put('/{id}')
def modify_activite(id:str, activite:ActiviteData):
    ...


@router.delete('/{id}')
def delete_activite(id:str):
    ...


@router.post('/photos/{id}')
def upload_bien_photos(id:str,photos:List[UploadFile]):
    # return id
    ...

