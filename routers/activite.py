from fastapi import APIRouter
from schemas import Activite, ActiviteData
from typing import List

router = APIRouter(
    prefix='/activite',tags=['Activite']
)


@router.get('/all', response_model=List[Activite])
def get_activites():
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
