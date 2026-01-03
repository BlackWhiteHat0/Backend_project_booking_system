from fastapi import FastAPI , Depends , HTTPException
from typing import Dict
from sqlalchemy.orm import Session
import models ,schemas ,crud
from database import SessionLocal , engine
from typing import List

from fastapi.security import OAuth2PasswordBearer ,OAuth2PasswordRequestForm
from datetime import timedelta
import utils

from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils import SECRET_KET, ALGORITHM



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=401,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KET, algorithms=[ALGORITHM])

        email:str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user



@app.post("/token")
def login_for_access_token(from_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=from_data.username)

    if not user or not utils.verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate":"Bearer"})
    
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(data={"sub":user.email},
                                             expires_delta=access_token_expires)
    
    return {"access_token":access_token, "token_type":"bearer"}


@app.post("/user/",response_model=schemas.User)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    return crud.create_user(db=db,user=user)

@app.get("/users/",response_model=List[schemas.User])
def read_users(skip:int = 0,limit:int = 100,db:Session = Depends(get_db)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users


@app.get("/users/{user_id}",response_model=schemas.User)
def read_user(user_id:int,db:Session = Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    
    if db_user==None:
        raise HTTPException(status_code=404,detail="User not found")
    return db_user



@app.post("/items/", response_model=schemas.Item)
def create_item(item:schemas.ItemCreate,
                current_user:schemas.User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    
    
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)




@app.get("/")
def read_root() -> Dict[str,str]:
    """
    Root endpoint to check service health.
    """
    return {"status":"ok",
            "message":"System is running"}


