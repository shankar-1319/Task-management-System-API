from fastapi import Request,HTTPException,status,Depends
import jwt
from src.utils.settings import settings
from src.user.models import UserModel
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
from src.utils.db import get_db

def is_authenticated(request:Request,db:Session=Depends(get_db)):
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