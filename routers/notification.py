from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Notification, TinyEntity
from fastapi_pagination import LimitOffsetPage, paginate
import py2neo_schemas as nodes
from functions import graph_driver
from oauth2 import get_current_user

router = APIRouter(
    prefix='/notification', tags=['Notification']
)


@router.get('/all', response_model=LimitOffsetPage[Notification])
def get_notifications(credentials=Depends(get_current_user)):
    driver = graph_driver(credentials)
    user = nodes.User.match(driver, credentials['email']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    notifications = [Notification(id=notification.__node__.identity, date_creation=notification.date_creation,
                                  sujet=notification.lien_associe, contenu=notification.contenu, lien_associe=notification.lien_associe) for notification in list(user.notifications)]

    return paginate(notifications)
    ...
