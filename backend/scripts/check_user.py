import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User
from app.core.security import get_password_hash, verify_password

async def check_and_fix_user():
    async with AsyncSessionLocal() as session:
        # Find the test user
        result = await session.execute(
            select(User).where(User.username == "testuser")
        )
        user = result.scalar_one_or_none()
        
        if user:
            print(f"Found user: {user.username}")
            print(f"Email: {user.email}")
            print(f"Active: {user.is_active}")
            
            # Reset the password
            new_password = "securepassword123"
            user.password_hash = get_password_hash(new_password)
            await session.commit()
            print(f"✅ Password reset to: {new_password}")
            
            # Verify it works
            is_valid = verify_password(new_password, user.password_hash)
            print(f"Password verification: {is_valid}")
        else:
            print("❌ User not found")

if __name__ == "__main__":
    asyncio.run(check_and_fix_user())
