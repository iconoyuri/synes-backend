from fastapi import APIRouter
from schemas import Fond, FondData
from typing import List
from fastapi_pagination import Page, paginate

router = APIRouter(
    prefix='/fond',tags=['Fond']
)


@router.get('/all', response_model=Page[Fond])
def get_fonds():
    return paginate([])
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
