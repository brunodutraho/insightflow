from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.client import Client
from app.models.subscription import Subscription
from app.schemas.client import ClientCreate, ClientResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/clients", tags=["Clients"])


# 🔹 CREATE CLIENT (com limite de plano)
@router.post("/", response_model=ClientResponse)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 🔎 busca assinatura
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id)
        .first()
    )

    if not subscription or not subscription.is_active:
        raise HTTPException(status_code=403, detail="No active subscription")

    total_clients = (
        db.query(Client)
        .filter(Client.owner_id == current_user.id)
        .count()
    )

    if total_clients >= subscription.max_clients:
        raise HTTPException(
            status_code=403,
            detail="Client limit reached for your plan"
        )

    new_client = Client(
        name=client_data.name,
        owner_id=current_user.id
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client


# 🔹 LIST CLIENTS
@router.get("/", response_model=list[ClientResponse])
def list_clients(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return (
        db.query(Client)
        .filter(Client.owner_id == current_user.id)
        .order_by(Client.id.desc())
        .all()
    )


# 🔹 GET CLIENT BY ID
@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    client = (
        db.query(Client)
        .filter(
            Client.id == client_id,
            Client.owner_id == current_user.id
        )
        .first()
    )

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


# 🔹 UPDATE CLIENT
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    client = (
        db.query(Client)
        .filter(
            Client.id == client_id,
            Client.owner_id == current_user.id
        )
        .first()
    )

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.name = client_data.name

    db.commit()
    db.refresh(client)

    return client


# 🔹 DELETE CLIENT
@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    client = (
        db.query(Client)
        .filter(
            Client.id == client_id,
            Client.owner_id == current_user.id
        )
        .first()
    )

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"message": "Client deleted successfully"}