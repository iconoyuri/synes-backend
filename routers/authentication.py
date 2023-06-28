from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserLoginResponse
from oauth2 import create_access_token
from passlib.context import CryptContext
from py2neo_schemas import User
from functions import graph_driver, verify_email
from globals import DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD


router = APIRouter(
    prefix = "",
    tags = ["Authentication"]
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login(login_form: OAuth2PasswordRequestForm = Depends()):
    email = login_form.username.lower()
    verify_email(email)
    
    # print(email,login_form.password)
    user = find_user(email, login_form.password)
    if user:
        credentials = f"{email}\\\\{login_form.password}"
        access_token = create_access_token(
            data={"sub": credentials}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User doesn't exists or password is wrong"
        )

def find_user(identifier, password):
    driver = graph_driver({'email':DATABASE_DEFAULT_USERNAME,'password':DATABASE_DEFAULT_PASSWORD})
    
    user = User.match(driver,identifier).first()
    if not user: 
        return False

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    same_password = pwd_context.verify(password, user.mot_de_passe)
    if same_password:
        return user 
    else: 
        return None