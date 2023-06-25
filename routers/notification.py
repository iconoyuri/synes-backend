from fastapi import APIRouter
from schemas import Notification
from typing import List

router = APIRouter(
    prefix='/notification',tags=['Notification']
)

@router.get('/all', response_model=List[Notification])
def get_notifications():
    ...
