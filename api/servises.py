from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from datetime import datetime, timedelta
from jose import jwt

from database.connect import Session, get_db
from config.settings import settings
from api.models import User

security = HTTPBearer()


def encode_token(username):
    iat = datetime.utcnow()
    access_token = jwt.encode(
        claims=dict(sub=username,
                    iat=iat,
                    exp=iat + timedelta(minutes=settings.app_access_lifetime),
                    scope='access_token'),
        key=settings.app_secret,
        algorithm=settings.app_token_alg)
    refresh_token = jwt.encode(
        claims=dict(sub=username,
                    iat=iat,
                    exp=iat + timedelta(minutes=settings.app_refresh_token_lifetime),
                    scope='refresh_token'),
        key=settings.app_secret,
        algorithm=settings.app_token_alg)
    return dict(token_type='bearer', access_token=access_token, refresh_token=refresh_token)


def decode_token(token, scope):
    try:
        payload = jwt.decode(token, settings.app_secret, algorithms=settings.app_token_alg)
        if payload['scope'] == scope:
            return payload['sub']
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})


def get_current_user(token: str = Depends(OAuth2PasswordBearer('auth/jwt/login')), db: Session = Depends(get_db)):
    username = decode_token(token, 'access_token')
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return user


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Inactive user')
    return user


def get_current_active_admin(user: User = Depends(get_current_active_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Go away, you are not an admin')
    return user
