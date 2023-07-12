from fastapi import UploadFile
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class Entity(BaseModel):
    id: Optional[str]
    date_creation: Optional[datetime]

    class Config:
        orm_mode = True


class TinyEntity(BaseModel):
    id: int
    nom: str

    class Config:
        orm_mode = True


class TinyUser(BaseModel):

    email: str
    nom: str

    class Config:
        orm_mode = True
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
    link: Optional[str]

    class Config:
        orm_mode = True


class User(BaseModel):
    matricule: str
    nom: str
    etablissement: Optional[str]
    age: int
    section: Optional[TinySection]
    sexe: str
    specialite: str
    nationalite: str
    adresse_mail: EmailStr
    phone_number: str
    photo: Optional[Photo]
    date_creation: Optional[datetime]


class UserTest(BaseModel):

    matricule: str
    nom: str
    adresse_mail: EmailStr

    class Config:
        orm_mode = True


class UserData(BaseModel):

    matricule: str
    nom: str
    etablissement: str
    adresse_mail: EmailStr

    id_section: Optional[int]
    age: Optional[int] = 0
    sexe: Optional[str] = ""
    specialite: Optional[str] = ""
    nationalite: Optional[str] = ""
    phone_number: Optional[str] = ""
    photo: Optional[UploadFile]

    class Config:
        orm_mode = True


class Section(Entity):
    nom: str
    etablissement: str


class SectionData(BaseModel):
    nom: str
    etablissement: str


class Activite(Entity):
    titre: str
    lieu: str
    date_debut: datetime
    date_fin: datetime
    membre_convies: List[TinyUser]
    createur: Optional[TinyUser]
    photos: Optional[List[Photo]]
    moderateurs: Optional[List[TinyUser]]


class ActiviteData(BaseModel):

    titre: str
    lieu: str
    date_fin: datetime
    date_debut: datetime
    membre_convies: List[TinyUser]
    moderateurs: Optional[List[TinyUser]]
    photos: Optional[List[Photo]]


class Fond(Entity):
    createur: TinyUser
    id_caisse: Optional[int]
    titre: str
    description: str
    montant: float


class FondData(BaseModel):
    email_createur: str
    id_caisse: int
    # id_caisse:Optional[int]
    titre: str
    description: str
    montant: float


class Caisse(Entity):
    createur: TinyUser
    nom: str
    description: str
    montant_courant: float


class CaisseData(BaseModel):
    email_createur: str
    nom: str
    description: str
    montant_courant: Optional[float] = 0


class Depense(Entity):
    createur: TinyUser
    id_caisse: int
    # id_caisse:Optional[int]
    titre: str
    description: str
    montant: float


class DepenseData(BaseModel):
    email_createur: str
    id_caisse: int
    # id_caisse:Optional[int]
    titre: str
    description: str
    montant: float


class Bien(Entity):
    section: Optional[TinySection]
    nom: str
    photos: List[Photo]
    description: str
    valeur_marchande: Optional[str]


class BienData(BaseModel):
    nom: str
    description: str
    valeur_marchande: Optional[str]
    section: Optional[TinySection]
    photos: Optional[List[UploadFile]]


class Sujet(BaseModel):
    id: str
    type: str


class Objet(BaseModel):
    id: str
    type: str


class Action(BaseModel):
    sujet: Sujet
    type: str
    objet: Objet
    date: datetime


class Notification(Entity):
    contenu: str
    sujet: str
    lien_associe: Optional[str] = '#'
    # entity:Optional[TinyEntity]
    type: Optional[str] = ''


class Contribution(BaseModel):
    id_fond: int
    date_creation: Optional[datetime]
    email_user: str
    montant: float


class ContributionData(BaseModel):
    id_fond: int
    email_user: Optional[str]
    montant: float


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
