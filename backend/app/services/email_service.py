import resend
from app.config.settings import settings


# =========================================
# CONFIG
# =========================================
resend.api_key = settings.RESEND_API_KEY


# =========================================
# CORE EMAIL SENDER
# =========================================
def send_email(to: str, subject: str, html: str):
    try:
        return resend.Emails.send({
            "from": settings.EMAIL_FROM,
            "to": to,
            "subject": subject,
            "html": html
        })
    except Exception as e:
        print("❌ PRIMARY EMAIL FAILED:", str(e))

        # FALLBACK
        return resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to,
            "subject": subject,
            "html": html
        })


# =========================================
# VERIFICATION EMAIL
# =========================================
def send_verification_email(
    to_email: str,
    code: str,
    verify_link: str
):
    html = f"""
    <h2>Verificação de Email</h2>
    <p>Seu código:</p>
    <h1>{code}</h1>

    <p>Ou clique no link abaixo:</p>
    <a href="{verify_link}">Verificar Email</a>
    """

    return send_email(
        to=to_email,
        subject="Verifique seu email",
        html=html
    )


# =========================================
# SAFE WRAPPER (NÃO QUEBRA FLUXO)
# =========================================
def send_verification_email_safe(
    to_email: str,
    code: str,
    verify_link: str
):
    try:
        print(f"📨 Enviando email para: {to_email}")

        response = send_verification_email(
            to_email=to_email,
            code=code,
            verify_link=verify_link
        )

        print("✅ Email enviado:", response)
        return True

    except Exception as e:
        print("❌ Erro ao enviar email:", str(e))
        return False