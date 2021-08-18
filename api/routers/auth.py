from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.connect import get_db
from api.models import User
from api.schemes import UserSet, UserGet, Token
from api.servises import security, encode_token, decode_token, get_current_active_user

auth_router = APIRouter(prefix="/auth/jwt", tags=['auth'])


@auth_router.post('/register', status_code=201, response_model=Token)
def register(data: UserSet, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    user = User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return encode_token(user.username)


@auth_router.post('/login', response_model=Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        UserSet(username=data.username, password=data.password)
    except Exception:
        raise credentials_exception
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not user.verify(data.password):
        raise credentials_exception
    return encode_token(user.username)


@auth_router.get('/refresh_token', response_model=Token)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    username = decode_token(credentials.credentials, 'refresh_token')
    return encode_token(username)


@auth_router.get('/profile', response_model=UserGet)
def profile(user: User = Depends(get_current_active_user)):
    return user
