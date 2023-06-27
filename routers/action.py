from fastapi import APIRouter, Depends
from schemas import Action
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate
from oauth2 import get_current_user


router = APIRouter(
    prefix='/action',tags=['Action']
)

@router.get('/all', response_model=LimitOffsetPage[Action])
def get_actions(credentials = Depends(get_current_user)):
    return paginate([])
    ...
