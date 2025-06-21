from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} API", "version": settings.version}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test/db")
async def test_database():
    """Test database connectivity and basic queries"""
    from app.database import AsyncSessionLocal
    from app.models import DifficultyLevelModel
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as session:
        # Get difficulty levels
        result = await session.execute(
            select(DifficultyLevelModel).order_by(DifficultyLevelModel.level_order)
        )
        levels = result.scalars().all()
        
        return {
            "status": "connected",
            "difficulty_levels": [
                {"name": level.name, "points": float(level.points)} 
                for level in levels
            ]
        }
