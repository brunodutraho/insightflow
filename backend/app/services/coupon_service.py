from sqlalchemy.orm import Session
from app.models.coupon import Coupon


def get_all_coupons(db: Session):
    return db.query(Coupon).all()


def create_coupon(db: Session, data: dict):
    coupon = Coupon(**data)
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


def update_coupon(db: Session, coupon_id: int, data: dict):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()

    if not coupon:
        return None

    for key, value in data.items():
        setattr(coupon, key, value)

    db.commit()
    db.refresh(coupon)

    return coupon