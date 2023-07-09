from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Contribution, ContributionData
from fastapi_pagination import LimitOffsetPage, paginate
import py2neo_schemas as nodes
from typing import List
from functions import graph_driver
from oauth2 import get_current_user

router = APIRouter(
    prefix='/contribution', tags=['Contribution']
)


# @router.get('/all', response_model=LimitOffsetPage[Contribution])
# def get_contributions():
#     driver = graph_driver(credentials)

#     fond = nodes.Fond.match(driver, fond_id).first()
#     if not fond:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     contributions = [
#         Contribution(id_fond=fond.__node__.identity, email_user=user.adresse_mail, montant=fond.contributeurs.get(user, 'montant'), date_creation=fond.contributeurs.get(user, 'date')) for user in list(fond.contributeurs)
#     ]

#     return all_contributions
#     return paginate(all_contributions)
# ...


@router.get('/{fond_id}', response_model=LimitOffsetPage[Contribution])
def get_contributions(fond_id: int, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    fond = nodes.Fond.match(driver, fond_id).first()
    if not fond:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    contributions = [
        Contribution(id_fond=fond.__node__.identity, email_user=user.adresse_mail, montant=fond.contributeurs.get(user, 'montant'), date_creation=fond.contributeurs.get(user, 'date')) for user in list(fond.contributeurs)
    ]

    return paginate(contributions)
    ...


@router.post('/')
def post_contribution(contribution: ContributionData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    if contribution.montant <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Montant inférieur à 1")

    createur = nodes.User.match(driver, contribution.email_user).first()
    if not createur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    fond = nodes.Fond.match(driver, contribution.id_fond).first()
    if not fond:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    caisse = list(fond.caisse)[0] if len(list(fond.caisse)) > 0 else None
    if not caisse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="caisse non existante")
    from datetime import datetime
    time = datetime.now()
    time_str = str(time)
    createur.fonds_contribues.add(
        fond, {
            'montant': contribution.montant + createur.fonds_contribues.get(fond, 'montant'),
            'date': time_str
        })
    caisse.montant_courant = caisse.montant_courant + contribution.montant
    driver.push(createur)
    driver.push(caisse)
    ...
