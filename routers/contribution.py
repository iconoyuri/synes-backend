from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Contribution, ContributionData
from fastapi_pagination import LimitOffsetPage, paginate
import py2neo_schemas as nodes
from functions import graph_driver
from oauth2 import get_current_user

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
def post_contribution(contribution:ContributionData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    if contribution.montant <= 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Montant inférieur à 1")

    createur = nodes.User.match(driver, contribution.email_user).first()
    if not createur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    fond = nodes.Fond.match(driver, contribution.id_fond).first()
    if not fond:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    caisse = list(fond.caisse)[0] if len(list(fond.caisse)) > 0 else None    
    if not caisse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="caisse non existante")
    
    # return createur.fonds_contribues.get(fond,'montant')
    createur.fonds_contribues.add(fond, {'montant': contribution.montant + createur.fonds_contribues.get(fond,'montant')})
    caisse.montant_courant = caisse.montant_courant + contribution.montant
    driver.push(createur)
    driver.push(caisse)
    ...
