from fastapi import APIRouter
from schemas import Notification
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix='/notification',tags=['Notification']
)

@router.get('/all', response_model=LimitOffsetPage[Notification])
def get_notifications():
    return paginate([])
    ...
