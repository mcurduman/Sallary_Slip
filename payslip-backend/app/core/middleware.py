import uuid
from flask import request, g, after_this_request
from structlog.contextvars import bind_contextvars, clear_contextvars

REQUEST_ID_HEADER = "x-request-id"

def request_id_middleware(app):
    @app.before_request
    def set_request_id():
        rid = request.headers.get(REQUEST_ID_HEADER, str(uuid.uuid4()))
        g.request_id = rid
        bind_contextvars(request_id=rid, path=request.path, method=request.method)

        @after_this_request
        def add_request_id_header(response):
            response.headers[REQUEST_ID_HEADER] = g.request_id
            clear_contextvars()
            return response