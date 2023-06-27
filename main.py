from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from globals import APP_NAME

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


from routers import action, activite, bien, caisse, depense, fond, notification, profile, section, contribution, authentication, image

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
app.include_router(image.router)
