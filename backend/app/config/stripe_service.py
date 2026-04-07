import stripe
from app.config.settings import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user, plan):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[
            {
                "price_data": {
                    "currency": "brl",
                    "product_data": {
                        "name": plan.name,
                    },
                    "unit_amount": int(plan.price * 100),
                    "recurring": {
                        "interval": "month",
                    },
                },
                "quantity": 1,
            }
        ],
        subscription_data={
            "trial_period_days": 7, 
        },
        success_url=f"{settings.FRONTEND_URL}/billing/success",
        cancel_url=f"{settings.FRONTEND_URL}/choose-plan",
        metadata={
            "tenant_id": str(user.tenant_id),
            "user_id": str(user.id),
            "plan_id": str(plan.id),
        }
    )

    return session