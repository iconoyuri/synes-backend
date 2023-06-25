from fastapi import APIRouter
from schemas import Fond, FondData
from typing import List

router = APIRouter(
    prefix='/fond',tags=['Fond']
)


@router.get('/all', response_model=List[Fond])
def get_fonds():
    ...


@router.get('/{id}', response_model=Fond)
def get_fond(id:str):
    ...


@router.post('/')
def post_fond(fond:FondData):
    ...


@router.put('/{id}')
def modify_fond(id:str, fond:FondData):
    ...


@router.delete('/{id}')
def delete_fond(id:str):
    ...
