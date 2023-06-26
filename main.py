from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from globals import APP_NAME
from functions import default_driver


app = FastAPI(
    title=APP_NAME,
    description=f"This is the backend service of the {APP_NAME} application")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)

add_pagination(app)


from routers import action, activite, bien, caisse, depense, fond, notification, profile, section, contribution, authentication

app.include_router(action.router)
app.include_router(activite.router)
app.include_router(authentication.router)
app.include_router(bien.router)
app.include_router(caisse.router)
app.include_router(contribution.router)
app.include_router(depense.router)
app.include_router(fond.router)
app.include_router(notification.router)
app.include_router(profile.router)
app.include_router(section.router)


default_driver.run("MERGE (u:User{matricule:'19M2222',nom:'melie',age:12,sexe:'m',specialite:'info',nationalite:'cmr',adresse_mail:'uriel.melie@gmail.com', phone_number:'454681351', mot_de_passe:'$2b$12$l56nprsVM0sfHZBI5v.aOO5JfJleSzJFyVUR9jRUXYoTO2PCdL1v2'})")