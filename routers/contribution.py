from fastapi import APIRouter
from schemas import Contribution, ContributionData
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix='/contribution',tags=['Contribution']
)


@router.get('/all', response_model=LimitOffsetPage[Contribution])
def get_contributions():
    return paginate([])
    ...


@router.get('/{id}', response_model=Contribution)
def get_contribution(id:str):
    ...


@router.post('/')
def post_contribution(contribution:ContributionData):
    ...
