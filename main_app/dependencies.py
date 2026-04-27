import redis.asyncio as redis
from fastapi import Header, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from crud.users import AppException, decode_access_token, get_user_by_id

async def get_redis():
    client = redis.from_url("redis://localhost:6379")
    try:
        yield client
    finally:
        await client.close()

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
    
    user_id = payload.get("id") 
    if not user_id:
        raise AppException(status.HTTP_401_UNAUTHORIZED, "Invalid token payload")

    return get_user_by_id(db, int(user_id))
