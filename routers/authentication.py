from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserLoginResponse
from token_handler import create_access_token


router = APIRouter(
    prefix = "",
    tags = ["Authentication"]
)


# @router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
# def login(login_form: OAuth2PasswordRequestForm = Depends()):
#     ...

    

# @router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
@router.post("/login", status_code=status.HTTP_200_OK)
def login(login_form: OAuth2PasswordRequestForm = Depends()): 
    username = login_form.username.lower()
    return None
    
    user = find_user(username, login_form.password)
    if user:
        if user.activated: 
            access_token = create_access_token(
                data={"sub": user.login}
            )
            user_type = None
            if user.member:
                user_type = "member"
            elif user.admin:
                user_type = "admin"
            else:
                user_type = "user"

            return {"access_token": access_token, "token_type": "bearer", "user_type": user_type}
        else: 
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="This user account isn't yet activated. Look for the activation link in your mail box"
            )
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The user doesn't exists"
        )



# def find_user(login, password):
#     user = User.match(main_graph).where(f"_.email = '{login}' OR _.login = '{login}'").first()
#     if not user: 
#         return False    

#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     same_password = pwd_context.verify(password, user.password)
#     if same_password:
#         return user 
#     else: 
#         return None