import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User

async def list_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print(f"Found {len(users)} users in database:")
        for user in users:
            print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}, Active: {user.is_active}")
        
        if len(users) == 0:
            print("No users found in database!")

if __name__ == "__main__":
    asyncio.run(list_all_users())
