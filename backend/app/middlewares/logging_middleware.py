import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jose import jwt

# Importamos o settings que lê do seu .env
from app.config.settings import settings

# Usamos o logger padrão que o FastAPI/Uvicorn reconhece
logger = logging.getLogger("app")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Correlation ID: ID único para rastrear esta requisição específica
        request_id = str(uuid.uuid4())
        user_id = None
        role = None

        # Tenta extrair o usuário do Token para auditoria (Logging)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Usamos settings.SECRET_KEY e settings.ALGORITHM do seu .env
                payload = jwt.decode(
                    token, 
                    settings.SECRET_KEY, 
                    algorithms=[settings.ALGORITHM]
                )
                user_id = payload.get("sub")
                role = payload.get("role")
            except Exception:
                # Se o token for inválido, apenas ignoramos para o log não quebrar
                pass 

        # Continua o fluxo para a rota
        response = await call_next(request)

        duration = (time.time() - start_time) * 1000

        # Dados estruturados para o Log (Nível Sênior)
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration, 2),
            "user_id": user_id,
            "role": role,
        }

        # Logando a mensagem com os dados extras
        logger.info(
            f"ID: {request_id} | {request.method} {request.url.path} | "
            f"Status: {response.status_code} | Time: {round(duration, 2)}ms | User: {user_id}",
            extra={"extra_data": log_data}
        )

        # Injetamos o Request ID no cabeçalho da resposta para o Frontend
        response.headers["X-Request-ID"] = request_id

        return response
