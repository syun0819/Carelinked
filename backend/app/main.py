from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.database import engine, Base, AsyncSessionLocal
from app.routers import facilities


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup: attempt to create any missing tables; skip silently if no permission
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        pass
    yield
    # shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(facilities.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-test")
async def db_test():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()
        return {"status": "connected", "postgresql_version": version}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
