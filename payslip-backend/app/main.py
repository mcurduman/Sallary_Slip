from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from app.api.routers.auth import auth_router
from app.api.error_handler import register_error_handlers
from app.api.routes_handler import register_routes
from app.core.config import get_settings
from app.core.middleware import log_requests
from app.core.logging import get_logger

load_dotenv()

app = FastAPI(title=get_settings().APP_NAME)

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)

@app.get("/health", response_class=JSONResponse)
async def health_check():
    return JSONResponse(content={"status": "ok"})

register_error_handlers(app)
register_routes(app)

get_logger(__name__).info("Application startup")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050, reload=True)