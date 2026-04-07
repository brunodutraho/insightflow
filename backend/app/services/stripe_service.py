import stripe
from app.models.plan import Plan


def create_checkout_session(db, user, plan_id, success_url, cancel_url):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        return {"error": "Plan not found"}

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price_data": {
                "currency": "brl",
                "product_data": {
                    "name": plan.name,
                },
                "unit_amount": int(plan.price * 100),
                "recurring": {
                    "interval": "month"
                },
            },
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "tenant_id": str(user.tenant_id),
            "user_id": str(user.id),
            "plan_id": str(plan.id),
        }
    )

    return {"checkout_url": session.url}