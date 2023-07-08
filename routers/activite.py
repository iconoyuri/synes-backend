from fastapi import APIRouter, UploadFile, Depends, HTTPException, status, Request
from schemas import Activite, ActiviteData, Photo, TinyUser
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate
from oauth2 import get_current_user
from functions import graph_driver, save_image
import py2neo_schemas as nodes
from datetime import datetime
from functools import reduce

router = APIRouter(
    prefix='/activite',tags=['Activite']
)


@router.get('/all', response_model=LimitOffsetPage[Activite])
def get_activites(credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    activites = nodes.Activite.match(driver).all()
    activites = [Activite(
                    id=activite.__node__.identity,
                    date_creation=activite.date_creation,
                    titre = activite.titre,
                    lieu = activite.lieu,
                    date_debut = activite.date_debut,
                    date_fin = activite.date_fin,
                    createur= TinyUser(email=list(activite.createur)[0].adresse_mail,nom=list(activite.createur)[0].nom) if len(list(activite.createur)) > 0 else None,
                    membre_convies = [TinyUser(email=invite.adresse_mail,nom=invite.nom) for invite in list(activite.invites)],
                    moderateurs = [TinyUser(email=moderateur.adresse_mail,nom=moderateur.nom) for moderateur in list(activite.moderateurs)],
                    photos = [Photo(link=photo.link) for photo in list(activite.photos)],
                ) for activite in activites]

    return paginate(activites)


@router.get('/{id}', response_model=Activite)
def get_activite(id:int,credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    activite = nodes.Activite.match(driver,id).first()
    if not activite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Activite(
                    id=activite.__node__.identity,
                    date_creation=activite.date_creation,
                    titre = activite.titre,
                    lieu = activite.lieu,
                    date_debut = activite.date_debut,
                    date_fin = activite.date_fin,
                    createur= TinyUser(email=list(activite.createur)[0].adresse_mail,nom=list(activite.createur)[0].nom) if len(list(activite.createur)) > 0 else None,
                    membre_convies = [TinyUser(email=invite.adresse_mail,nom=invite.nom) for invite in list(activite.invites)],
                    moderateurs = [TinyUser(email=moderateur.adresse_mail,nom=moderateur.nom) for moderateur in list(activite.moderateurs)],
                    photos = [Photo(link=photo.link) for photo in list(activite.photos)],
                )


@router.post('/')
def post_activite(activite:ActiviteData, request:Request, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    time = datetime.now()
    time_str = str(time)

    photos_query = reduce(
        lambda acc,val: f"{acc} {val}",
        ["MERGE (:Photo{link:'" + f"{request.url.scheme}://{request.url.netloc}/{save_image(photo)}" + "',date_creation:'" + time_str + "'})-[:is_snapshot]->(activite)" for photo in activite.photos]
        )  if activite.photos else ""
    
    invites_query = ""
    if activite.membre_convies:
        # invites_query = "WITH activite "
        i = 0
        for membre in activite.membre_convies:
            sub_query = " WITH activite "
            sub_query += "MATCH (i"+str(i)+":User{adresse_mail:'"+membre.email+"'}) "
            sub_query += "MERGE (i"+str(i)+")<-[:invited]-(activite) "
            invites_query += sub_query
            i+=1

    moderateurs_query = ""
    if activite.moderateurs:
        moderateurs_query = "WITH activite "
        i = 0
        for membre in activite.moderateurs:
            sub_query = " WITH activite  "
            sub_query += "MATCH (u"+str(i)+":User{adresse_mail:'"+membre.email+"'}) "
            sub_query += "MERGE (u"+str(i)+")-[:moderate]->(activite) "
            moderateurs_query += sub_query
            i+=1
            
    data_query = """
        MATCH (user:User{adresse_mail:$adresse_mail})
        MERGE (activite:Activite{titre:$titre,lieu:$lieu,date_debut:$date_debut,date_fin:$date_fin, date_creation:$now})<-[:create_activity]-(user)
    """
    query = data_query + invites_query + moderateurs_query + photos_query
    params = {
        'titre': activite.titre,
        'lieu':activite.lieu,
        'date_debut':str(activite.date_debut),
        'date_fin':str(activite.date_fin),
        'adresse_mail':credentials['email'],
        'now':time_str
    }
    driver.run(query, params)


@router.put('/{id}')
def modify_activite(id:int, activite:ActiviteData,request: Request, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    _activite = nodes.Activite.match(driver, id).first()
    if not _activite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    time = datetime.now()
    time_str = str(time)

    photos_query = "\n WITH activite MATCH (activite)<-[i_s:is_snapshot]-(p:Photo) DELETE i_s, p "
    # photos_query = ""
    photos_query += reduce(
        lambda acc,val: f"{acc} {val}",
        ["CREATE (:Photo{link:'" + f"{request.url.scheme}://{request.url.netloc}/{save_image(photo)}" + "',date_creation:'" + time_str + "'}) CREATE (photo)-[:is_snapshot]->(activite)" for photo in activite.photos]
        )  if activite.photos else ""
    
    invites_query = "\n WITH activite MATCH (:User)<-[i:invited]-(activite) DELETE i "
    # invites_query = ""
    if activite.membre_convies:
        # invites_query = "WITH activite "
        i = 0
        for membre in activite.membre_convies:
            # print('test')
            sub_query = " WITH activite "
            sub_query = ""
            sub_query += " CREATE (:User{adresse_mail:'"+membre.email+"'})<-[:invited]-(activite) "
            # sub_query += " MATCH (i"+str(i)+":User{adresse_mail:'"+membre.email+"'}) "
            # sub_query += " CREATE (i"+str(i)+")<-[:invited]-(activite) "
            invites_query += sub_query
            i+=1

    moderateurs_query = "\n WITH activite MATCH (:User)-[m:moderate]->(activite) DELETE m "
    # moderateurs_query = ""
    # if activite.moderateurs:
    #     # moderateurs_query = "WITH activite "
    #     # print('test')
    #     i = 0
    #     for membre in activite.moderateurs:
    #         sub_query = " WITH activite  "
    #         sub_query += "MATCH (u"+str(i)+":User{adresse_mail:'"+membre.email+"'}) "
    #         sub_query += "CREATE (u"+str(i)+")-[:moderate]->(activite) "
    #         moderateurs_query += sub_query
    #         i+=1
    # print(moderateurs_query)       
    data_query = """
        MATCH (activite:Activite) WHERE ID(activite) = $id_activite
        SET
            activite.titre = $titre,
            activite.lieu = $lieu,
            activite.date_debut = $date_debut,
            activite.date_fin = $date_fin

    """
    query = data_query + invites_query + moderateurs_query + photos_query
    # print(query)
    params = {
        'id_activite': id,
        'titre': activite.titre,
        'lieu':activite.lieu,
        'date_debut':str(activite.date_debut),
        'date_fin':str(activite.date_fin)
    }
    driver.run(query, params)
    ...


@router.delete('/{id}')
def delete_activite(id:int,credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    activite = nodes.Activite.match(driver,id).first()
    if not activite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    driver.delete(activite)


@router.post('/photos/{id}')
def upload_activity_photos(id:int,photos:List[UploadFile],credentials = Depends(get_current_user)):
    # return id
    ...

