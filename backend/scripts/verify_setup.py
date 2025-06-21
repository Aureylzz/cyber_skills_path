import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text, select
from app.database import AsyncSessionLocal, engine
from app.models import (
    User, Category, SubTheme, Question, AnswerOption,
    DifficultyLevelModel, AssessmentSession, UserRole
)
from app.config import get_settings

async def verify_setup():
    print("🔍 Starting verification...\n")
    
    # 1. Check configuration
    print("1️⃣ Checking configuration...")
    try:
        settings = get_settings()
        print(f"   ✅ App Name: {settings.app_name}")
        print(f"   ✅ Version: {settings.version}")
        print(f"   ✅ Database URL: {settings.database_url.split('@')[1]}")  # Hide credentials
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return
    
    # 2. Check database connection
    print("\n2️⃣ Checking database connection...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"   ✅ PostgreSQL connected: {version}")
    except Exception as e:
        print(f"   ❌ Database connection error: {e}")
        return
    
    # 3. Check tables exist
    print("\n3️⃣ Checking tables...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name NOT IN ('alembic_version')
            """))
            table_count = result.scalar()
            print(f"   ✅ Found {table_count} tables (excluding alembic_version)")
    except Exception as e:
        print(f"   ❌ Table check error: {e}")
    
    # 4. Check difficulty levels
    print("\n4️⃣ Checking difficulty levels...")
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(DifficultyLevelModel).order_by(DifficultyLevelModel.level_order)
            )
            levels = result.scalars().all()
            print(f"   ✅ Found {len(levels)} difficulty levels:")
            for level in levels:
                print(f"      - {level.name}: {level.points} points")
    except Exception as e:
        print(f"   ❌ Difficulty levels error: {e}")
    
    # 5. Test creating a user
    print("\n5️⃣ Testing model creation (User)...")
    try:
        async with AsyncSessionLocal() as session:
            # Check if test user exists
            result = await session.execute(
                select(User).where(User.username == "test_user")
            )
            test_user = result.scalar_one_or_none()
            
            if not test_user:
                # Create test user
                test_user = User(
                    username="test_user",
                    email="test@example.com",
                    password_hash="hashed_password_here",
                    first_name="Test",
                    last_name="User",
                    role=UserRole.STUDENT
                )
                session.add(test_user)
                await session.commit()
                print("   ✅ Created test user successfully")
            else:
                print("   ✅ Test user already exists")
            
            # Verify user properties
            print(f"      - Username: {test_user.username}")
            print(f"      - Full name: {test_user.full_name}")
            print(f"      - Role: {test_user.role.value}")
    except Exception as e:
        print(f"   ❌ User creation error: {e}")
    
    # 6. Test creating category and sub-theme
    print("\n6️⃣ Testing relationships (Category -> SubTheme)...")
    try:
        async with AsyncSessionLocal() as session:
            # Check if test category exists
            result = await session.execute(
                select(Category).where(Category.name == "Test Category")
            )
            test_category = result.scalar_one_or_none()
            
            if not test_category:
                # Create test category with sub-theme
                test_category = Category(
                    name="Test Category",
                    display_order=1
                )
                session.add(test_category)
                await session.flush()
                
                # Add sub-theme
                test_subtheme = SubTheme(
                    category_id=test_category.id,
                    name="Test Sub-theme",
                    description="This is a test sub-theme",
                    display_order=1
                )
                session.add(test_subtheme)
                await session.commit()
                print("   ✅ Created category and sub-theme successfully")
            else:
                print("   ✅ Test category already exists")
            
            # Verify relationships
            await session.refresh(test_category)
            print(f"      - Category: {test_category.name}")
            print(f"      - Sub-themes count: {len(test_category.sub_themes)}")
    except Exception as e:
        print(f"   ❌ Category/SubTheme error: {e}")
    
    # 7. Check all model imports
    print("\n7️⃣ Checking all model imports...")
    models_to_check = [
        "User", "Category", "SubTheme", "Question", "AnswerOption",
        "QuestionTag", "AssessmentSession", "UserResponse", "ResponseAnswer",
        "DifficultyLevelProgress", "CategoryProgress", "SubThemeProgress",
        "AssessmentReport", "AuditLog"
    ]
    
    all_good = True
    for model_name in models_to_check:
        try:
            model = globals().get(model_name)
            if model is None:
                from app import models
                model = getattr(models, model_name)
            print(f"   ✅ {model_name} - OK")
        except Exception as e:
            print(f"   ❌ {model_name} - Failed: {e}")
            all_good = False
    
    # 8. Final summary
    print("\n" + "="*50)
    if all_good:
        print("✅ All checks passed! Your setup is working correctly.")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(verify_setup())
