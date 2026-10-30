import json
import logging
import time
import uuid
from datetime import UTC, datetime

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


request_logger = logging.getLogger("cibersegura.requests")


class JsonLogFormatter(logging.Formatter):
    """Emite registros estructurados sin cuerpos, consultas ni datos personales."""

    extra_fields = (
        "event",
        "method",
        "path",
        "status",
        "duration_ms",
        "request_id",
    )

    def format(self, record):
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in self.extra_fields:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


class RequestMetricsMiddleware:
    """Registra duración y estado por ruta, sin almacenar contenido del usuario."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))[:80]
        try:
            response = self.get_response(request)
        except Exception:
            self._log(request, request_id, started_at, 500, exception=True)
            raise

        response["X-Request-ID"] = request_id
        if request.path != "/api/health/":
            self._log(request, request_id, started_at, response.status_code)
        return response

    @staticmethod
    def _log(request, request_id, started_at, status_code, exception=False):
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        log_method = request_logger.exception if exception else (
            request_logger.warning if status_code >= 400 else request_logger.info
        )
        log_method(
            "request_completed" if not exception else "request_failed",
            extra={
                "event": "http_request",
                "method": request.method,
                "path": request.path,
                "status": status_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
            },
        )


@require_GET
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        request_logger.exception(
            "database_health_check_failed",
            extra={"event": "health_check", "status": 503},
        )
        return JsonResponse(
            {"status": "unavailable", "database": "unavailable"},
            status=503,
        )
    return JsonResponse(
        {
            "status": "ok",
            "database": "ok",
            "version": settings.APP_VERSION,
        }
    )
