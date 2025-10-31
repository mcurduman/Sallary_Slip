from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import get_settings

cfg = get_settings()
engine = create_async_engine(
    str(cfg.database.DB_URL),       
    future=True,
    pool_pre_ping=True,
    echo=(cfg.LOG_LEVEL=="DEBUG"),
)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)