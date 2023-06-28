from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Section, SectionData
from oauth2 import get_current_user
import py2neo_schemas as nodes
from fastapi_pagination import LimitOffsetPage, paginate
from functions import graph_driver
from datetime import datetime

router = APIRouter(
    prefix='/section',tags=['Section']
)


@router.get('/all', response_model=LimitOffsetPage[Section])
def get_sections(credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    sections = nodes.Section.match(driver).all()
    sections = [Section(
        id=section.__node__.identity,
        date_creation=section.date_creation,
        nom=section.nom, 
        etablissement=list(section.etablissement)[0].nom if len(list(section.etablissement)) > 0 else "")
        for section in sections]
    return paginate(sections)


@router.get('/{id}', response_model=Section)
def get_section(id:int, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)

    section = nodes.Section.match(driver, id).first()

    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    print(section.nom, list(section.etablissement), list(section.biens))
    section = Section(
        id=section.__node__.identity,
        date_creation=section.date_creation,
        nom=section.nom, 
        etablissement=list(section.etablissement)[0].nom if len(list(section.etablissement)) > 0 else "")
    print(section)
    return section
 


@router.post('/')
def post_section(section:SectionData, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    time = datetime.now()
    time_str = str(time)
    query = """
        MERGE (etablissement:Etablissement{nom:$nom_etablissement})
            ON CREATE 
                SET etablissement.date_creation = $now

        MERGE (section:Section{nom:$nom_section})
            ON CREATE 
                SET section.date_creation = $now

        MERGE (etablissement)-[:related_school]->(section)
    """
    params = {
        'nom_etablissement':section.etablissement,
        'nom_section':section.etablissement,
        'now':time_str
    }
    driver.run(query, params)


@router.put('/{id}')
def modify_section(id:int, section:SectionData, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    _section = nodes.Section.match(driver, id).first()

    if not _section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    time = datetime.now()
    time_str = str(time)
    query = """
        MATCH (section:Section)<-[r:related_school]-(:Etablissement) WHERE ID(section) = $id_section
        SET section.nom = $nom
        DELETE r

        MERGE (etablissement:Etablissement{nom:$nom_etablissement})
            ON CREATE 
                SET etablissement.date_creation = $now

        CREATE (etablissement)-[:related_school]->(section)
    """
    params = {
        'id_section':id,
        'now':time_str,
        'nom_etablissement':section.etablissement,
        'nom':section.nom
    }
    driver.run(query, params)


@router.delete('/{id}')
def delete_section(id:int, credentials = Depends(get_current_user)):
    driver = graph_driver(credentials)
    section = nodes.Section.match(driver, id).first()

    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    driver.delete(section)
    ...
