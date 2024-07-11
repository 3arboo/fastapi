from fastapi import Depends , status , HTTPException , APIRouter
from schemas.client_model import *
from typing import Optional
from dependencies import get_db
from database import Client
from sqlalchemy.orm import Session
import asyncio
router = APIRouter()

@router.get('/api/clients/' , tags=["Clients"])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get('/api/client/{id}' , status_code= status.HTTP_200_OK ,tags=['Clients'])
def get_client(id:int , db :Session=Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"we not found client:{id}")
    return client

@router.delete('/api/client/delete/{id}',status_code=status.HTTP_404_NOT_FOUND ,tags=['Clients'])
def remove_client(id:int , db :Session =Depends(get_db)):
    client = db.query(Client).filter(Client.id == id)
    if not client.first() :
        raise HTTPException(status_code= status.HTTP_204_NO_CONTENT , detail= f" not found:{id}")
    else:
        client.delete()
        db.commit()
        return {"msg":"delete client Done..!"}
    

@router.post('/api/client', status_code=status.HTTP_201_CREATED)
def add_client(client : Clientmodel , db :Session =Depends(get_db)):

    existing_client = db.query(Client).filter(
        (Client.id == client.id) & (Client.client_name == client.client_name)
    ).first()

    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Client with id {client.id} or client_name {client.client_name} already exists."
        )
    new_client = Client(
        id = client.id , 
        client_name= client.client_name , 
        post_url =client.post_url , 
        price=client.price,
        days_number=client.days_name , 
        is_finished = client.is_finished)
    
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"msg":"Created client Done..!"}

@router.put('/api/client' , status_code= status.HTTP_202_ACCEPTED)
def update_client(id :int ,client: Clientmodel , db : Session = Depends(get_db)):
    old_client = db.query(Client).filter(Client.id == id)
    if not old_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found this:{id}")
    
    old_client.update({
        Client.client_name : client.client_name,
        Client.price : client.price
    })
    db.commit()
    return {"msg":"Update client Done..!"}




