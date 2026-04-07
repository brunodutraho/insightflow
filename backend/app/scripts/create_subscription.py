from app.database.database import SessionLocal
from app.models.subscription import Subscription

db = SessionLocal()

sub = Subscription(
    user_id=1,  # 🔥 SEU ADMIN
    plan="pro",
    is_active=True
)

db.add(sub)
db.commit()

print("Subscription criada!")