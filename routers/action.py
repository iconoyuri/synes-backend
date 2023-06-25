from fastapi import APIRouter
from schemas import Action
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix='/action',tags=['Action']
)

@router.get('/all', response_model=LimitOffsetPage[Action])
def get_actions():
    return paginate([])
    ...
