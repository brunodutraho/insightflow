import logging
import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("app")


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except Exception as e:
            logger.error(
                "error_occurred",
                extra={
                    "extra_data": {
                        "path": request.url.path,
                        "method": request.method,
                        "error": str(e),
                        "trace": traceback.format_exc(),
                    }
                },
            )
            raise e