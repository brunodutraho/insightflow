from app.database.base import Base
from app.database.database import engine

from app.models import user, insight, client, subscription, ad_account, ad_metric



def init_db():
    Base.metadata.create_all(bind=engine)