from fastapi import APIRouter
from schemas import Section, SectionData
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix='/section',tags=['Section']
)


@router.get('/all', response_model=LimitOffsetPage[Section])
def get_sections():
    paginate([])
    ...


@router.get('/{id}', response_model=Section)
def get_section(id:str):
    ...


@router.post('/')
def post_section(section:SectionData):
    ...


@router.put('/{id}')
def modify_section(id:str, section:SectionData):
    ...


@router.delete('/{id}')
def delete_section(id:str):
    ...
