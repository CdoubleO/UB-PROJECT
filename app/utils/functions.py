from ..database import Base
from fastapi import HTTPException, status


def raise_404_if_not_exist(register: Base):
    if register.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"Project with id: {id} does not exist")
    return