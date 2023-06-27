from fastapi import APIRouter, UploadFile, Depends, HTTPException, status, Request
from schemas import User, UserData, Photo, TinySection
from typing import List
from fastapi_pagination import LimitOffsetPage, paginate
from oauth2 import get_current_user
import py2neo_schemas as nodes
from functions import graph_driver, encode_password, save_image, verify_email
from datetime import datetime
from mail.account_activation_handler import AccountActivationHandler

router = APIRouter(
    prefix='/user',tags=['User']
)


@router.get('/all', response_model=LimitOffsetPage[User])
def get_profiles(credentials = Depends(get_current_user)):
    results = nodes.User.match(graph_driver()).all()
    results = [User(
                id = user.__node__.identity,
                matricule=user.matricule, 
                nom= user.nom, 
                etablissement=str(list(user.etablissement)[0].nom), 
                age=user.age,
                section=TinySection(id=list(user.section)[0].__node__.identity, nom=list(user.section)[0].nom),
                sexe=user.sexe,
                specialite=user.specialite,
                nationalite=user.nationalite,
                adresse_mail=user.adresse_mail,
                phone_number=user.phone_number,
                photo=Photo(link=list(user.photo)[0].link if len(list(user.photo)) > 0 else None)
                ) for user in results]
    return paginate(results)


@router.get('/', response_model=User)
def get_own_profile(credentials = Depends(get_current_user)):
    user = nodes.User.match(graph_driver(),credentials['email']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = User(
                id = user.__node__.identity,
                matricule=user.matricule, 
                nom= user.nom, 
                etablissement=str(list(user.etablissement)[0].nom), 
                age=user.age,
                section=TinySection(id=list(user.section)[0].__node__.identity, nom=list(user.section)[0].nom),
                sexe=user.sexe,
                specialite=user.specialite,
                nationalite=user.nationalite,
                adresse_mail=user.adresse_mail,
                phone_number=user.phone_number,
                photo=Photo(link=list(user.photo)[0].link if len(list(user.photo)) > 0 else None)
                )
    return user

@router.get('/{id}', response_model=User)
def get_profile(id:str,credentials = Depends(get_current_user)):
    user = nodes.User.match(graph_driver(),id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = User(
                id = user.__node__.identity,
                matricule=user.matricule, 
                nom= user.nom, 
                etablissement=str(list(user.etablissement)[0].nom), 
                age=user.age,
                section=TinySection(id=list(user.section)[0].__node__.identity, nom=list(user.section)[0].nom),
                sexe=user.sexe,
                specialite=user.specialite,
                nationalite=user.nationalite,
                adresse_mail=user.adresse_mail,
                phone_number=user.phone_number,
                photo=Photo(link=list(user.photo)[0].link if len(list(user.photo)) > 0 else None)
                )
    return user


@router.post('/')
def post_profile(profile:UserData, credentials = Depends(get_current_user)):
    verify_email(profile.adresse_mail)

    driver = graph_driver()
    user = nodes.User.match(driver,profile.adresse_mail).first()
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists")
    
    time = datetime.now()
    time_str = str(time)
    timestamp = str(time.timestamp()).replace('.','')
    password = encode_password(timestamp)

    link = ""
    if profile.photo:
        link = save_image(profile.photo)

    query = ""
    params = None
    if profile.id_section != "": # if the user section was specified
        query = """
            MATCH (section:Section) WHERE ID(section) = $id_section

            MERGE (user:User{adresse_mail:$adresse_mail})
                ON CREATE
                    SET
                        user.matricule = $matricule,
                        user.nom = $nom,
                        user.age = $age,
                        user.sexe = $sexe,
                        user.specialite = $specialite,
                        user.nationalite = $nationalite,
                        user.phone_number = $phone_number,
                        user.mot_de_passe = $mot_de_passe,
                        user.date_creation = $now

            MERGE (etablissement:Etablissement{nom:$nom_etablissement})
                ON CREATE 
                    SET etablissement.date_creation = $now

            MERGE (user)-[:belong]->(etablissement)
            MERGE (etablissement)-[:belong]->(section)
            MERGE (user)-[:belong]->(section)

            MERGE (user)<-[:illustrate]-(photo:Photo)
                ON CREATE 
                    SET photo.date_creation = $now, photo.link = $link
        """
        params = {
            'id_section': profile.id_section,
            'adresse_mail':profile.adresse_mail,
            'matricule':profile.matricule,
            'nom':profile.nom,
            'age':profile.age,
            'sexe':profile.sexe,
            'specialite':profile.specialite,
            'nationalite':profile.nationalite,
            'phone_number':profile.phone_number,
            'mot_de_passe':password,
            'nom_etablissement':profile.etablissement,
            'now':time_str,
            'link':link
        }
    else: # otherwise
        query = """
            MERGE (user:User{adresse_mail:$adresse_mail})
                ON CREATE
                    SET
                        user.matricule = $matricule,
                        user.nom = $nom,
                        user.age = $age,
                        user.sexe = $sexe,
                        user.specialite = $specialite,
                        user.nationalite = $nationalite,
                        user.phone_number = $phone_number,
                        user.mot_de_passe = $mot_de_passe,
                        user.date_creation = $now

            MERGE (etablissement:Etablissement{nom:$nom_etablissement})
                ON CREATE 
                    SET etablissement.date_creation = $now

            MERGE (section:Section{nom:$nom_etablissement})
                ON CREATE 
                    SET section.date_creation = $now

            MERGE (user)-[:belong]->(etablissement)
            MERGE (etablissement)-[:belong]->(section)
            MERGE (user)-[:belong]->(section)

            MERGE (user)<-[:illustrate]-(photo:Photo)
                ON CREATE 
                    SET photo.date_creation = $now, photo.link = $link
        """
        params = {
            'adresse_mail':profile.adresse_mail,
            'matricule':profile.matricule,
            'nom':profile.nom,
            'age':profile.age,
            'sexe':profile.sexe,
            'specialite':profile.specialite,
            'nationalite':profile.nationalite,
            'phone_number':profile.phone_number,
            'mot_de_passe':password,
            'nom_etablissement':profile.etablissement,
            'now':time_str,
            'link':link
        }
    driver.run(query, params)

    AccountActivationHandler.send_credentials_mail(profile.nom, profile.adresse_mail, timestamp)
    ...


@router.post('/photo', response_model=Photo)
def post_profile_photo(photo:UploadFile, request:Request, credentials = Depends(get_current_user)):
    driver = graph_driver()
    user = nodes.User.match(driver,credentials['email']).first()
        
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists")
    
    image_name = save_image(photo)
    image_link = f"{request.url.scheme}://{request.url.netloc}/{image_name}"
    now = str(datetime.now())

    query = """
        MATCH (user:User{adresse_mail:$adresse_mail})
        MERGE (user)<-[:illustrate]-(photo:Photo)
        SET photo.date_creation = $now, photo.link = $link
    """
    params = {
        'adresse_mail':credentials['email'],
        'now':now,
        'link':image_link
    }
    driver.run(query, params)
    return Photo(link=image_link)


@router.put('/{id}')
def modify_profile(id:str, profile:UserData, credentials = Depends(get_current_user)):
    
    verify_email(profile.adresse_mail)

    driver = graph_driver()

    user = nodes.User.match(driver,id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    time = datetime.now()
    time_str = str(time)
    link = ""
    if profile.photo:
        link = save_image(profile.photo)

    query = ""
    params = None
    if profile.id_section != "": # if the user section was specified
        query = """
            MATCH (section:Section) WHERE ID(section) = $id_section

            MATCH (user:User{adresse_mail:$adresse_mail})
                SET
                    user.adresse_mail = $new_adresse_mail,
                    user.matricule = $matricule,
                    user.nom = $nom,
                    user.age = $age,
                    user.sexe = $sexe,
                    user.specialite = $specialite,
                    user.nationalite = $nationalite,
                    user.phone_number = $phone_number

            MATCH (:Section)<-[r2:belong]-(user)-[r1:belong]->(:Etablissement)
            DELETE r1,r2

            MERGE (etablissement:Etablissement{nom:$nom_etablissement})
                ON CREATE 
                    SET etablissement.date_creation = $now

            MERGE (user)-[:belong]->(etablissement)
            MERGE (etablissement)-[:belong]->(section)
            MERGE (user)-[:belong]->(section)
        """ + ("""
            MATCH (user)<-[:illustrate]-(photo:Photo)
                SET photo.link = $link
        """ if link else "")

        params = {
            'id_section': profile.id_section,
            'adresse_mail':credentials['email'],
            'new_adresse_mail':profile.adresse_mail,
            'matricule':profile.matricule,
            'nom':profile.nom,
            'age':profile.age,
            'sexe':profile.sexe,
            'specialite':profile.specialite,
            'nationalite':profile.nationalite,
            'phone_number':profile.phone_number,
            'nom_etablissement':profile.etablissement,
            'now':time_str,
            'link':link
        }
    else: # if the user section was not specified
        query = """
            MATCH (:Section)<-[r2:belong]-(user:User{adresse_mail:$adresse_mail})-[r1:belong]->(:Etablissement)
            DELETE r1,r2
            SET
                user.adresse_mail = $new_adresse_mail,
                user.matricule = $matricule,
                user.nom = $nom,
                user.age = $age,
                user.sexe = $sexe,
                user.specialite = $specialite,
                user.nationalite = $nationalite,
                user.phone_number = $phone_number
            

            MERGE (etablissement:Etablissement{nom:$nom_etablissement})
                ON CREATE 
                    SET etablissement.date_creation = $now

            MERGE (section:Section{nom:$nom_etablissement})
                ON CREATE 
                    SET section.date_creation = $now

            CREATE (user)-[:belong]->(etablissement)
            CREATE (user)-[:belong]->(section)
            MERGE (etablissement)-[:belong]->(section)
        """ + ("""
            MATCH (user)<-[:illustrate]-(photo:Photo)
                SET photo.link = $link
        """ if link else "")
        params = {
            'adresse_mail':credentials['email'],
            'new_adresse_mail':profile.adresse_mail,
            'matricule':profile.matricule,
            'nom':profile.nom,
            'age':profile.age,
            'sexe':profile.sexe,
            'specialite':profile.specialite,
            'nationalite':profile.nationalite,
            'phone_number':profile.phone_number,
            'nom_etablissement':profile.etablissement,
            'now':time_str,
            'link':link
        }
    driver.run(query, params)


@router.delete('/{id}')
def delete_profile(id:str, credentials = Depends(get_current_user)):
    driver = graph_driver()
    user = nodes.User.match(driver,id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    driver.delete(user)


@router.post('/section/{id_user}/{id_section}')
def affect_to_section(id_user:str,id_section:int, credentials = Depends(get_current_user)):
    driver = graph_driver()
    query = """
            MATCH (section:Section) WHERE ID(section) = $id_section
            MATCH (user:User{adresse_mail:$adresse_mail})-[b:belong]->(s:Section)
            DELETE b
            CREATE (user)-[:belong]->(section)
        """
    params = {
        'id_section':id_section,
        'adresse_mail':id_user,
    }
    driver.run(query,params)

@router.post('/password/{previous_pwd}/{new_pwd}')
def change_password(previous_pwd:str,new_pwd:str, credentials = Depends(get_current_user)):
    from routers.authentication import find_user
    driver = graph_driver()
    user = find_user(credentials['email'], previous_pwd)
    
    if not user:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User doesn't exists or password is wrong"
        )
    
    user.mot_de_passe = encode_password(new_pwd)
    driver.push(user)

