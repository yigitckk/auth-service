from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router
from app.logger import setup_logger
import structlog
  
logger = structlog.get_logger()
app = FastAPI(
    title = "Standalone Auth Service",
    description = "JWT tabanlı , Rate-limiting desteli kimlik doğrulama Service",
    version="0.1.0",
)

setup_logger()

#cors settings, devices - frontends to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #geliştirme aşamasında izinler
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

#router connetions here 
app.include_router(router)

#endpoints foundational 

@app.get("/")
async def root():
    return {
        "message": "Welcome to Auth Service API",
        "docs": "/docs", # FastAPI automatic doc navigate
    }

@app.get("/health")
async def health_chech():
    logger.info("health_check")
    return {"status": "healthy", "service": "auth-service"}


