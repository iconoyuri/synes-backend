from fastapi import APIRouter
from schemas import Contribution, ContributionData
from typing import List

router = APIRouter(
    prefix='/contribution',tags=['Contribution']
)


@router.get('/all', response_model=List[Contribution])
def get_contributions():
    ...


@router.get('/{id}', response_model=Contribution)
def get_contribution(id:str):
    ...


@router.post('/')
def post_contribution(contribution:ContributionData):
    ...
