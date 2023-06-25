from fastapi import status, Depends, APIRouter, Query
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserLoginResponse


router = APIRouter(
    prefix = "",
    tags = ["Authentication"]
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login(login_form: OAuth2PasswordRequestForm = Depends()):
    ...