from .database import Base
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

def __get_register_by_id(table: Base, db: Session, id: int):    
    return db.query(table).filter(table.id == id)


def get_register_by_id(table: Base, db: Session, id: int):    
    return db.query(table).filter(table.id == id).first()


def get_registers(table: Base, db: Session, current_user: dict):    
    #return db.query(table).all()
    return db.query(table).filter(table.created_by_user_id == current_user.id).all()


def insert_register(table: Base, db: Session, data: Base): 
    
    new_register = table(**data.dict())
    db.add(new_register)
    db.commit()
    db.refresh(new_register)
    return new_register


def delete_register(register, db: Session):

    register.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_register(register, db: Session, data: Base):
    register.update(data.dict(), synchronize_session=False)
    db.commit()

    return register.first()