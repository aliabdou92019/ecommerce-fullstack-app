from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from crud.users import (
    AppException,
    authenticate_user,
    create_access_token,
    create_user,
    decode_access_token,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from database import get_db
from schemas.users import Message, Token, UserCreate, UserLogin, UserOut, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["Authentication & Users"])

def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not authorization:
        raise AppException(status.HTTP_401_UNAUTHORIZED, "Authorization header is required")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AppException(status.HTTP_401_UNAUTHORIZED, "Invalid authorization format")

    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise AppException(status.HTTP_401_UNAUTHORIZED, "Invalid token payload")

    return get_user_by_id(db, int(user_id))
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.email, user_in.password)
    token = create_access_token({"id": user.id, "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}



@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/me", response_model=UserOut)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserOut)
def edit_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user_in)


@router.delete("/{user_id}", response_model=Message)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
