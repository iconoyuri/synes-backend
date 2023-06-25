from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime



class TinyEntity(BaseModel):
    id:str
    nom:str

class TinyUser(TinyEntity):
    ...

class TinySection(TinyEntity):
    ...

class TinyActivite(TinyEntity):
    ...

class TinyFond(TinyEntity):
    ...

class TinyCaisse(TinyEntity):
    ...

class TinyDepense(TinyEntity):
    ...

class TinyBien(TinyEntity):
    ...



class Photo(BaseModel):
    image_link:str

class User(BaseModel):
    id:str
    matricule:str
    nom:str 
    etablissement:str
    age:int 
    section:TinySection
    sexe:str
    specialite:str
    nationalite:str 
    adresse_mail:EmailStr
    phone_number:str
    photo:Photo

class UserData(BaseModel):
    matricule:str
    nom:str 
    etablissement:str
    id_section:str
    age:int 
    sexe:str
    specialite:str
    nationalite:str 
    adresse_mail:EmailStr
    phone_number:str
    photo:Photo

class Section(BaseModel):
    id:str
    nom:str
    etablissement:str

class SectionData(BaseModel):
    nom:str
    etablissement:str

class Activite(BaseModel):
    id:str 
    createur:TinyUser
    titre:str
    lieu:str
    moderateurs:List[TinyUser]
    membre_convies:List[TinyUser]
    date_debut:datetime
    date_fin:datetime

class ActiviteData(BaseModel):
    id_createur:str
    titre:str
    lieu:str
    moderateurs:Optional[List[TinyUser]]
    membre_convies:List[TinyUser]
    date_debut:datetime
    date_fin:datetime

class Fond(BaseModel):
    id:str
    createur:TinyUser
    id_caisse:Optional[str]
    titre:str
    description:str
    montant:float

class FondData(BaseModel):
    id_createur:str
    id_caisse:Optional[str]
    titre:str
    description:str
    montant:float

class Caisse(BaseModel):
    id:str
    createur:TinyUser
    nom:str
    description:str
    montant_courant:float

class CaisseData(BaseModel):
    id_createur:str
    nom:str
    description:str
    montant_courant:float

class Depense(BaseModel):
    id:str
    createur:TinyUser
    id_caisse:Optional[str]
    titre:str
    description:str
    montant:float

class DepenseData(BaseModel):
    id_createur:str
    id_caisse:Optional[str]
    titre:str
    description:str
    montant:float

class Bien(BaseModel):
    id:str
    section:TinySection
    nom:str
    photos:List[Photo]
    description:str 
    valeur_marchande:Optional[str]

class BienData(BaseModel):
    section:TinySection
    nom:str
    photos:List[Photo]
    description:str 
    valeur_marchande:Optional[str]

class Sujet(BaseModel):
    id:str
    type:str

class Objet(BaseModel):
    id:str
    type:str

class Action(BaseModel):
    sujet:Sujet
    type:str
    objet:Objet
    date:datetime

class Notification(BaseModel):
    id:str
    contenu:str 
    entity:TinyEntity
    type:str


class Contribution(BaseModel):
    id:str
    id_fond:str 
    id_user:str
    montant:float

class ContributionData(BaseModel):
    id_fond:str 
    id_user:str
    montant:float


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
