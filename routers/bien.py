from fastapi import APIRouter, UploadFile, Depends, Request
from schemas import Bien, BienData, TinySection, Photo
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate
from functions import graph_driver, save_image
import py2neo_schemas as nodes
from oauth2 import get_current_user
from datetime import datetime
from functools import reduce

router = APIRouter(
    prefix='/bien',tags=['Bien']
)


@router.get('/all', response_model=LimitOffsetPage[Bien])
def get_biens(credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    biens = nodes.Bien.match(driver).all()
    biens = [Bien(
            id=bien.__node__.identity,
            date_creation=bien.date_creation,
            nom=bien.nom,
            section= TinySection(
                    id= list(bien.section)[0].__node__.identity, 
                    nom = list(bien.section)[0].nom
                    ) if len(list(bien.section)) > 0 else None,
            photos= list(bien.photos),
            description= bien.description ,
            valeur_marchande = bien.valeur 
            )
            for bien in biens]

    return paginate(biens)


@router.get('/{id}', response_model=Bien)
def get_bien(id:str, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    bien = nodes.Bien.match(driver,id).first()
    bien = Bien(
            id=bien.__node__.identity,
            date_creation=bien.date_creation,
            nom=bien.nom,
            section= TinySection(
                    id= list(bien.section)[0].__node__.identity, 
                    nom = list(bien.section)[0].nom
                    ) if len(list(bien.section)) > 0 else None,
            photos= list(bien.photos),
            description= bien.description,
            valeur_marchande = bien.valeur 
            )
    return bien


@router.post('/')
def post_bien(bien:BienData, request:Request, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    time = datetime.now()
    time_str = str(time)

    photos_query = reduce(
        lambda acc,val: f"{acc} {val}",
        ["MERGE (:Photo{link:'" + f"{request.url.scheme}://{request.url.netloc}/{save_image(photo)}" + "',date_creation:'" + time_str + "'})-[:illustrate]->(bien)" for photo in bien.photos]
        )  if bien.photos else ""
    data_query = """
        MATCH (user:User{adresse_mail:$adresse_mail})
        MERGE (user)<-[:create_good]-(bien:Bien{nom:$nom,description:$description,valeur:$valeur,date_creation:$now})
    """
    section_query = """
        MATCH (section:Section) WHERE ID(section) = $id_section
        MERGE (bien)-[:belong_section]->(section)
    """ if bien.section else ""
    
    query = data_query + section_query + photos_query
    params = {
        'adresse_mail':credentials['email'],
        'id_section':bien.section.id if bien.section else "",
        'nom':bien.nom,
        'description':bien.description,
        'valeur':bien.valeur_marchande,
        'now':time_str
    }
    driver.run(query, params)
    ...


@router.put('/{id}')
def modify_bien(id:int, bien:BienData, request:Request, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    time = datetime.now()
    time_str = str(time)
    data_query = """
        MATCH (bien:Bien) WHERE ID(bien) = $id_bien
        SET
            bien.nom = $nom,
            bien.description = $description,
            bien.valeur = $valeur

    """
    section_query = """
        WITH bien
        MATCH (bien)-[b:belong_section]->(s:Section)
        MATCH (section:Section{nom:$nom_section})
        DELETE b
        CREATE (bien)-[:belong_section]->(section)
    """ if bien.section else ""
    
    photos_query = ""
    if bien.photos :
        photos_queries = ["MERGE (:Photo{link:'" + f"{request.url.scheme}://{request.url.netloc}/{save_image(photo)}" + "',date_creation:'" + time_str + "'})-[:illustrate]->(bien)" for photo in bien.photos]
        photos_query = """
            WITH bien
            OPTIONAL MATCH (bien)<-[i:illustrate]-(p:Photo)
            DELETE i
        """ + str(reduce(lambda acc,val: f"{acc} {val}",photos_queries))
    

    query = data_query + section_query + photos_query 
    params = {
        'id_bien':id,
        'nom_section':bien.section.nom if bien.section else "",
        'nom':bien.nom,
        'description':bien.description,
        'valeur':bien.valeur_marchande
    }
    driver.run(query, params)


@router.delete('/{id}')
def delete_bien(id:int, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    query = """
        MATCH (bien:Bien) WHERE ID(bien) = $id_bien
        MATCH (bien)<-[:illustrate]-(photo:Photo)
        DETACH DELETE bien, photo
    """
    params = {
        'id_bien':id
    }
    driver.run(query, params)


@router.post('/photos/{id}')
def upload_bien_photos(id:int, photos:List[UploadFile], request:Request, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    time = datetime.now()
    time_str = str(time)

    photos_query = reduce(
            lambda acc,val: f"{acc} {val}",
            ["MERGE (:Photo{link:'" + f"{request.url.scheme}://{request.url.netloc}/{save_image(photo)}" + "',date_creation:'" + time_str + "'})-[:illustrate]->(bien)" for photo in photos]
        )
    query = """
        MATCH (bien:Bien) WHERE ID(bien) = $id_bien
    """ + photos_query

    params = {
        'id_bien':id
    }
    driver.run(query, params)
