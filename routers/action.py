from fastapi import APIRouter
from schemas import Action
from typing import List

router = APIRouter(
    prefix='/action',tags=['Action']
)

@router.get('/all', response_model=List[Action])
def get_actions():
    ...
