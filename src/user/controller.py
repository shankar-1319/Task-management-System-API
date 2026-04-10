from fastapi import HTTPException,status,Request
from src.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel 
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime ,timedelta
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

#object of PasswordHash
hash_password = PasswordHash.recommended()

#hash password maker
def password_to_hashedpassword(password): 
    return hash_password.hash(password)

#hash_password and plane password verifier
def verify_password(planepassword,hashpassword):
    return hash_password.verify(planepassword,hashpassword)


def register_user(body:UserSchema,db:Session):
    #print(body)
    is_user = db.query(UserModel).filter(UserModel.username==body.Username).first()
    if is_user:
        raise HTTPException(status_code=400,detail="Username already exists..")
    
    is_user = db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user:
        raise HTTPException(status_code=400,detail="email already exists..")
    
    hashpassword = password_to_hashedpassword(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.Username,
        hashed_password=hashpassword,
        email = body.email,
        phone = body.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# login user
def login_user(body:LoginSchema,db:Session):
    user = db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid user name")
    
    if not verify_password(body.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password try again")
    
    #exp time 
    exp_time = datetime.now() + timedelta(minutes=settings.SESSON_TIME)
    #print(f"current date time = {datetime.now()} \n exp_ time = {exp_time}")
    #generate token 
    token = jwt.encode({"_id": user.id,"_username":user.username,"exp":exp_time.timestamp()},settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return {"Token": token}

# authentication function to verify token and return user details
def is_authenticated(request:Request,db:Session):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorized missing token")
        
        token = token.split(" ")[-1]
        data = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        _id = data.get("_id")
        exp_time = data.get("exp")
        current_time = datetime.now().timestamp()
        #sesson time validation
        if current_time > exp_time :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized by time out")
        
        user = db.query(UserModel).filter(UserModel.id==_id).first()
        #user id validation
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized by id")

        # print(data)
        # print(exp_time-current_time)
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired ")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized ")
    