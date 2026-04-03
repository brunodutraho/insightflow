import argparse
from app.database.init_db import init_db
from app.database.database import SessionLocal
from app.models.user import User, UserRole, UserStatus
from app.models.client import Tenant
from app.auth.utils import hash_password


def create_admin(email: str, password: str, tenant_name: str = "InsightFlow Tenant"):
    init_db()

    db = SessionLocal()
    try:
        # 🔍 Verifica se já existe admin_master
        existing = db.query(User).filter(User.role == UserRole.admin_master).first()
        if existing:
            print(f"[SKIP] admin_master already exists: {existing.email}")
            return existing

        # 🔥 CRIA USER PRIMEIRO (sem tenant ainda)
        admin_user = User(
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.admin_master,
            email_verified=True,
            status=UserStatus.active,
            terms_accepted=True
        )

        db.add(admin_user)
        db.flush()  # 👈 já gera ID sem commit

        # 🔥 AGORA cria tenant com owner correto
        tenant = Tenant(
            name=tenant_name,
            owner_id=admin_user.id
        )

        db.add(tenant)
        db.flush()

        # 🔥 Vincula tenant ao user
        admin_user.tenant_id = tenant.id

        # 🔥 COMMIT ÚNICO (atomicidade)
        db.commit()

        db.refresh(admin_user)
        db.refresh(tenant)

        print("[DONE] Admin user created")
        print(f"  id: {admin_user.id}")
        print(f"  email: {admin_user.email}")
        print(f"  tenant_id: {tenant.id}")

        return admin_user

    except Exception as e:
        db.rollback()
        print(f"[ERROR] {str(e)}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap an admin user for local development")
    parser.add_argument("--email", default="admin@example.com", help="Admin email")
    parser.add_argument("--password", default="Admin123!", help="Admin password")
    parser.add_argument("--tenant", default="InsightFlow Tenant", help="Tenant name")

    args = parser.parse_args()

    create_admin(args.email, args.password, args.tenant)