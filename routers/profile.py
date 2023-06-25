from fastapi import APIRouter, UploadFile
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


@router.post('/')
def post_profile_photo(photo:UploadFile):
    ...


@router.put('/{id}')
def modify_profile(id:str, profile:UserData):
    ...


@router.delete('/{id}')
def delete_profile(id:str):
    ...


@router.post('/section/{id_user}/{id_section}')
def affect_to_section(id_user:str,id_section:str):
    ...


@router.post('/password/{previous_pwd}/{new_pwd}')
def affect_to_section(previous_pwd:str,new_pwd:str):
    ...
