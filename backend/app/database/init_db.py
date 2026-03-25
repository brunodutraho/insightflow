from app.database.base import Base
from app.database.database import engine

from app.models import user, insight, client, subscription



def init_db():
    Base.metadata.create_all(bind=engine)