
from fastapi import Request
import time
import uuid
from app.core.logging import get_logger

async def log_requests(request: Request, call_next):
    logger = get_logger("middleware")
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    logger.info(f"Request ID: {request_id} - {request.method} {request.url}")
    start_time = time.perf_counter()
    response = None
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Request ID: {request_id} - Error: {str(e)}")
        raise e
    finally:
        process_time = (time.perf_counter() - start_time) * 1000
        status_code = getattr(response, "status_code", "N/A") if response is not None else "N/A"
        logger.info(f"Request ID: {request_id} - Completed in {process_time:.2f}ms with status {status_code}")
