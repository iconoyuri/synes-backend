from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Depense, DepenseData, TinyUser
from fastapi_pagination import LimitOffsetPage, paginate
import py2neo_schemas as nodes
from functions import graph_driver
from oauth2 import get_current_user
router = APIRouter(
    prefix='/depense',tags=['Depense']
)



@router.get('/all', response_model=LimitOffsetPage[Depense])
def get_depense(credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    depenses = nodes.Depense.match(driver).all()
    depenses = [Depense(
        id=depense.__node__.identity,
        date_creation=depense.date_creation,
        createur=TinyUser(
            email=list(depense.createur)[0].adresse_mail,
            nom=list(depense.createur)[0].nom
        ) if len(list(depense.createur)) > 0 else None,
        id_caisse=list(depense.caisse)[0].__node__.identity if len(
            list(depense.caisse)) > 0 else None,
        titre=depense.titre,
        description=depense.description,
        montant=depense.montant
    )
        for depense in depenses]

    return paginate(depenses)
    ...


@router.get('/{id}', response_model=Depense)
def get_depense(id: int, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    depense = nodes.Depense.match(driver, id).first()
    if not depense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    depense = Depense(
        id=depense.__node__.identity,
        date_creation=depense.date_creation,
        createur=TinyUser(
            email=list(depense.createur)[0].adresse_mail,
            nom=list(depense.createur)[0].nom
        ) if len(list(depense.createur)) > 0 else None,
        id_caisse=list(depense.caisse)[0].__node__.identity if len(
            list(depense.caisse)) > 0 else None,
        titre=depense.titre,
        description=depense.description,
        montant=depense.montant
    )
    return depense
    ...


@router.post('/')
def post_depense(depense: DepenseData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    depense_node = nodes.Depense(titre=depense.titre,
                      description=depense.description, montant=depense.montant)
    
    createur = nodes.User.match(driver, depense.email_createur).first()
    if not createur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" Utilisateur non existant")
    else:
        depense_node.createur.add(createur)

    caisse = nodes.Caisse.match(driver, depense.id_caisse).first()
    if not caisse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="caisse non existante")
    if caisse.montant_courant >= depense.montant:
        caisse.montant_courant = caisse.montant_courant - depense.montant
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Le montant de la dépense est plus grand que celui de la caisse")

    depense_node.caisse.add(caisse)
    driver.push(depense_node)
    driver.push(caisse)



@router.put('/{id}')
def modify_depense(id:int, depense:DepenseData):
    ...


@router.delete('/{id}')
def delete_depense(id:int):
    ...
