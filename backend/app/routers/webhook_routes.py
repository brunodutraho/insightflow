import stripe
from fastapi import APIRouter, Request, HTTPException
from app.config.settings import settings

from app.database.database import SessionLocal
from app.services.subscription_service import subscribe_to_plan
from app.models.subscription import SubscriptionStatus

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook inválido")

    db = SessionLocal()

    try:
        # Checkout finalizado (criação)
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            metadata = session.get("metadata")

            subscribe_to_plan(
                db=db,
                tenant_id=metadata["tenant_id"],
                user_id=metadata["user_id"],
                plan_id=metadata["plan_id"]
            )

        # TRIAL TERMINOU / PAGAMENTO CRIADO
        elif event["type"] == "invoice.payment_succeeded":
            # pagamento OK → mantém ativo
            pass

        # PAGAMENTO FALHOU
        elif event["type"] == "invoice.payment_failed":
            invoice = event["data"]["object"]

            # aqui você pode marcar como past_due
            # ou bloquear acesso
            print("Pagamento falhou:", invoice["id"])

        # CANCELAMENTO
        elif event["type"] == "customer.subscription.deleted":
            print("Subscription cancelada")

    finally:
        db.close()

    return {"status": "ok"}