from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Fond, FondData, TinyUser
from fastapi_pagination import LimitOffsetPage, paginate
import py2neo_schemas as nodes
from functions import graph_driver
from oauth2 import get_current_user

router = APIRouter(
    prefix='/fond', tags=['Fond']
)


@router.get('/all', response_model=LimitOffsetPage[Fond])
def get_fonds(credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    fonds = nodes.Fond.match(driver).all()
    fonds = [Fond(
        id=fond.__node__.identity,
        date_creation=fond.date_creation,
        createur=TinyUser(
            email=list(fond.createur)[0].adresse_mail,
            nom=list(fond.createur)[0].nom
        ) if len(list(fond.createur)) > 0 else None,
        id_caisse=list(fond.caisse)[0].__node__.identity if len(
            list(fond.caisse)) > 0 else None,
        titre=fond.titre,
        description=fond.description,
        montant=fond.montant
    )
        for fond in fonds]

    return paginate(fonds)
    ...


@router.get('/{id}', response_model=Fond)
def get_fond(id: int, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    fond = nodes.Fond.match(driver, id).first()
    if not fond:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    fond = Fond(
        id=fond.__node__.identity,
        date_creation=fond.date_creation,
        createur=TinyUser(
            email=list(fond.createur)[0].adresse_mail,
            nom=list(fond.createur)[0].nom
        ) if len(list(fond.createur)) > 0 else None,
        id_caisse=list(fond.caisse)[0].__node__.identity if len(
            list(fond.caisse)) > 0 else None,
        titre=fond.titre,
        description=fond.description,
        montant=fond.montant
    )
    return fond
    ...


@router.post('/')
def post_fond(fond: FondData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    from datetime import datetime
    time = datetime.now()
    time_str = str(time)
    
    fond_node = nodes.Fond(titre=fond.titre,
                      description=fond.description, montant=fond.montant, date_creation=time_str)
    
    createur = nodes.User.match(driver, fond.email_createur).first()
    if not createur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        fond_node.createur.add(createur)
    caisse = nodes.Caisse.match(driver, fond.id_caisse).first()
    if caisse:
        fond_node.caisse.add(caisse)
    driver.push(fond_node)

    ...


@router.put('/{id}')
def modify_fond(id: int, fond: FondData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    fond_node = nodes.Fond.match(driver, id).first()
    if not fond_node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    fond_node.titre = fond.titre
    fond_node.description = fond.description
    fond_node.montant = fond.montant
    
    caisse = nodes.Caisse.match(driver, fond.id_caisse).first()
    if caisse:
        fond_node.caisse.clear()
        fond_node.caisse.add(caisse)

    driver.push(fond_node)
    ...


@router.delete('/{id}')    
def delete_fond(id: str, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    fond = nodes.Fond.match(driver, id).first()
    if not fond:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    driver.delete(fond)
    ...
