from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

from fastapi import Security
from fastapi.security.api_key import APIKeyHeader
from app.models.project import ApiKey, Project

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def get_project_by_api_key(
    db: Session = Depends(get_db), api_key_header: str = Security(api_key_header)
) -> Project:
    if not api_key_header:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    
    token = api_key_header.replace("Bearer ", "") if api_key_header.startswith("Bearer ") else api_key_header
    
    api_key_obj = db.query(ApiKey).filter(ApiKey.key_hash == token).first()
    if not api_key_obj:
        raise HTTPException(status_code=403, detail="Could not validate API key")
        
    project = db.query(Project).filter(Project.id == api_key_obj.project_id).first()
    if not project:
        raise HTTPException(status_code=403, detail="Project not found")
        
    return project