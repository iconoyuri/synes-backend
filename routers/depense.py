from fastapi import APIRouter
from schemas import Depense, DepenseData
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix='/depense',tags=['Depense']
)


@router.get('/all', response_model=LimitOffsetPage[Depense])
def get_depenses():
    return paginate([])
    ...


@router.get('/{id}', response_model=Depense)
def get_depense(id:str):
    ...


@router.post('/')
def post_depense(depense:DepenseData):
    ...


@router.put('/{id}')
def modify_depense(id:str, depense:DepenseData):
    ...


@router.delete('/{id}')
def delete_depense(id:str):
    ...
