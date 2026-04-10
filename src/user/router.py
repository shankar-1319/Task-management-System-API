from fastapi import APIRouter,Depends,status,Request
from src.user.dtos import UserSchema,UserResponseSchema,LoginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller



user_routes = APIRouter(prefix="/user")

#create user route
@user_routes.post("/create_user",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def create_user(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register_user(body,db)

#user login route
@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login_user(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

@user_routes.get("/is_auth",response_model=UserResponseSchema,status_code=status.HTTP_200_OK)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db)