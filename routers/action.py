from fastapi import APIRouter
from schemas import Action
from typing import List
from fastapi_pagination import Page, paginate

router = APIRouter(
    prefix='/action',tags=['Action']
)

@router.get('/all', response_model=Page[Action])
def get_actions():
    return paginate([])
    ...
