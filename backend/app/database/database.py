from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# 🚀 Nível Sênior: Adicionamos timeouts e reciclagem de pool
# para evitar que o Windows/WSL2 trave a conexão
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # Verifica se a conexão está viva antes de usar
    pool_recycle=300,        # Recicla conexões a cada 5 min
    pool_size=5,             # Limita o número de conexões simultâneas
    max_overflow=10,         # Permite um estouro temporário
    connect_args={
        "connect_timeout": 5 # Se o banco não responder em 5s, ele desiste (destrava o app)
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
