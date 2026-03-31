import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.database.base import Base

class UserRole(str, enum.Enum):
    admin = "admin"     # Você (Dono do SaaS)
    gestor = "gestor"   # O assinante (Dono da conta)
    cliente = "cliente" # O cliente final do gestor

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Usando o Enum definido acima
    role = Column(Enum(UserRole), default=UserRole.cliente, nullable=False)
    
    # --- Hierarquia Sênior ---
    
    # manager_id: Aponta para outro Usuário (o Gestor)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # client_id: Aponta para a Empresa (Tabela Clients)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Relacionamentos Corrigidos (Sem Ambiguidade) ---

    # 1. Relacionamento com a Empresa (Client)
    # Especificamos 'foreign_keys' para o SQLAlchemy não confundir com o manager_id
    company = relationship(
        "Client", 
        foreign_keys=[client_id],
        back_populates="users" # Recomenda-se usar back_populates se definido no Client
    )

    # 2. Relacionamento de Hierarquia (Auto-referência)
    # Define quem são os usuários gerenciados por este usuário (subordinados)
    managed_users = relationship(
        "User",
        backref=backref("manager", remote_side=[id]),
        foreign_keys=[manager_id]
    )

    profile = relationship(
        "UserProfile", 
        back_populates="user", 
        uselist=False
    )

    # Relacionamento com Insights 
    insights = relationship("Insight", back_populates="user")
