from fastapi import APIRouter
from schemas import User, UserData
from typing import List

router = APIRouter(
    prefix='/user',tags=['User']
)


@router.get('/all', response_model=List[User])
def get_profiles():
    ...


@router.get('/{id}', response_model=User)
def get_profile(id:str):
    ...


@router.post('/')
def post_profile(profile:UserData):
    ...


@router.put('/{id}')
def modify_profile(id:str, profile:UserData):
    ...


@router.delete('/{id}')
def delete_profile(id:str):
    ...
