from fastapi import APIRouter
from schemas import Caisse, CaisseData
from typing import List

router = APIRouter(
    prefix='/caisse',tags=['Caisse']
)


@router.get('/all', response_model=List[Caisse])
def get_caisses():
    ...


@router.get('/{id}', response_model=Caisse)
def get_caisse(id:str):
    ...


@router.post('/')
def post_caisse(caisse:CaisseData):
    ...


@router.put('/{id}')
def modify_caisse(id:str, caisse:CaisseData):
    ...


@router.delete('/{id}')
def delete_caisse(id:str):
    ...
