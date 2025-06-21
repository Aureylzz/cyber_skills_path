import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import AsyncSessionLocal
from app.models import DifficultyLevelModel

async def seed_difficulty_levels():
    async with AsyncSessionLocal() as session:
        # Check if already seeded
        result = await session.execute(
            text("SELECT COUNT(*) FROM difficulty_levels")
        )
        count = result.scalar()
        
        if count > 0:
            print(f"Difficulty levels already seeded ({count} levels exist)")
            return
        
        # Create difficulty levels
        levels = [
            DifficultyLevelModel(
                name="novice",
                points=0.5,
                level_order=1,
                description="Basic awareness and fundamental concepts"
            ),
            DifficultyLevelModel(
                name="amateur",
                points=1.0,
                level_order=2,
                description="Working knowledge and practical understanding"
            ),
            DifficultyLevelModel(
                name="initiate",
                points=2.0,
                level_order=3,
                description="Intermediate skills and applied knowledge"
            ),
            DifficultyLevelModel(
                name="professional",
                points=3.5,
                level_order=4,
                description="Advanced expertise and real-world experience"
            ),
            DifficultyLevelModel(
                name="expert",
                points=5.5,
                level_order=5,
                description="Deep mastery and cutting-edge knowledge"
            ),
        ]
        
        session.add_all(levels)
        await session.commit()
        print(f"✅ Seeded {len(levels)} difficulty levels successfully!")

if __name__ == "__main__":
    asyncio.run(seed_difficulty_levels())
