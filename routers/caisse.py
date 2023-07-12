from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Caisse, CaisseData, TinyUser
from fastapi_pagination import LimitOffsetPage, paginate
import py2neo_schemas as nodes
from functions import graph_driver
from oauth2 import get_current_user

router = APIRouter(
    prefix='/caisse', tags=['Caisse']
)


@router.get('/all', response_model=LimitOffsetPage[Caisse])
def get_caisses(credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    caisses = nodes.Caisse.match(driver).all()
    caisses = [Caisse(
        id=caisse.__node__.identity,
        date_creation=caisse.date_creation,
        createur=TinyUser(
            email=list(caisse.createur)[0].adresse_mail,
            nom=list(caisse.createur)[0].nom
        ) if len(list(caisse.createur)) > 0 else None,
        nom=caisse.nom,
        description=caisse.description,
        montant_courant=caisse.montant_courant
    )
        for caisse in caisses]

    return paginate(caisses)
    ...


@router.get('/{id}', response_model=Caisse)
def get_caisse(id: int, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    caisse = nodes.Caisse.match(driver, id).first()
    caisse = Caisse(
        id=caisse.__node__.identity,
        date_creation=caisse.date_creation,
        createur=TinyUser(
            email=list(caisse.createur)[0].adresse_mail,
            nom=list(caisse.createur)[0].nom
        ) if len(list(caisse.createur)) > 0 else None,
        nom=caisse.nom,
        description=caisse.description,
        montant_courant=caisse.montant_courant
    )
    return caisse
    ...


@router.post('/')
def post_caisse(caisse: CaisseData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)

    from datetime import datetime
    time = datetime.now()
    time_str = str(time)

    caisse_node = nodes.Caisse(nom=caisse.nom,
                               description=caisse.description, montant_courant=caisse.montant_courant, date_creation=time_str)

    createur = nodes.User.match(driver, caisse.email_createur or credentials['email']).first()
    if not createur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    else:
        caisse_node.createur.add(createur)
    driver.push(caisse_node)

    query = """
        MATCH (user:User)
        MERGE (n:Notification{sujet:$sujet, contenu:$contenu, type:$type, lien_associe:$lien_associe, date_creation:$date_creation})
        MERGE (n)-[r:notify]->(user)
    """
    params = {
        'sujet': f'Création Caisse',
        'contenu': f'{createur.nom} vient de créer une nouvelle caisse',
        'type': 'Simple',
        'lien_associe': '',
        'date_creation': time_str
    }
    driver.run(query, params)
    ...


@router.put('/{id}')
def modify_caisse(id: int, caisse: CaisseData, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    caisse_node = nodes.Caisse.match(driver, id).first()
    if not caisse_node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    nom_caisse = caisse_node.nom
    caisse_node.nom = caisse.nom
    caisse_node.description = caisse.description
    driver.push(caisse_node)
    
    query = """
        MATCH (user:User)
        MERGE (n:Notification{sujet:$sujet, contenu:$contenu, type:$type, lien_associe:$lien_associe, date_creation:$date_creation})
        MERGE (n)-[r:notify]->(user)
    """
    from datetime import datetime
    time = datetime.now()
    time_str = str(time)
    params = {
        'sujet': f'Modification Caisse',
        'contenu': f'La caisse {nom_caisse} vient d\'ètre modifiée par {credentials["email"]}',
        'type': 'Simple',
        'lien_associe': '',
        'date_creation': time_str
    }
    driver.run(query, params)
    ...


@router.delete('/{id}')
def delete_caisse(id: int, credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    caisse = nodes.Caisse.match(driver, id).first()
    if not caisse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    driver.delete(caisse)
    
    query = """
        MATCH (user:User)
        MERGE (n:Notification{sujet:$sujet, contenu:$contenu, type:$type, lien_associe:$lien_associe, date_creation:$date_creation})
        MERGE (n)-[r:notify]->(user)
    """

    from datetime import datetime
    time = datetime.now()
    time_str = str(time)
    params = {
        'sujet': f'Suppression Caisse',
        'contenu': f'La caisse {caisse.nom} vient d\'ètre supprimée par {credentials["email"]}',
        'type': 'Simple',
        'lien_associe': '',
        'date_creation': time_str
    }
    driver.run(query, params)
    ...
